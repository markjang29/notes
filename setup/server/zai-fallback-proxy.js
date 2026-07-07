#!/usr/bin/env node
/**
 * zai-fallback-proxy.js — Z.ai 과부하(529) 자동 폴백 로컬 프록시
 *
 * 목적: cokacdir가 띄운 Claude Code가 Z.ai(glm-5.2[1m], 1M 컨텍스트)에 요청할 때
 *       짧은 요청은 표준 모델(glm-5.2) 백업으로 살리고, 긴 요청은 1M 컨텍스트를
 *       보장하기 위해 표준 모델로 몰래 낮추지 않는다.
 *
 * 보안: 인증(AUTH_TOKEN)은 클라이언트가 보낸 Authorization 헤더를 그대로 upstream으로 relay.
 *       프록시 자체는 토큰을 저장/출력하지 않는다.
 *
 * 적용: ~/.cokacdir/.env.json 에 "ANTHROPIC_BASE_URL": "http://127.0.0.1:8788" 추가 후 cokacdir 재시작.
 *
 * 환경변수(기본값):
 *   ZAI_UPSTREAM       https://api.z.ai/api/anthropic   실제 Z.ai 엔드포인트
 *   PROXY_PORT         8788                             로컬 수신 포트
 *   FALLBACK_MODEL     glm-5.2                          짧은 요청에서만 치환할 표준 모델
 *   OVERLOAD_MODELS    glm-5.2[1m]                      폴백 대상 1M 변형(콤마 구분)
 *   STANDARD_FALLBACK_MAX_BYTES 204800                  이 크기 이하 요청만 표준 모델 백업 허용
 *   MAX_ATTEMPTS       4                                원본 1 + 폴백 재시도 3
 *   PROXY_LOG          ~/.local/state/cokacdir/zai-fallback-proxy.log
 *
 * ADR: ~/notes/decisions/2026-07-01-zai-fallback-proxy.md
 */
'use strict';

const http = require('http');
const https = require('https');
const fs = require('fs');
const os = require('os');
const path = require('path');

const UPSTREAM       = process.env.ZAI_UPSTREAM    || 'https://api.z.ai/api/anthropic';
const PORT           = parseInt(process.env.PROXY_PORT || '8788', 10);
const FALLBACK_MODEL = process.env.FALLBACK_MODEL  || 'glm-5.2';
const OVERLOAD_MODELS= (process.env.OVERLOAD_MODELS || 'glm-5.2[1m]').split(',').map(s => s.trim()).filter(Boolean);
const STANDARD_FALLBACK_MAX_BYTES = parseInt(process.env.STANDARD_FALLBACK_MAX_BYTES || '204800', 10);
const MAX_ATTEMPTS   = parseInt(process.env.MAX_ATTEMPTS || '4', 10);
const LOG_PATH       = process.env.PROXY_LOG || path.join(os.homedir(), '.local/state/cokacdir/zai-fallback-proxy.log');

// --- 폴백 텔레그램 알림 (선택) ---
const NOTIFY_CHAT     = process.env.NOTIFY_CHAT || '';           // 알림 받을 chat_id (없으면 알림 안 함)
const NOTIFY_BATCH_MS = parseInt(process.env.NOTIFY_BATCH_MS || '90000', 10);
function loadNotifyBotToken() {
  if (process.env.NOTIFY_BOT_TOKEN) return process.env.NOTIFY_BOT_TOKEN;
  try { // 기존 cokacctl.json 의 첫 봇 토큰 재사용 (평문 비밀 추가 회피)
    return JSON.parse(fs.readFileSync(path.join(os.homedir(), '.cokacdir/cokacctl.json'), 'utf8')).tokens[0] || '';
  } catch { return ''; }
}
const NOTIFY_BOT = loadNotifyBotToken();

const upstreamUrl = new URL(UPSTREAM);
const upstreamMod = upstreamUrl.protocol === 'https:' ? https : http;
const UPSTREAM_PORT = upstreamUrl.port || (upstreamUrl.protocol === 'https:' ? 443 : 80);
const UPSTREAM_PATH_BASE = upstreamUrl.pathname.replace(/\/+$/, ''); // '/api/anthropic'

function ts() { return new Date().toISOString(); }
function log(line) {
  const msg = `${ts()} ${line}`;
  try { fs.appendFileSync(LOG_PATH, msg + '\n'); } catch {}
  if (process.env.PROXY_STDERR === '1') console.error(msg);
}
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const backoffMs = (a) => Math.min(8000, (1 << (a - 1)) * 1000); // 1,2,4,8s

