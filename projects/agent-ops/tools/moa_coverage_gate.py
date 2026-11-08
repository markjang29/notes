#!/usr/bin/env python3
"""MOA coverage reference validator. Trusted normalized inputs only; no network I/O.

This is a pilot contract, not an authentication service or a production audit ledger.
All demo identities and evidence references are fictional.
"""
import argparse
import copy
import hashlib
import json
import re
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

STAGES = ('received', 'delivered', 'ack', 'executing', 'submitted', 'verified')
LABELS = ('접수', '전달', 'ACK', '실행', '제출', '검수')
IDENT = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}$')
SHA = re.compile(r'^[a-f0-9]{64}$')


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def timestamp(value):
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        raise ValueError('timezone required')
    return dt


def require(ok, message):
    if not ok:
        raise ValueError(message)


def validate(scope, events, as_of):
    now = timestamp(as_of)
    for key in ('version', 'run_id'):
        require(bool(IDENT.fullmatch(scope[key])), 'invalid ' + key)
    hosts, actors = scope['hosts'], scope['actors']
    require(hosts and len(hosts) == len(set(hosts)), 'unique hosts required')
    require(all(IDENT.fullmatch(h) for h in hosts), 'invalid host id')
    require(type(scope['max_age_seconds']) is int and scope['max_age_seconds'] > 0,
            'positive freshness window required')
    actor_ids = [a['actor_id'] for a in actors]
    require(all(IDENT.fullmatch(a) for a in actor_ids), 'invalid actor id')
    require(len(actor_ids) == len(set(actor_ids)), 'duplicate actor id')
    identity_keys = [a['identity_key'] for a in actors]
    require(all(isinstance(k, str) and k for k in identity_keys), 'identity key required')
    require(len(identity_keys) == len(set(identity_keys)), 'identity aliases not reconciled')
    required = scope['required_actor_ids']
    require(required and len(required) == len(set(required)), 'nonempty fixed denominator required')
    require(set(required) <= set(actor_ids), 'required actor absent from manifest')
    by_id = {a['actor_id']: a for a in actors}
    for actor in actors:
        require(actor['host_id'] in hosts, 'unknown host')
        require(actor['kind'] in ('agent', 'service', 'human'), 'invalid actor kind')
        require(actor['lifecycle'] in ('active', 'paused', 'retired', 'excluded'), 'invalid lifecycle')
        if actor['actor_id'] in required:
            require(actor['kind'] == 'agent' and actor['lifecycle'] in ('active', 'paused'),
                    'required bots must remain active or paused')
        else:
            require(bool(actor.get('exclusion_reason')) and bool(actor.get('exclusion_ref')),
                    'omission requires explicit reason and approval reference')
    reviewers = scope['reviewers']
    require(reviewers and all(IDENT.fullmatch(r) for r in reviewers), 'reviewer ids required')
    rec = scope['reconciliation']
    require(type(rec['approved']) is bool and isinstance(rec['unresolved'], list), 'invalid reconciliation')
    started = timestamp(scope['started_at'])
    require(started <= now, 'run starts in future')
    scope_hash = digest(scope)
    problems = set()
    if not rec['approved'] or not rec.get('evidence_ref') or rec['unresolved']:
        problems.add('scope_unreconciled')
    seen, normalized, ignored = {}, [], 0
    for event in events:
        if event.get('run_id') != scope['run_id']:
            ignored += 1
            continue
        if event.get('scope_sha256') != scope_hash:
            problems.add('scope_mismatch')
            continue
        try:
            require(bool(IDENT.fullmatch(event['event_id'])), 'invalid event id')
            require(event['actor_id'] in by_id, 'unknown actor')
            require(event['stage'] in STAGES, 'unknown stage')
            require(type(event['ok']) is bool, 'boolean outcome required')
            require(bool(event['evidence_ref']), 'evidence reference required')
            received, occurred = timestamp(event['received_at']), timestamp(event['occurred_at'])
            require(started <= occurred <= received <= now, 'timestamp outside run or future')
            if event['stage'] in ('submitted', 'verified'):
                require(bool(SHA.fullmatch(event['artifact_sha256'])), 'artifact hash required')
            payload = canonical(event)
            if event['event_id'] in seen:
                require(seen[event['event_id']] == payload, 'conflicting duplicate event')
                continue
            seen[event['event_id']] = payload
            normalized.append(event)
        except (KeyError, TypeError, ValueError):
            problems.add('invalid_event')
    counts = dict.fromkeys(STAGES, 0)
    rows = []
    cutoff = now - timedelta(seconds=scope['max_age_seconds'])
    for actor_id in sorted(required):
        relevant = [e for e in normalized if e['actor_id'] == actor_id]
        latest = {}
        for event in sorted(relevant, key=lambda e: (timestamp(e['occurred_at']), e['event_id'])):
            previous = latest.get(event['stage'])
            if previous and previous['occurred_at'] == event['occurred_at'] and previous != event:
                problems.add('ambiguous_stage_event')
            latest[event['stage']] = event
        passed, missing, stale = {}, [], False
        previous_time = started
        evidence = {}
        for stage in STAGES:
            event = latest.get(stage)
            ok = bool(event and event['ok'])
            if event:
                occurred = timestamp(event['occurred_at'])
                fresh = occurred >= cutoff
                stale = stale or not fresh
                ok = ok and fresh and occurred >= previous_time
                previous_time = occurred
                evidence[stage] = event['evidence_ref']
            if stage == 'verified' and event:
                submitted = latest.get('submitted')
                ok = ok and bool(submitted) and event['artifact_sha256'] == submitted.get('artifact_sha256')
                ok = ok and event.get('reviewer_id') in reviewers and event.get('reviewer_id') != actor_id
            # A later stage must never silently manufacture missing ACKs or submissions.
            ok = bool(ok and all(passed.values()))
            passed[stage] = ok
            counts[stage] += int(ok)
            if not ok:
                missing.append(stage)
        rows.append({'actor_id': actor_id, 'host_id': by_id[actor_id]['host_id'],
                     'lifecycle': by_id[actor_id]['lifecycle'], 'stages': passed,
                     'missing': missing, 'stale': stale, 'evidence': evidence})
    host_counts = []
    for host in hosts:
        host_rows = [r for r in rows if r['host_id'] == host]
        host_counts.append({'host_id': host, 'expected': len(host_rows),
                            'verified': sum(r['stages']['verified'] for r in host_rows)})
        if not host_rows:
            problems.add('host_without_expected_bots')
    return {'schema': 'moa-coverage-result-v1', 'run_id': scope['run_id'],
            'scope_version': scope['version'], 'scope_sha256': scope_hash,
            'as_of': now.isoformat(), 'max_age_seconds': scope['max_age_seconds'],
            'expected': len(required), 'excluded': len(actors) - len(required),
            'counts': counts, 'problems': sorted(problems), 'ignored_other_runs': ignored,
            'complete': not problems and counts['verified'] == len(required),
            'hosts': host_counts, 'rows': rows}


