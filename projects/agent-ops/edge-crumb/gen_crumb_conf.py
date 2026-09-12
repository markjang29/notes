#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""edge-crumb v1 생성기 — 이사님 지시(전 페이지 상단 트리경로 링크 + 기술·고유ID 표기).
sites.json(8024 포털 카탈로그)에서 nginx http-level sub_filter conf를 생성한다.
- map "$server_port::$uri" → 사이트별 (메타+브레드크럼바) HTML
- 8024(홈), 8018(자체 배너 보유), :80 루트/게이트/스프링 내부경로는 제외(주입 없음)
- 8023은 메타만 주입(가시 바 제외): 소스 레벨 정적 트리바 보유 — 이중 렌더 방지(코덱스 실측 2026-09-12)
"""
import json, sys

HOME = 'http://43.201.34.144:8024/'
SITES = 'http://43.201.34.144/sites'

def esc(s):  # conf 안전화: 백슬래시·작은따옴표 제거(값은 nginx 작은따옴표 문자열로 래핑)
    return s.replace('\\', '').replace("'", '')

def bar(site_id, name, cat, stack):
    n, c, st = esc(name), esc(cat), esc(stack)
    return (
        '<div data-matrix-crumb style="position:sticky;top:0;z-index:99999;'
        'background:#0b1220;color:#cfe0ff;border-bottom:1px solid #2a3a5a;'
        'padding:6px 10px;font:700 11.5px/1.5 system-ui,sans-serif">'
        '<a href="' + HOME + '" style="color:#9fc5ff;text-decoration:none">🏠 홈</a>'
        ' › <a href="' + SITES + '" style="color:#9fc5ff;text-decoration:none">' + c + '</a>'
        ' › <b>' + n + '</b>'
        ' · <span style="color:#93a2bd">기술 ' + st + '</span>'
        ' · <span style="color:#93a2bd">ID ' + esc(site_id) + '</span>'
        '<span class="mcrumb-path" style="color:#6d7a92;font-weight:400"></span>'
        '</div>'
        '<script>(function(){var e=document.querySelector("[data-matrix-crumb] .mcrumb-path");'
        'if(e){e.textContent=" · 페이지 "+location.pathname;}})();</script>'
    )

def meta(site_id, stack):
    # 네이밍 컨벤션: heav_aws512 소스 레벨 메타(site-id · implemented-with)와 정렬
    return ('<meta name="site-id" content="' + esc(site_id) + '">'
            '<meta name="implemented-with" content="' + esc(stack) + '">'
            '<meta name="crumb-source" content="edge-crumb v1 GM윈도 2026-09-12">')

sites = {str(s['port']): s for s in json.load(open(sys.argv[1], encoding='utf-8'))}  # port 타입 정규화(문자열/정수 호환)

# 주입 대상: nginx listen 포트 (8018 자체배너·8024 홈 제외, 미리슨 포트 8002/8011/8016/8017 제외)
PORTS = ['8003','8004','8005','8006','8008','8009','8010','8012','8013',
         '8015','8020','8021','8022','8023','8025','8027','8030','8100']
# 소스 레벨 자체 표기 실태(2026-09-13 tailscale 전수 순회) 반영 — 엣지 중복 방지:
BAR_EXCLUDE_PORTS = {'8023'}   # 소스 정적 트리바 보유 → 엣지는 메타만
EDGE_SKIP_PORTS = {'8009'}     # 소스가 메타+바 모두 자체 보유 → 엣지 개입 없음
BAR_ONLY_PORTS = {'8004', '8021', '8100'}  # 소스 메타 보유 → 엣지는 바만(메타는 소스에 위임)
SID_OVERRIDE = {'8004': 'arcade-8004', '8021': 'studio-8021', '8100': 'envsync-8100'}  # 바 표시 ID 소스 정합
META_ONLY_EXTRA = [('8024', 'portal-8024')]  # 포털 홈(SPA) 무표기 — 엣지 메타만 보강(6debe42 병합분)
# :80 경로 라우트 (사이트 ID는 경로 기준, 카탈로그 port와 연결)
PATHS = [
    ('/arcade/',        'arcade',       sites['8004']),
    ('/drawing/',       'drawing-8765', None),  # NUC 드로잉 앱
    ('/drawing2/',      'drawing2-8766',None),  # NUC 드로잉 Spring v2
    ('/assets/',        'drawing2-8766',None),
    ('/src-img/',       'drawing-8765', None),
    ('/insa/',          'insa-roster',  None),  # NUC 인사 로스터
    ('/studio/',        'studio-8021',  sites['8021']),
    ('/studio-spring/', 'drawing2-8766',None),
]

def entry(html):
    if html is None:
        return '        "";\n'
    v = bar(*html) if isinstance(html, tuple) else html
    m = meta(html[0], html[2]) if isinstance(html, tuple) else ''
    full = (m + v) if m else v
    return "        '" + full + "';\n"

out = []
out.append('# matrix-crumb.conf — edge-crumb v1 (GM윈도, 2026-09-12)\n')
out.append('# 이사님 지시: 전 페이지 상단 트리경로(홈›카테고리›사이트) 링크 + 기술스택·고유ID 표기.\n')
out.append('# 정본: notes repo projects/agent-ops/edge-crumb/ · 생성기: gen_crumb_conf.py\n')
out.append('# 미적용(의도): 8024 홈 자체, 8018(자체 배너 보유), 미리슨 포트(8002/8011/8016/8017/8765/8766)\n\n')
out.append('sub_filter_once on;\n')
out.append('sub_filter \'<head>\' \'<head>$matrix_meta_html\';\n')
out.append('sub_filter \'<body\' \'$matrix_bar_html<body\';\n')
out.append('proxy_set_header Accept-Encoding "";\n\n')

def map_block(varname, html_fn, exclude_ports=(), extra_ports=()):
    lines = ['map "$server_port::$uri" ' + varname + ' {\n', '    default "";\n']
    for p in PORTS:
        if p in exclude_ports:
            continue
        s = sites[p]
        sid = SID_OVERRIDE.get(p, p)
        lines.append('    ~^' + p + ':: ' + html_fn(sid, s['name'], s['category'], s['stack']))
    for p, sid in extra_ports:
        s = sites[p]
        lines.append('    ~^' + p + ':: ' + html_fn(sid, s['name'], s['category'], s['stack']))
    for prefix, sid, s in PATHS:
        if s:
            lines.append('    ~^80::' + prefix + ' ' + html_fn(sid, s['name'], s['category'], s['stack']))
        else:
            name, cat, stack = {
                'drawing-8765': ('드로잉 앱', '그림·이미지', 'Node.js · Drawing UI'),
                'drawing2-8766': ('드로잉 Spring v2', '그림·이미지', 'Spring Boot · Thymeleaf/JavaScript'),
                'insa-roster': ('인사 로스터', '관제', 'Node.js · HTML'),
            }[sid]
            lines.append('    ~^80::' + prefix + ' ' + html_fn(sid, name, cat, stack))
    lines.append('}\n')
    return lines

def meta_entry(sid, name, cat, stack):
    return "        '" + meta(sid, stack) + "';\n"

def bar_entry(sid, name, cat, stack):
    return "        '" + bar(sid, name, cat, stack) + "';\n"

out.extend(map_block('$matrix_meta_html', meta_entry,
                     exclude_ports=EDGE_SKIP_PORTS | BAR_ONLY_PORTS,
                     extra_ports=META_ONLY_EXTRA))
out.append('\n')
out.extend(map_block('$matrix_bar_html', bar_entry,
                     exclude_ports=EDGE_SKIP_PORTS | BAR_EXCLUDE_PORTS))

sys.stdout.write(''.join(out))
