# INFRA#16 [A4] run.sh 봇 토큰 평문(7개) → token-file 전환 — 승인게이트(이사님 승인 후 반영) (2026-10-02, 98)
## 재현 (운영 무변경)
- /home/smlime21/.local/state/cokacdir/run.sh: `exec cokacdir --ccserver -- '<7개 토큰, 1줄>'` (값 마스킹)
- ps 출력: pid 1511690 명령행에 토큰 7개 평문 — 프로세스 목록 노출 실측(진단 일치)
- cokacdir --help: `--ccserver-token-file <PATH>`(1행 1토큰, "recommended")·`--ccserver-stdin` 지원, 현재는 legacy `--ccserver <TOKEN>...` 사용
- 로그: "token arguments are visible in process listings; use --ccserver-token-file" 경고도 이미 존재
## 준비 (전환안 — 적용은 이사님 승인 후. 토큰 값 본문 기입 금지, 경로만)
1. 토큰파일 신설: ~/.cokacdir/bot_keys/ccserver.tokens(1행 1토큰, 7개, chmod 600)
   - 생성: 현재 run.sh에서 토큰 부분만 추출해 1행씩 배치(스크립트로, 값은 출력하지 않음)
2. run.sh 교체: `exec cokacdir --ccserver-token-file ~/.cokacdir/bot_keys/ccserver.tokens`
   - 기존 run.sh는 run.sh.bak-A4로 백업(이미 run.sh.bak-migration 존재 — 추가)
3. 재시작: systemctl --user restart cokacdir (데몬 — 순단 순간. 사이드카 각성 3단(PIPE#60)이 있어 무해)
4. 검증: `ps`로 새 데몬 명령행에 토큰 없음(--ccserver-token-file 경로만), cokacdir.log에 7봇 등록 확인, 각 봇 --whoami/메시지 1건 수발신 무결
5. 기존 토큰 교체 검토는 **별도 건**(진단 문구 "교체 검토" — 본 건은 경로 전환만. 교체시 8023 .env·bot_settings.json 등 참조처 동시 변경 필요 — 이사님 결정 사항)
## 롤백
- run.sh.bak-A4 원복+재시작(토큰값 불변 — 서비스 무영향)
