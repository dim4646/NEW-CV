function getCookie(request, name) {
  const header = request.headers.get('cookie') || '';
  const match = header.split(';').map(c => c.trim()).find(c => c.startsWith(`${name}=`));
  return match ? decodeURIComponent(match.slice(name.length + 1)) : null;
}

function base64urlDecode(str) {
  str = str.replace(/-/g, '+').replace(/_/g, '/');
  while (str.length % 4) str += '=';
  return atob(str);
}

async function hmacHex(payload, secret) {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']
  );
  const sigBuf = await crypto.subtle.sign('HMAC', key, enc.encode(payload));
  return Array.from(new Uint8Array(sigBuf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function verifyToken(token, secret) {
  if (!token) return null;
  const [encPayload, sig] = token.split('.');
  if (!encPayload || !sig) return null;

  let payload;
  try {
    payload = base64urlDecode(encPayload);
  } catch {
    return null;
  }

  const expectedSig = await hmacHex(payload, secret);
  if (sig !== expectedSig) return null;

  const [email, expStr] = payload.split(':');
  const exp = Number(expStr);
  if (!email || !exp || Date.now() > exp) return null;
  return { email, exp };
}

export default async (request, context) => {
  const secret = Netlify.env.get('ACCESS_TOKEN_SECRET');
  const token = getCookie(request, 'access_token');
  const claim = await verifyToken(token, secret);

  if (!claim) {
    return Response.redirect(`${new URL(request.url).origin}/?access=required`, 302);
  }

  return context.next();
};

export const config = { path: '/protected/*' };
