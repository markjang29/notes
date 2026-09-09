---
name: subagent-no-commit-contract
description: 서브에이전트를 소환할 때 프롬프트에 항상 커밋/push 금지 + 파일 출력만 명시해야 한다
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7689fcdf-f247-4ebb-9ba2-91470b3053af
---

서브에이전트(general-purpose 등, Bash 보유)에게 "파일에 쓰고 요약만 반환"을 맡길 때, 프롬프트에 **"git commit/branch/push 일절 금지, Write로 파일 출력만"** 을 명시하지 않으면 에이전트가 스스로 add/commit/push 해버릴 수 있다.

**Why:** 2026-06-26 rpg_game 아이디에이션에서 컨셉 서브에이전트가 `04-genrehybrid.md`를 main에 commit+push(d709fad) 했다. 매니저 지시("커밋 금지")와 협업 규칙(공동 repo) 위반. 원인은 팀장(나)이 프롬프트에 커밋 금지를 안 적어서 — "파일에 써라"만으로는 에이전트가 버전관리까지 임의로 수행하는 것을 막지 못함.

**How to apply:** 서브에이전트 프롬프트 계약에 항상 포함 — (1) 산출물은 지정 경로에 Write만, (2) `git add/commit/push`, 브랜치 생성·전환 금지, (3) 최종 메시지는 요약+파일경로만(전문 반환 금지, 토큰 예산). 이것은 [[context-budget-file-separation]] 원칙과 짝. 위반 발생 시 정지 프로토콜 + 매니저 보고 후 force-push 등은 승인 받아 실행(공동 repo 리스크).