// --- 텔레그램 알림 전송 ---
let _recoverCount = 0, _lastRecoverNotify = 0, _lastGaveupKey = '';
function tgSend(text) {
  if (!NOTIFY_CHAT || !NOTIFY_BOT) return;
  try {
    const data = JSON.stringify({ chat_id: NOTIFY_CHAT, text, parse_mode: 'Markdown', disable_web_page_preview: true });
    const u = new URL(`https://api.telegram.org/bot${NOTIFY_BOT}/sendMessage`);
    const r = https.request({ method: 'POST', hostname: u.hostname, path: u.pathname,
      headers: { 'content-type': 'application/json', 'content-length': Buffer.byteLength(data) } });
    r.on('error', () => {});
    r.end(data);
  } catch (e) { log(`NOTIFY-ERR ${e.message}`); }
}
function notifyRecovered(fromModel, toModel, usage, reqBytes) {
  _recoverCount++;
  const now = Date.now();
  if (now - _lastRecoverNotify >= NOTIFY_BATCH_MS) { // 첫 폴백 즉시, 이후 배치(90s)
    let line = `🔄 *Z.ai 529 폴백*\n${fromModel} 과부하 → *${toModel}* 회피`;
    const parts = [];
    if (reqBytes) parts.push(`요청 ${(reqBytes/1024).toFixed(1)}KB`);
    if (usage && usage.input) parts.push(`입력 ${usage.input.toLocaleString()}토큰`);
    if (usage && usage.output) parts.push(`출력 ${usage.output.toLocaleString()}토큰`);
    if (parts.length) line += '\n' + parts.join(' · ');
    line += `\n최근 ${Math.round(NOTIFY_BATCH_MS/1000)}초 ${_recoverCount}회 응답 정상 복구`;
    tgSend(line);
    _recoverCount = 0; _lastRecoverNotify = now;
  }
}
// 응답 본문(SSE/non-stream)에서 토큰 usage 추출
function extractUsage(buf) {
  const u = {};
  const mi = buf.match(/"input_tokens"\s*:\s*(\d+)/);
  if (mi) u.input = +mi[1];
  const outs = buf.match(/"output_tokens"\s*:\s*(\d+)/g) || [];
  if (outs.length) u.output = +outs[outs.length - 1].match(/\d+/)[0];
  return u;
}
function notifyGaveup(model) {
  const key = model + ts().slice(0, 16); // 분 단위 중복 억제
  if (key === _lastGaveupKey) return;
  _lastGaveupKey = key;
  tgSend(`❌ *Z.ai 529 완전실패*\n${model} — 폴백 체인 전부 과부하. 응답 없음.`);
}

function isOverloadStatus(status) {
  return status === 529 || status === 503 || status === 429;
}
function isOverloadModel(m) {
  if (!m) return false;
  return OVERLOAD_MODELS.some(o => m.includes(o));
}
function canStandardFallback(bodyBuf) {
  return bodyBuf.length <= STANDARD_FALLBACK_MAX_BYTES && FALLBACK_MODEL && FALLBACK_MODEL !== parseModel(bodyBuf);
}
function parseModel(bodyBuf) {
  try { return JSON.parse(bodyBuf.toString('utf8')).model || null; } catch { return null; }
}
function swapModel(bodyBuf, newModel) {
  try {
    const j = JSON.parse(bodyBuf.toString('utf8'));
    j.model = newModel;
    return Buffer.from(JSON.stringify(j), 'utf8');
  } catch { return bodyBuf; }
}

/**
 * upstream으로 1회 시도.
 * @returns {Promise<{status, headers, buffered:Buffer|null, res:object|null}>}
 *   - 정상(2xx): res 스트림을 클라이언트로 pipe하기 위해 res를 반환 (buffered=null)
 *   - 비정상: 본문을 버퍼링해 반환 (res=null)
 */
function sendOnce(targetPath, method, headers, bodyBuf) {
  return new Promise((resolve, reject) => {
    const reqOpts = {
      method,
      hostname: upstreamUrl.hostname,
      port: UPSTREAM_PORT,
      path: UPSTREAM_PATH_BASE + targetPath,
      headers: { ...headers, host: upstreamUrl.host },
    };
    const req = upstreamMod.request(reqOpts, (res) => {
      const status = res.statusCode;
      if (status >= 200 && status < 300) {
        resolve({ status, headers: res.headers, buffered: null, res });
        return;
      }
      // 비-2xx: 본문 버퍼링
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => resolve({ status, headers: res.headers, buffered: Buffer.concat(chunks), res: null }));
      res.on('error', reject);
    });
    req.on('error', reject);
    if (bodyBuf && bodyBuf.length) req.write(bodyBuf);
    req.end();
  });
}

function pipeUpstreamToClient(clientRes, upstreamRes, status, headers, onDone) {
  const h = { ...headers };
  delete h['content-length'];
  clientRes.writeHead(status, h);
  let buf = '';
  upstreamRes.on('data', (c) => { clientRes.write(c); if (onDone) buf += c.toString('utf8'); });
  upstreamRes.on('end', () => { clientRes.end(); if (onDone) onDone(buf); });
  upstreamRes.on('error', () => { try { clientRes.end(); } catch {} });
}

function writeBuffered(clientRes, status, headers, body) {
  const h = { ...headers };
  delete h['content-length'];
  delete h['transfer-encoding'];
  h['content-length'] = body.length;
  clientRes.writeHead(status, h);
  clientRes.end(body);
}

