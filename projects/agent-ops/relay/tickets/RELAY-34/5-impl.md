# [impl] 소설 자산 NAI 이미지화 — 캐릭터·세계 디자인 연습
- jira: RELAY-34
- 커밋 목록(해시 + 한 줄):
  - (이 commit) RELAY-34 1차 산출 — NAI 생성 파이프라인 확정 + 캐릭/세계 디자인 10종 프롬프트 정본
- 테스트 결과(명령과 출력 요약):
  - 모델 확정: nai-diffusion-3 (v4.5-full=500, 4-5/4-5-click=400 → 전부 불가, Opus 구독이어도 v3만 응답)
  - 인증: image.novelai.net + persistent token Bearer, 브라우저 UA 필수 (python 기본 UA=Cloudflare 1010)
  - 응답 형식: raw ZIP(binary/octet-stream, PK 헤더) → zipfile로 image_0.png 추출
  - 무료 사이즈 832x1216 기준 10종 생성 성공 (개당 ~3초, Anlas 미소비)
  - 전달: 이사님 Telegram 10장 발송 완료 (01-10)
- spec 대비 이탈 및 사유:
  - 원천: novel_assets 34작품 완결 components 중 시각 특징 뚜렷한 캐릭터/세계 선별
  - PNG 바이너리는 Git 미반입(용량) — prompts 정본(batch1/batch2 JSON)만 커밋, 이미지는 이사님 승인 시 구글 드라이브 알피지 저장고로

## 업로드 (2026-08-22 이사님 승인)
- 위치: `matrix-upload:RPG저장고/NAI_캐릭터디자인_1차/` (10종 전체, 15.5MiB)
- 원격 메모: matrix-upload가 rclone 공유 client_id 사용 중 — 2026년 중 폐기 예정 NOTICE. 전용 client_id 발급 필요할 수 있음(매니저 안건).
