---
name: projects-and-collaboration
description: "Two shared projects (autotrader, rpg_game) and multi-agent cross-machine collaboration rules"
metadata: 
  node_type: memory
  type: project
  originSessionId: 471bf542-7577-448f-8d74-7dd7548495f8
---

사용자가 함께 진행 중인 프로젝트 2개 (2026-06-25 기준):
- **autotrader** (자동매매 시스템) — github.com/markjang29/autotrader, 로컬 `~/projects/autotrader`. 스택 미확정(Python 권장).
- **rpg_game** (파랜드 택틱스풍 전술 SRPG) — github.com/markjang29/rpg_game, 로컬 `~/projects/rpg_game`. 엔진 미확정(Godot 권장).

**다중 에이전트 협업**: 본 Linux 서버(Claude Code) 외에 Windows 머신에 별도 에이전트가 같은 저장소들을 공유함.

**Why:** 코드/작업이 두 머신에서 동시에 진행되므로, 분리·누락·충돌 방지를 위해 모든 작업을 명시적으로 공유해야 한다.
**How to apply:** 모든 변경/결정/진행상황은 (1) 해당 프로젝트 git 저장소에 커밋, (2) 전반 맥락은 `~/notes`(github.com/markjang29/notes)에 상세 기록. 작업 전 `git pull`, 후 즉시 `git push`. 커밋 작성자는 `markjang29` / `markjang29@users.noreply.github.com` (GitHub noreply).
연관: [[workspace-layout]]
