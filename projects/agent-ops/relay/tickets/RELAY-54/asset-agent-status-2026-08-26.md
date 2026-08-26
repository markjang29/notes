# asset_agent 상태 표시 (RELAY-54, 2026-08-26)

기준: 이사님 AWS Zcode 대화 100건 · 정합성 장부 지시.
Jira 404(RELAY-35/41/50/54/55/56)는 gap으로 남김 — 완료 처리하지 않음.
구현 커밋: matrix_asset_agent `e5d8838` (도구 city_nsfw/city_master/city_tags + 규격 docs/ASSET-MASTER-SPEC.md).

## 담당 사이트·산출물 상태

| 대상 | 상태 | 비고 |
|---|---|---|
| 8015 자산 도시·게시판·사전·로드아웃·RISU 디플로이 | 구현됨 | cb05f11 등 · live 검증 완료. 3턴 워크벤치 부분은 AWS ZCode 담당이라 본 표에서 제외 |
| 8008 matrix-candidate 관측 | 검증불가 | HTTP 200 응답 확인만 — 내부 카드·리스트 정합성 미검증 |
| P-3 risupreset 전역 설정 반영 | 부분구현 | 13건 디코드 완료, 원클릭 적용 잔여 (덮어쓰기 안전장치 설계 필요) |
| P-3 로어북 단독 주입 | 미구현 | 유형 조사·실사 전 |
| RELAY-24 페르소나 324 파싱 | 미구현 (의도적 보류) | TRACK-1 체험 승인 전 착수 금지 규칙 준수 |

## 금일 구현 (장부 지시분)

| 산출물 | 상태 | 근거 |
|---|---|---|
| NSFW·일반 자산 분리 | 구현됨 | 전수 2,037종 = 성인 635 · 일반 1,402. 신호 5종(이름/mcat/게시글시그널/카탈로그/게시글카테고리), 근거 `nsfw_evidence` 전건 보존. 포탈 🌿/🔞 칩 + 리스트 🔞 배지 (블락 아닌 필터) |
| 마스터 자산번호 + sha256 alias | 구현됨 | `asset_master` 대장 MA-00001~002037 전량 부여 · city_assets join 완료. sha256 해싱 백그라운드 진행 (원본 77GB). 멱등 규칙: path→sha256→신규 |
| 장르 태그 체계 | 부분구현 | 이사님 6축(여성향·무협·판타지·현대물·연애소설·웹소설식)+보조 3. K분류 매핑+키워드 1차 559종. 정밀화는 검토카드→이사님 판정 절차 대기 |

## 정리필요 (매니저 건의)

- **8015 실행 주체 충돌**: AWS ZCode 세션이 systemd 유닛 프로세스를 kill 후 nohup
  (RELAY_TICKET=RELAY-56)으로 기동 → 포트 점유로 유닛 재시작이 반복 실패함.
  systemd 상주로 복구 완료(동일 코드, 기능 변화 없음). 재발 방지를 위해
  port-registry 8015 항목에 상주 방식(`systemd --user matrix-workbench`) 명시 필요.
- matrix_asset_agent repo에 타 봇(ZCode) commits 유입 중 — 공유 repo 규칙(pull→push) 준수 확인 필요.
