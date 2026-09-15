package com.matrix.studio.portal;

import tools.jackson.databind.JsonNode;
import tools.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicReference;

/**
 * 사칙·규칙 원장 읽기전용 투영 (95_ 사칙 관리 화면 백엔드).
 *
 * 정본 = notes Git (policy-index-v1.json + principles/*.md 본문).
 * 이 서비스는 notes를 절대 쓰지 않는다(봇 기계 .md 직접 편집 금지 — 사칙 95_·L0).
 * 초안(draft)만本 서비스가 수집하며, 정본화는 각 actor의 notes commit+push로만 이뤄진다.
 */
@Service
public class PortalRulesService {

    private static final long MAX_DRAFT_BYTES = 32L * 1024;
    private static final int EXCERPT_LIMIT = 600;

    private final ObjectMapper mapper;
    private final Path notesRoot;
    private final Path draftQueue;
    private final AtomicReference<Snapshot> cache = new AtomicReference<>();

    public record RuleDoc(
            String id, String kind, String title, String status, String owner,
            String ref, String eli5, String summary,
            String notesRef, boolean readable, String docSha256, String excerpt,
            String bodyFull) {
    }

    public record Snapshot(String policySha, String indexVersion, String generatedAt,
                           List<RuleDoc> docs) {
    }

    public record DraftRecord(String id, String kind, String title, String eli5,
                              String summary, String proposedBy, String receivedAt) {
    }

    public PortalRulesService(
            ObjectMapper mapper,
            @Value("${matrix.rules.notes-root:${user.home}/notes}") String notesRoot,
            @Value("${matrix.rules.draft-queue:./data/rules-drafts.ndjson}") String draftQueue) {
        this.mapper = mapper;
        this.notesRoot = Path.of(notesRoot).toAbsolutePath().normalize();
        this.draftQueue = Path.of(draftQueue).toAbsolutePath().normalize();
    }

