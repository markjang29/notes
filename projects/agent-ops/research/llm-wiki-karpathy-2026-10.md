---
title: "LLM Wiki 패턴 분석 — Karpathy gist 회수 (query → 위키 누적 1호)"
date: 2026-10-26
status: active
tags:
  - research
  - llm-wiki
  - knowledge-base
  - agent-ops
source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
authority: 이사님 10-26 지시 "읽어보고 우리 회사에 적용 가능한 방법좌" + 승인 "고고"
---

# LLM Wiki 패턴 분석 (Karpathy, 2026-10)

> 이 문서는 LLM Wiki의 "좋은 답변은 채팅에 묻히지 말고 위키 페이지로 저장하라" 원칙의
> 첫 적용 사례다 — 이사님 요청으로 수행한 gist 분석을 notes에 회수했다.

## 원문 핵심

- **RAG와의 차이**: RAG는 매 질문마다 지식을 원본에서 재조립(축적 없음). LLM Wiki는
  **LLM이 직접 만들고 계속 유지하는 마크다운 위키**를 원본과 사용자 사이에 둔다.
  지식은 한 번 정리되어 계속 최신으로 유지된다(compounding artifact).
- **3층 구조**: 원본(불변·source of truth) / 위키(LLM이 작성·유지) / 스키마
  (CLAUDE.md류 — 구조·규약·작업 절차를 규정, LLM을 "훈련된 위키 관리자"로 만드는 설정).
- **3개 운영**: Ingest(소스 1건이 위키 10~15페이지를 갱신 — 요약·인덱스·교차참조·로그까지),
  Query(답변을 위키에 회수해 탐색이 축적되게), Lint(주기 건강검진 — 모순·stale·고아·빠진 참조).
- **작동 이유**: 인간 위키가 죽는 원인은 유지관리(교차참조·요약 최신화)의 지루함.
  LLM은 지루하지 않으니 유지비용≈0 — 위키가 살아있다. 사람은 소스 큐레이션·질문·해석 담당.

## 우리 구조와의 대응

- 위키 = **notes Git 정본**(principles/decisions/projects) — 글의 팁 "위키는 그냥 git repo"와 동일.
- 인덱스 = **policy-index-v1.json**(id/종류/제목/eli5/요약/ref) — 글의 index.md 역할, eli5 포함으로 더 강함.
- 스키마 = **L0-agent-common.md + agent-rules.md**(+ 각 CLAUDE.md) — 96_ 사칙의 CLAUDE.md
  계층화 제안이 바로 이 층 강화에 해당함을 확인(외부 근거).
- 열람 UI = **8024 /rules·/comm** — 글의 Obsidian 브라우징 역할 + ACK 추적.
- 원본 층 = 각 프로젝트 저장소·이사님 지시 원문·외부 문서(본 gist 포함).

## 채택 결정 (이사님 10-26 승인)

1. **Query → 위키 회수**: 분석·비교·조사 결과를 `projects/agent-ops/research/` 에 누적.
   본 문서가 1호.
2. **정기 lint(건강검진)**: 월 1회 감사(aws-audit)가 notes 전체 점검·보고.
   1차 결과: `projects/agent-ops/audits/notes-lint-2026-10.md`.
3. **주제 허브 페이지 시범**: `topics/communication.md`(1호 — 통신). lint에서 참조 무결성 점검.
4. **ingest 절차 명시(제안 초안 — 별도 승인 대기)**: 새 정본 문서 커밋 시
   ① policy-index 등록 ② 상호참조 갱신(관련 문서 역링크) ③ 해당 topics 허브 갱신까지
   한 커밋 세트로. 스키마(L0 또는 agent-rules)에 절차 문구 추가 제안.

## 미채택 (원문이 오히려 확인해줌)

- 임베딩 RAG 인프라·qmd 검색엔진 — 원문 "인덱스 파일이 ~100 소스 규모에서 충분".
  현재 정본 22건 규모엔 과투자. grep+인덱스 유지.
- Obsidian 전용 도구(Web Clipper, Dataview 등) — 8024 투영이 같은 역할 수행 중.

## 상호 참조

- 관련: `projects/agent-ops/audits/notes-lint-2026-10.md` · `topics/communication.md`
- 스키마 계층 논의: `principles/ai-dev-신념.md`(96_ 사칙 초안 맥락)
