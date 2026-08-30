# 컨텍스트 방전 체크포인트 — manager
- 시각: 2026-08-21 21:23:22 KST
- 모드: check
- 측정: 📊 glm-5.3[1m] | 한계 1,000,000 | 735,188 (73.5%) | 13.6MB
- 퍼센트: 73.5%

## 활성 작업 (work-queue.md 상단)
```
# Work Queue — markjang29 dev

> 매니저(`@heav_lnx_bot`) 전관. 활성 작업·대기 결정·다음 스텝만 유지한다.
> 과거 상세는 Git 이력, `work-archive.md`, checkpoints를 본다.
> **2026-08-16 갱신**: 07-12 정지 이후 5주 공백 반영(Windows 종료, Matrix 통합 후임 인계,
> zcode 클라이언트 승계). 07-10~07-12 야간 사이클·승인보드 상세는 `work-archive.md`
> '2026-08-16 아카이브' 섹션으로 이동.

## ★ Matrix 통합 후임 (2026-08-16)

- 담당 actor: `aws-manager`
- 교대 결정: `decisions/2026-08-16-matrix-successor-handoff.md`
- 전체 정본: `matrix_asset_agent` 최신 main의 `collaboration/MATRIX-SUCCESSOR-HANDOFF.md`
- 현재 카드: `NEXT-001` 동일조건 Codex/ZCODE/RISU 품질시험
- Clear는 대화 컨텍스트만 지울 수 있다는 뜻이며, 제품 완료나 서비스 정상 판정이 아니다.
- 아래 한 문장으로 새 세션을 시작한다.

```text
너는 Matrix 통합 후임이다. matrix_asset_agent 최신 main의 collaboration/MATRIX-SUCCESSOR-HANDOFF.md를 전부 읽고 [MATRIX-SUCCESSOR-CERT]를 출력한 뒤, 문서에 적힌 전체 Git의 최신 origin/main과 역할 경계를 재검증하고 NEXT-001부터 작은 카드로 실행·검사·commit·push·보고하라.
```

## 조직 현황 (2026-08-16, actors.json v8)

- Windows Codex·ZCode 구독 종료(08-16). 신규 **zcode 클라이언트**(telegram-zcode-bridge 구동)가
  승계자로 활동 중.
- zcode 클라이언트가 이어받음:
  - Windows 자산 수집 파이프라인(아카 수집/다운로드/디코딩/중복제거 → `matrix_asset_agent` 입고).
    노하우 정본은 Windows 인수인계 문서 `handover-2026-08-16.md`, 이식 착수 예정.
  - 매니저가 직접 실행 금지라 비어있던 '직접 실행 작업자' 역할(예: 8011 ZCODE 서비스 복구).
  - 팀장 봇이 content policy로 blocked 남긴 기계적 처리(성인 픽션 포함 소설 수집·가공·카탈로그) 이관.
    정책 유지: NSFW를 이유로 버리지 않고 동일 provenance/security/quality gate.
- 매니저(`@heav_lnx_bot`): 조율·배정·보고 전관 + **LIVING-DRAMA-OS(Matrix) 통합 작업자 겸직**.
  repo 범위에 matrix 7종(`matrix_asset_agent`/`scenario`/`matrix`/`matrix_zcode`/`matrix_codex`/
  `matrix-engine`/`matrix-living-drama`) + `music_video`(08-08 추가) 포함.
- `aws-trader`: 07-16 이사님 지시로 pause. 재개는 이사님 결정.
- 퇴역 windows-codex/windows-zcode 잔여 권한(크론·approval-board 클라이언트 토큰·시스템 프롬프트)
  감사: 08-16 감사봇 의뢰 진행 중(아래 대기 결정 #3).

## Matrix 다음 카드 (NEXT-001~005; 정본은 handoff 문서)

1. **NEXT-001 동일조건 품질시험** — 같은 모델·요청·온도·출력 예산 고정, 8011/8012/RISU를
   첫 장면·10턴·20턴·재개로 비교. 실행 결과 없이 승자 선언 금지.
2. NEXT-002 사건 코어 흡수 결정 — `matrix-engine` vs `matrix-living-drama` event schema/reducer/
   checkpoint/replay 비교 → 8012 command bus·SQLite 경계 안에서 수렴. donor 재구현 금지.
3. NEXT-003 reviewed 시츄에이션 10개 — 사람 승인 후 같은 release ID로 8011·8012에 공급.
```