def render_mdx(result):
    # Only fixed labels, validated identifiers, numbers and ISO time enter executable MDX.
    lines = ["export const title = '00 봇 커버리지 — 판정 시점 스냅샷'",
             "export const group = '운영'", 'export const order = 0',
             "export const date = '" + result['as_of'][:10] + "'", '',
             '# 봇 커버리지', '',
             '**주의: 자동 생존 확인 화면이 아닙니다. 판정 시점 이후 상태는 재수집해야 합니다.**', '',
             '판정: ' + ('검수 충족' if result['complete'] else '미충족'),
             '', '판정 시점: ' + result['as_of'], '',
             '명부 해시: `' + result['scope_sha256'] + '`', '',
             f"대상 {result['expected']} / 명시적 제외 {result['excluded']}", '',
             ' | '.join(('접수', '전달', 'ACK', '실행', '제출', '검수')), '|---|---|---|---|---|---|',
             ' | '.join(str(result['counts'][s]) + '/' + str(result['expected']) for s in STAGES), '',
             '| 봇 | 장비 | 상태 | 미충족 단계 |', '|---|---|---|---|']
    for row in result['rows']:
        missing = ', '.join(LABELS[STAGES.index(s)] for s in row['missing']) or '없음'
        state = '오래됨' if row['stale'] else ('검수 충족' if not row['missing'] else '미충족')
        lines.append(f"| {row['actor_id']} | {row['host_id']} | {state} | {missing} |")
    lines += ['', '## 명부 및 입력 점검', '']
    lines += ['- ' + p for p in result['problems']] or ['- 명부·입력 조건 충족']
    lines += ['', '검수 충족은 이 점검 실행의 증거 조건을 충족했다는 뜻입니다. 제품 구현 완료와 다릅니다.',
              '원본 증거는 coverage.json의 evidence 참조로 확인합니다. 이 도구는 링크 내용이나 발신자 신원을 인증하지 않습니다.', '']
    return '\n'.join(lines)


