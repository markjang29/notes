# rclone 전용 client_id 만들기 (구글드라이브 스로틀 해소)

**왜**: `matrix-upload` 리모트가 rclone 공유 client_id를 써서 구글 쓼스로틀을 받는 중
(3시간에 3,600파일). 공유 id는 2026년 안에 만료 예고(rclone 공식 경고). 전용 id는
할당량이 분리되어 속도도 빨라지고 만료도 없음.

**소요**: 브라우저 작업 약 10분 (구글 계정 로그인 필요 — 에이전트가 대신 못 함)

## 절차
1. https://console.cloud.google.com 접속 (heav 구글 계정으로)
2. 상단 프로젝트 선택 → 새 프로젝트: `rclone-backup`
3. 좌측 "API 및 서비스" → "라이브러리" → **Google Drive API** 검색 → 사용
4. "OAuth 동의 화면": External → 앱명 `rclone-backup`, 이메일만 채우고 저장.
   "테스트 사용자"에 본인 계정 추가 (게시 안 해도 테스트 모드로 충분)
5. "사용자 인증 정보" → "사용자 인증 정보 만들기" → OAuth 클라이언트 ID →
   유형 **데스크톱 앱** → 만들기 → **클라이언트 ID / 클라이언트 보안 비밀** 메모
6. gmlnx에서:
```bash
rclone config update matrix-upload client_id <ID> client_secret <SECRET>
# 토큰 재발급 (기존 토큰은 옛 id용이라 무효화됨)
rclone config reconnect matrix-upload:
# 확인
rclone about matrix-upload:
```
7. AWS도 같은 Drive 계정을 쓰면 AWS의 rclone 설정에도 같은 id/secret 적용
   (AWS 접속 후 `rclone config update` + `reconnect`)

## 검증
다음 새벽 동기화 로그(`/gdive/.sync/gdrive-sync.log`)에서
"shared Google Drive client_id" 경고가 사라지고 전송 속도가 올라가면 성공.
