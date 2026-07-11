const crypto = require('crypto');

const TTL_MS = 24 * 60 * 60 * 1000;

function makeToken(email, secret) {
  const exp = Date.now() + TTL_MS;
  const payload = `${email}:${exp}`;
  const sig = crypto.createHmac('sha256', secret).update(payload).digest('hex');
  return Buffer.from(payload).toString('base64url') + '.' + sig;
}

function verifyToken(token, secret) {
  if (!token) return null;
  const [encPayload, sig] = token.split('.');
  if (!encPayload || !sig) return null;

  let payload;
  try {
    payload = Buffer.from(encPayload, 'base64url').toString('utf8');
  } catch {
    return null;
  }

  const expectedSig = crypto.createHmac('sha256', secret).update(payload).digest('hex');
  const sigBuf = Buffer.from(sig);
  const expBuf = Buffer.from(expectedSig);
  if (sigBuf.length !== expBuf.length || !crypto.timingSafeEqual(sigBuf, expBuf)) return null;

  const [email, expStr] = payload.split(':');
  const exp = Number(expStr);
  if (!email || !exp || Date.now() > exp) return null;
  return { email, exp };
}

module.exports = { makeToken, verifyToken };