def demo():
    scope = {'version': 'demo-v1', 'run_id': 'demo-run-1',
             'started_at': '2026-11-08T00:00:00Z', 'max_age_seconds': 300,
             'hosts': ['host-a', 'host-b', 'host-c'],
             'required_actor_ids': ['bot-a', 'bot-b', 'bot-c'],
             'actors': [{'actor_id': 'bot-' + x, 'host_id': 'host-' + x,
                         'kind': 'agent', 'lifecycle': 'active', 'identity_key': 'fictional-' + x}
                        for x in 'abc'],
             'reviewers': ['reviewer'],
             'reconciliation': {'approved': True, 'evidence_ref': 'fixture:scope-review', 'unresolved': []}}
    events = []
    for x in 'abc':
        for i, stage in enumerate(STAGES):
            at = f'2026-11-08T00:00:{i + 1:02d}Z'
            events.append({'event_id': f'event-{x}-{i}', 'actor_id': 'bot-' + x,
                           'run_id': scope['run_id'], 'scope_sha256': digest(scope),
                           'stage': stage, 'ok': True, 'occurred_at': at, 'received_at': at,
                           'evidence_ref': 'fixture:' + x + '-' + stage,
                           'artifact_sha256': 'a' * 64, 'reviewer_id': 'reviewer'})
    return scope, events, '2026-11-08T00:00:30Z'