## git 상태 — scenario
status:
?? catalog/operations/director_console.sqlite3
?? "novel_assets/works/\352\262\200\354\235\200_\354\227\254\354\232\260_\353\217\205\354\213\254\355\230\270\353\246\254_2\353\266\200_\352\267\200\355\230\270/"
?? "novel_assets/works/\353\252\205\354\230\210\353\241\234\354\232\264_\353\271\214\353\237\260\354\235\264_\353\220\230\352\262\240\353\213\244/"
?? "novel_assets/works/\354\243\274\354\235\270\352\263\265_\352\260\221\354\247\210\353\247\214\354\204\270/"
?? "novel_assets/works/\354\247\201\352\260\220\354\234\274\353\241\234_\353\266\200\354\236\220_\353\220\240\353\236\230\354\232\224/"
?? "novel_assets/works/\354\260\275\354\262\234\353\254\264\354\213\240/"
log:
f4a14f7 docs(archmap): scenario repo 아키텍처 맵 graph 정본 (15노드·4플로우)
5eb5722 docs(novel): 08-17 토큰 소비 세션 정리 — 28/28 확정 + 다음주 재개 지침 보존
e3306fa docs(novel): 체크포인트 갱신 — 34작품·457 components (Wave4 완결)

## git 상태 — rpg_game
status:
?? OVERNIGHT_2026-07-12.md
?? ideation/DRAFT-parry-handfeel-one-breath.md
?? ideation/OVERNIGHT_2026-07-09.md
?? ideation/WIP-second-battle-full-match-script.md
?? ideation/WIP-second-battle-signature-fusion.md
?? ideation/WIP-second-battle-win-lose-fork.md
log:
79681e9 design: 공격 분류(상/중/하+타입, 격투게임식) — 패링 전 긴장 층 (이사님 2026-07-26 아이디어)
235feea design: core-incarnation 세계 간 이동 = 하이브리드 해금 확정 (이사님 2026-07-26, 옵션 2번 선택)
296c3a5 design: 코어 빙의(정체성 핵→세계 캐릭터) (이사님 2026-07-26 아이디어)

## git 상태 — autotrader
status:
 M research/WIP-weight-slide-results-v1-draft.md
?? OVERNIGHT_2026-07-12.md
?? research/OVERNIGHT_2026-07-09.md
?? research/WIP-adr-rest-api-port-ownership-v1-draft.md
?? research/WIP-compass-decision-flow-v1-draft.md
?? research/WIP-quarter-run-experience-v1-draft.md
?? research/WIP-strategy-instance-trade-v1-draft.md
log:
1277e72 야간배정 07-11: trader 팀장 지시문 (07-10 밤 결과 기반)
704e29e OVERNIGHT 2026-07-10: 2022 인플레 딥다이브 + weight-slide 하이브리드 대안
e20e9f5 보존(감사브리프 긴급): 미추적 산출물 일괄 — IDEATION/strategy-spec-v1/api/backtest/dashboard/research/run_backtest/analysis_exit_ratio

## 세션·복구 포인터
- canonical memory: /home/ubuntu/.claude/projects/-home-ubuntu--cokacdir-workspace-akl0hdys/memory
- 복구入口: akl0hdys memory MEMORY.md → work-queue.md
- CLAUDE_CODE_SESSION_ID: 4c29ca0f-e00c-4c5a-b76d-8995f37bb471
- transcript 힌트: /home/ubuntu/.claude/projects/-home-ubuntu--cokacdir-workspace-xjp2kqhu/4c29ca0f-e00c-4c5a-b76d-8995f37bb471.jsonl

## 복구 지침
1. /clear (또는 신규 세션). cron --session 으로 같은 세션 resume 금지(누적 폭발 원인).
2. 위 활성 작업·미커밋 변경부터 마무리.
3. memory + work-queue.md 기반 복구 (clear-recovery-map 참조).
4. 1M 폭발 재발 방지: work-queue/memory 통째 주입 억제, WebSearch dump 발췌만.