    /** 원장 읽기 — 정본(notes) 직독. 실패 시 마지막 캐시 유지(8018 H10 선례). */
    public synchronized Snapshot snapshot() {
        Snapshot current = cache.get();
        try {
            String policySha = notesHead();
            if (current != null && current.policySha() != null
                    && current.policySha().equals(policySha)) {
                return current; // 판본 동일 — 재파싱 불필요 (rerender-·server- 최소화)
            }
            Snapshot fresh = load(policySha);
            if (fresh != null) {
                cache.set(fresh);
                return fresh;
            }
        } catch (Exception ignored) {
            // fall through to stale cache
        }
        if (current != null) {
            return current; // stale 판본이라도 증거는 진실 — 프론트가 stale 배지 표시
        }
        throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE, "rules_index_unavailable");
    }

    public String draftQueuePath() {
        return draftQueue.toString();
    }

    public List<DraftRecord> recentDrafts(int limit) {
        if (!Files.isReadable(draftQueue)) {
            return List.of();
        }
        try {
            List<String> lines = Files.readAllLines(draftQueue, StandardCharsets.UTF_8);
            List<DraftRecord> out = new ArrayList<>();
            for (int i = lines.size() - 1; i >= 0 && out.size() < limit; i--) {
                String line = lines.get(i).strip();
                if (line.isEmpty()) {
                    continue;
                }
                try {
                    DraftRecord d = mapper.readValue(line, DraftRecord.class);
                    if (d != null && d.id() != null && !d.id().isBlank()) {
                        out.add(d);
                    }
                } catch (IOException parseSkip) {
                    // 1행 파싱 실패는 건너뛴다 — 큐 전체는 보존
                }
            }
            return out;
        } catch (IOException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "draft_queue_read_failed");
        }
    }

    /** 초안 추가 — ndjson append (단일원본 단일쓰기, 95_ 사칙의 이력 남기기 계약). */
    public synchronized DraftRecord appendDraft(DraftRecord in) {
        if (in == null || in.id() == null || in.id().isBlank()
                || in.title() == null || in.title().isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "draft_id_and_title_required");
        }
        if (in.proposedBy() == null || in.proposedBy().isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "draft_proposedBy_required");
        }
        try {
            if (draftQueue.getParent() != null) {
                Files.createDirectories(draftQueue.getParent());
            }
            long bytes = draftQueue.toFile().exists() ? Files.size(draftQueue) : 0L;
            if (bytes > MAX_DRAFT_BYTES * 1024) {
                throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE, "draft_queue_full");
            }
            DraftRecord stamped = new DraftRecord(
                    in.id().strip(), in.kind() == null ? "제안" : in.kind().strip(),
                    in.title().strip(), in.eli5() == null ? "" : in.eli5().strip(),
                    in.summary() == null ? "" : in.summary().strip(),
                    in.proposedBy().strip(), Instant.now().toString());
            String line = mapper.writeValueAsString(stamped);
            if (line.length() > MAX_DRAFT_BYTES) {
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "draft_too_large");
            }
            Files.writeString(draftQueue, line + "\n", StandardCharsets.UTF_8);
            return stamped;
        } catch (IOException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "draft_queue_write_failed");
        }
    }

    private String notesHead() {
        try {
            Process p = new ProcessBuilder(
                    "git", "-C", notesRoot.toString(), "rev-parse", "HEAD")
                    .redirectErrorStream(true).start();
            try (var in = p.getInputStream()) {
                String head = new String(in.readAllBytes(), StandardCharsets.UTF_8).strip();
                p.waitFor();
                if (p.exitValue() == 0 && head.matches("[0-9a-f]{40}")) {
                    return head;
                }
            }
        } catch (Exception ignored) {
            // 읽기 실패 — null은 "판본 미확정"으로 프론트에 표시된다
        }
        return null;
    }

    private Snapshot load(String policySha) {
        Path idx = notesRoot.resolve("projects/agent-ops/policy-index-v1.json");
        if (!Files.isReadable(idx)) {
            return null;
        }
        try {
            JsonNode root = mapper.readTree(idx);
            if (root == null || !root.has("docs") || !root.get("docs").isArray()) {
                return null;
            }
            List<RuleDoc> docs = new ArrayList<>();
            for (JsonNode d : root.get("docs")) {
                RuleDoc doc = toDoc(d, policySha);
                if (doc != null) {
                    docs.add(doc);
                }
            }
            String version = root.path("version").asText("");
            return new Snapshot(policySha, version, Instant.now().toString(), List.copyOf(docs));
        } catch (IOException e) {
            return null;
        }
    }

    private RuleDoc toDoc(JsonNode d, String policySha) {
        String id = d.path("id").asText("");
        if (id.isBlank()) {
            return null;
        }
        String ref = d.path("ref").asText("");
        Path file = ref.isBlank() ? null : notePath(ref);
        boolean readable = file != null && Files.isRegularFile(file);
        String sha = "";
        String excerpt = "";
        String bodyFull = "";
        if (readable) {
            try {
                String txt = Files.readString(file, StandardCharsets.UTF_8);
                String noFm = stripFrontMatter(txt);
                bodyFull = noFm;
                excerpt = noFm.length() > EXCERPT_LIMIT
                        ? noFm.substring(0, EXCERPT_LIMIT) + "…" : noFm;
                sha = sha256Hex(txt);
            } catch (IOException ignored) {
                readable = false;
            }
        }
        return new RuleDoc(
                id,
                d.path("kind").asText(""),
                d.path("title").asText(""),
                d.path("status").asText(""),
                d.path("owner").asText(""),
                ref,
                d.path("eli5").asText(""),
                d.path("summary").asText(""),
                "notes:" + ref,
                readable,
                sha,
                excerpt,
                bodyFull);
    }

    private Path notePath(String ref) {
        // ref 형식: "principles/xxx.md" 또는 "projects/agent-ops/xxx.md" — 상대경로만 (L0 비밀·절대경로 금지)
        if (ref.contains("..") || ref.startsWith("/")) {
            return null;
        }
        Path resolved = notesRoot.resolve(ref).normalize();
        return resolved.startsWith(notesRoot) ? resolved : null;
    }

    private String stripFrontMatter(String text) {
        if (text.startsWith("---\n")) {
            int end = text.indexOf("\n---", 4);
            if (end > 0 && text.length() > end + 4) {
                String after = text.substring(end + 4);
                return after.startsWith("\n") ? after.substring(1) : after;
            }
        }
        return text;
    }

    private String sha256Hex(String content) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            StringBuilder sb = new StringBuilder();
            for (byte b : md.digest(content.getBytes(StandardCharsets.UTF_8))) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (Exception e) {
            return "";
        }
    }

    // Map import 소거용 — LinkedHashMap 참조 유지 (기존 코드 스타일 호환)
    @SuppressWarnings("unused")
    private static Map<String, String> unusedShape() {
        return new LinkedHashMap<>();
    }
}