def self_test():
    s, e, at = demo()
    results = []
    def check(name, condition):
        require(condition, 'TEST FAILED: ' + name)
        results.append({'name': name, 'passed': True})
    def run(scope=None, events=None, when=None):
        return validate(scope if scope is not None else s, events if events is not None else e, when or at)
    def rebound(scope):
        out = copy.deepcopy(e)
        for event in out:
            event['scope_sha256'] = digest(scope)
        return out
    def rejects(scope):
        try:
            run(scope, rebound(scope))
            return False
        except ValueError:
            return True
    baseline = run()
    check('complete_fixture', baseline['complete'] and baseline['expected'] == 3)
    missing = run(events=[x for x in e if x['actor_id'] != 'bot-c'])
    check('missing_bot_kept', missing['expected'] == 3 and missing['counts']['verified'] == 2 and not missing['complete'])
    check('missing_host_visible', next(h for h in missing['hosts'] if h['host_id'] == 'host-c')['expected'] == 1)
    check('duplicate_event_idempotent', run(events=e + e) == baseline)
    check('arrival_order_independent', run(events=list(reversed(e))) == baseline)
    check('all_missing_not_complete', not run(events=[])['complete'])
    check('all_stale_not_complete', not run(when='2026-11-08T00:10:00Z')['complete'])
    for field, value, name in [('run_id', 'older-run', 'old_run_not_counted'),
                               ('scope_sha256', 'b' * 64, 'wrong_scope_not_counted'),
                               ('actor_id', 'unknown-bot', 'unknown_bot_not_counted'),
                               ('occurred_at', '2026-11-09T00:00:00Z', 'future_event_not_counted'),
                               ('evidence_ref', '', 'missing_evidence_not_counted')]:
        altered = copy.deepcopy(e)
        for item in altered:
            item[field] = value
        check(name, not run(events=altered)['complete'])
    check('missing_ack_blocks_later_stages', not run(events=[x for x in e if x['stage'] != 'ack'])['counts']['verified'])
    altered = copy.deepcopy(e)
    altered[-1]['reviewer_id'] = altered[-1]['actor_id']
    check('self_review_rejected', not run(events=altered)['complete'])
    altered[-1]['reviewer_id'] = 'stranger'
    check('unknown_reviewer_rejected', not run(events=altered)['complete'])
    altered = copy.deepcopy(e)
    altered[-1]['artifact_sha256'] = 'b' * 64
    check('review_bound_to_artifact', not run(events=altered)['complete'])
    failed = dict(e[-1], event_id='revoke-review', ok=False,
                  occurred_at='2026-11-08T00:00:20Z', received_at='2026-11-08T00:00:20Z')
    check('later_failed_review_revokes_pass', not run(events=e + [failed])['complete'])
    collision = dict(e[-1], ok=False)
    check('conflicting_duplicate_blocks_pass', not run(events=e + [collision])['complete'])
    scope = copy.deepcopy(s)
    scope['reconciliation']['unresolved'] = ['unmapped-candidate']
    check('unmapped_candidate_blocks_all_clear', not run(scope, rebound(scope))['complete'])
    scope = copy.deepcopy(s)
    scope['reconciliation']['approved'] = False
    check('unapproved_scope_blocks_all_clear', not run(scope, rebound(scope))['complete'])
    scope = copy.deepcopy(s)
    scope['actors'][2]['lifecycle'] = 'paused'
    check('paused_bot_kept', run(scope, rebound(scope))['expected'] == 3)
    scope = copy.deepcopy(s)
    scope['actors'][1]['identity_key'] = scope['actors'][0]['identity_key']
    check('duplicate_identity_rejected', rejects(scope))
    scope = copy.deepcopy(s)
    scope['actors'].pop()
    check('deleted_required_row_rejected', rejects(scope))
    scope = copy.deepcopy(s)
    scope['required_actor_ids'].pop()
    check('silent_exclusion_rejected', rejects(scope))
    scope = copy.deepcopy(s)
    scope['hosts'].append('host-empty')
    check('empty_host_blocks_all_clear', not run(scope, rebound(scope))['complete'])
    scope = copy.deepcopy(s)
    scope['actors'].append({'actor_id': 'service-observer', 'host_id': 'host-a', 'kind': 'service',
                            'lifecycle': 'active', 'identity_key': 'fictional-service',
                            'exclusion_reason': 'service tracked separately', 'exclusion_ref': 'fixture:approval'})
    check('service_not_in_bot_denominator', run(scope, rebound(scope))['expected'] == 3)
    check('scope_change_invalidates_prior_evidence', not run(scope, e)['complete'])
    check('zero_denominator_rejected', rejects(dict(s, required_actor_ids=[])))
    with tempfile.TemporaryDirectory() as folder:
        file = Path(folder) / 'snapshot.json'
        file.write_text(json.dumps({'scope': s, 'events': e}), encoding='utf-8')
        restored = json.loads(file.read_text(encoding='utf-8'))
        check('snapshot_replay_identical', validate(restored['scope'], restored['events'], at) == baseline)
    check('mdx_contains_missing_actor', 'bot-c' in render_mdx(missing))
    check('deterministic_repeat', digest(run()) == digest(baseline))
    return {'tests': len(results), 'passed': len(results), 'result_sha256': digest(baseline), 'cases': results,
            'boundary': 'Local contract fixtures only. No real bot, HTTP, browser, server or evidence-link validation.'}


def write_outputs(folder, result):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'coverage.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (folder / '00-coverage.mdx').write_text(render_mdx(result), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['self-test', 'demo', 'validate'])
    parser.add_argument('--scope', type=Path)
    parser.add_argument('--events', type=Path)
    parser.add_argument('--as-of', help='Explicit ISO timestamp with timezone, required for validate')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if args.mode == 'self-test':
        print(json.dumps(self_test(), ensure_ascii=False, indent=2))
        return 0
    if args.mode == 'demo':
        scope, events, at = demo()
        require(args.out is not None, '--out required')
        args.out.mkdir(parents=True, exist_ok=True)
        for name, value in [('scope.json', scope), ('events.json', events)]:
            (args.out / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    else:
        require(all([args.scope, args.events, args.as_of, args.out]), '--scope --events --as-of --out required')
        scope = json.loads(args.scope.read_text(encoding='utf-8'))
        events = json.loads(args.events.read_text(encoding='utf-8'))
        at = args.as_of
    result = validate(scope, events, at)
    write_outputs(args.out, result)
    print(json.dumps({k: result[k] for k in ('expected', 'counts', 'complete', 'problems')}, ensure_ascii=False))
    return 0 if result['complete'] else 1


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False))
        raise SystemExit(2)
