# Matrix topology control plane 홈 컷오버 (2026-09-10)

## 판정

- **완료**: Matrix 원사이트의 React Flow 구성도와 안전한 배포 제어면을 구현하고 AWS 8GB 서버에서 홈 `duradev`로 8024 런타임을 전환했다.
- 공개 읽기 화면: `http://43.201.34.144:8024/flow`
- 관리 화면: `http://43.201.34.144:8024/control/flow`
- 엣지 경로: `43.201.34.144:8024` → `100.109.91.0:8024` (`duradev`)
- AWS의 기존 `matrix-studio-spring.service`는 **stopped + disabled** 상태다.

## Git 정본

| 범위 | 저장소 / 정본 | 확인 내용 |
|---|---|---|
| Spring + React Flow | `markjang29/matrix-studio-spring` `73110e87dfc9f8f78587af3b65f1b1be118a7e97` | topology API, v2 seed, UI, 정적 번들, 테스트, 홈 user-unit |
| 홈 사이트맵 | `markjang29/matrix-home` `aef3864` | 홈 카드와 `/sites` 8024 항목을 `/flow`에 연결 |
| 큰그림 설계 | `notes/projects/agent-ops/topology-graph-v1.md` 등 | 전체 컴퓨터·AWS·봇·사이트 연결 모델 |

## 홈 배치

```text
/home/smlime21/projects/matrix-studio-spring
/home/smlime21/services/matrix-studio-spring/releases/73110e87dfc9f8f78587af3b65f1b1be118a7e97/app.jar
/home/smlime21/services/matrix-studio-spring/current -> releases/73110e87...
/home/smlime21/.local/state/matrix-studio-spring/data/chain.mv.db
/home/smlime21/.local/state/matrix-studio-spring/topology/
/home/smlime21/.config/matrix-studio-spring/env
/home/smlime21/.config/systemd/user/matrix-studio-spring-8024.service
/home/smlime21/.local/lib/jvm/java-17-openjdk-amd64
/home/smlime21/.local/lib/apache-maven-3.8.7
/home/smlime21/.m2/repository
```

- `env`는 0600이며 실제 `TOPOLOGY_ADMIN_TOKEN`과 외부 상태 경로만 담는다. 토큰은 Git·문서·로그에 기록하지 않았다.
- 홈에는 포터블 full JDK 17.0.20, Maven 3.8.7, Maven 오프라인 캐시와 프런트 `node_modules`가 이관됐다.
- 홈 자체에서 `mvn -o test`와 Vite production build를 다시 통과했다.
- JAR SHA-256: `2818dffce47c86470faf32feccc399cad16d8ad95b7bb3ba751e3c6d3f496974`
- 컷오버 H2 SHA-256: `254153af89807b001b02a30c071d9ab0556294159427790c2accb57a2c6d8b76`
- 홈 DB 백업: `chain.mv.db.pre-cutover-20260909T150322Z`

## 구현된 안전 경계

- `/flow`는 읽기 전용, `/control/flow`만 세션 토큰으로 편집한다.
- 관리 토큰은 브라우저 `sessionStorage`에만 두고 모든 쓰기는 `X-Topology-Admin-Token`으로 인증한다.
- Save Draft → Validate → Plan → Deploy 순서를 강제한다.
- immutable revision + SHA-256, expected active revision/digest CAS, idempotency key, 감사 이력을 적용했다.
- Deploy는 `CONFIG_PROMOTION_ONLY`다. shell, SSH, systemd, Docker, nginx, 클라우드 API를 실행하지 않는다.
- 비밀 필드·실행 명령·잘못된 참조·순환·desired/observed 불일치·빈 inventory를 서버가 거부한다.

## 검증 증거

- Java 단위/보안 회귀 테스트: **11/11 PASS**.
- Vite: **204 modules**, v2 seed **22 nodes / 26 edges** 왕복 보존.
- 홈 `mvn -o test`와 홈 Vite build 통과.
- 홈 `/`, `/flow`, `/control/flow`, `/api/topology`, `/api/topology/state`, `/api/zones`, `/api/basket` 모두 HTTP 200.
- 공개 엣지 `/`, `/flow`, `/control/flow`, `/api/topology/state`와 JS asset 모두 HTTP 200.
- 실제 홈 API에서 save → validate → plan → deploy → 동일 요청 replay를 실행했고 `valid=true`, generation 2, `idempotentReplay=true`를 확인했다.
- 무인 재기동: user-unit enabled/active, `Linger=yes`.
- 홈 8018 사이트맵도 공개 `/flow` 링크를 노출하고 재기동 확인했다.

## 복구/확인

```bash
ssh duradev 'systemctl --user status matrix-studio-spring-8024.service --no-pager'
ssh duradev 'curl -fsS http://127.0.0.1:8024/api/topology/state'
curl -fsS http://43.201.34.144:8024/flow >/dev/null
```

장애 시에는 홈 DB의 `pre-cutover` 백업과 immutable 이전 release를 사용한다. AWS 서비스는 삭제하지 않았지만 중지·비활성화했으므로, 홈 장애를 확인하지 않고 임의 재활성화하지 않는다.

## 새 세션 인수인계 문장

`관제, 홈 duradev의 ~/notes/projects/agent-ops/migration/2026-09-10-matrix-topology-home-cutover.md와 matrix-studio-spring 73110e8을 정본으로 읽고 user-unit·43.201.34.144:8024/flow·/control/flow 상태부터 검증한 뒤 남은 전체 토폴로지 작업만 이어가줘.`