const server = http.createServer(async (clientReq, clientRes) => {
  // 요청 본문 버퍼링(POST 본문은 보통 작~중간; Claude Code는 청크 업로드 안 씀)
  const chunks = [];
  for await (const c of clientReq) chunks.push(c);
  let bodyBuf = Buffer.concat(chunks);

  // relay 헤더 (host/connection/content-length 제외 — 직접 관리)
  const fwdHeaders = {};
  for (const [k, v] of Object.entries(clientReq.headers)) {
    const lk = k.toLowerCase();
    if (lk === 'host' || lk === 'connection' || lk === 'content-length') continue;
    fwdHeaders[k] = v;
  }

  const startedModel = parseModel(bodyBuf);
  let attempt = 0;
  let lastNon2xx = null;

  while (attempt < MAX_ATTEMPTS) {
    attempt++;
    fwdHeaders['content-length'] = bodyBuf.length;

    let resp;
    try {
      resp = await sendOnce(clientReq.url, clientReq.method, fwdHeaders, bodyBuf);
    } catch (e) {
      log(`NET-ERROR attempt=${attempt} model=${parseModel(bodyBuf)} ${e.message}`);
      lastNon2xx = { status: 599, headers: {'content-type':'application/json'},
        buffered: Buffer.from(JSON.stringify({type:'error',error:{type:'proxy_upstream_error',message:e.message}})) };
      await sleep(backoffMs(attempt));
      continue;
    }

    // 정상 응답 → pipe 후 종료
    if (resp.res) {
      if (attempt > 1) {
        const reqBytes = bodyBuf.length;
        const fm = startedModel || '?';
        const tm = parseModel(bodyBuf) || FALLBACK_MODEL;
        log(`RECOVERED model=${tm} attempts=${attempt} startModel=${fm} status=${resp.status} reqBytes=${reqBytes}`);
        pipeUpstreamToClient(clientRes, resp.res, resp.status, resp.headers, (buf) => {
          notifyRecovered(fm, tm, extractUsage(buf), reqBytes);
        });
      } else {
        pipeUpstreamToClient(clientRes, resp.res, resp.status, resp.headers);
      }
      return;
    }

    // 비-2xx
    const curModel = parseModel(bodyBuf);
    if (isOverloadStatus(resp.status)) {
      log(`OVERLOAD status=${resp.status} attempt=${attempt} model=${curModel} body=${resp.buffered.toString('utf8').slice(0,160)}`);
      // 1M 변형이면 요청 크기에 따라 분기:
      // - 짧은 요청: 표준 모델 백업으로 가용성 확보
      // - 긴 요청: 1M을 보장해야 하므로 같은 모델로 재시도하고, 안 되면 명시 실패
      if (isOverloadModel(curModel)) {
        if (canStandardFallback(bodyBuf)) {
          log(`FALLBACK-SHORT ${curModel} -> ${FALLBACK_MODEL} reqBytes=${bodyBuf.length} max=${STANDARD_FALLBACK_MAX_BYTES}`);
          bodyBuf = swapModel(bodyBuf, FALLBACK_MODEL);
        } else {
          log(`RETRY-1M curModel=${curModel} reqBytes=${bodyBuf.length} maxShortFallback=${STANDARD_FALLBACK_MAX_BYTES}`);
        }
      }
      lastNon2xx = resp;
      await sleep(backoffMs(attempt));
      continue;
    }

    // 그 외 에러(400 모델오류, 401 등) → 폴백으로 해결될 수 없으니 그대로 반환
    writeBuffered(clientRes, resp.status, resp.headers, resp.buffered);
    return;
  }

  // 재시도 한도 초과 → 마지막 응답 반환 (가능하면 폴백 모델 상태)
  log(`GAVE-UP attempts=${attempt} model=${parseModel(bodyBuf)} status=${lastNon2xx ? lastNon2xx.status : '?'}`);
  notifyGaveup(parseModel(bodyBuf) || '?');
  if (lastNon2xx) {
    writeBuffered(clientRes, lastNon2xx.status, lastNon2xx.headers, lastNon2xx.buffered);
  } else {
    writeBuffered(clientRes, 502, {'content-type':'application/json'},
      Buffer.from(JSON.stringify({type:'error',error:{type:'proxy_exhausted',message:'zai-fallback-proxy: all attempts failed'}})));
  }
});

server.listen(PORT, '127.0.0.1', () => {
  log(`STARTED listening=127.0.0.1:${PORT} upstream=${UPSTREAM} fallback=${FALLBACK_MODEL} overloadModels=[${OVERLOAD_MODELS.join(',')}] shortFallbackMaxBytes=${STANDARD_FALLBACK_MAX_BYTES} maxAttempts=${MAX_ATTEMPTS}`);
});
server.on('error', (e) => { log(`FATAL ${e.message}`); process.exit(1); });

// 종료 시그널 처리
for (const sig of ['SIGTERM', 'SIGINT']) {
  process.on(sig, () => { log(`STOP ${sig}`); server.close(() => process.exit(0)); });
}
