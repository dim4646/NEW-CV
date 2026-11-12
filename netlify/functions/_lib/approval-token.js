// Signed, expiring token that lets the site owner approve or reject one access request.
// Uses a key derived from ACCESS_TOKEN_SECRET so it can never be used as an access token.
const crypto = require('crypto');

const TTL_MS = 7 * 24 * 60 * 60 * 1000; // owner has 7 days to decide

function key(secret) {
  return crypto.createHmac('sha256', secret).update('approval-key-v1').digest();
}

function makeApprovalToken(email, secret) {
  const payload = JSON.stringify({ email, exp: Date.now() + TTL_MS });
  const sig = crypto.createHmac('sha256', key(secret)).update(payload).digest('hex');
  return Buffer.from(payload).toString('base64url') + '.' + sig;
}

function verifyApprovalToken(token, secret) {
  if (!token || typeof token !== 'string') return null;
  const [encPayload, sig] = token.split('.');
  if (!encPayload || !sig) return null;
  let payload;
  try {
    payload = Buffer.from(encPayload, 'base64url').toString('utf8');
  } catch {
    return null;
  }
  const expected = crypto.createHmac('sha256', key(secret)).update(payload).digest('hex');
  const a = Buffer.from(sig);
  const b = Buffer.from(expected);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  let data;
  try {
    data = JSON.parse(payload);
  } catch {
    return null;
  }
  if (!data.email || !data.exp || Date.now() > data.exp) return null;
  return data;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

module.exports = { makeApprovalToken, verifyApprovalToken, escapeHtml };
