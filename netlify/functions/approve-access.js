// Step 2: the owner clicks Approve / Reject in the notification email.
// GET  -> confirmation page (so email link scanners can't approve by just opening the link)
// POST -> performs the action; on approve the visitor receives their 24-hour access link.
const { getEnv } = require('./_lib/env');
const { makeToken } = require('./_lib/access-token');
const { verifyApprovalToken, escapeHtml } = require('./_lib/approval-token');

function page(title, body, status = 200) {
  return {
    statusCode: status,
    headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex' },
    body: `<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${title}</title>
<style>body{font-family:Arial,sans-serif;background:#0f1c33;color:#fff;display:flex;min-height:100vh;align-items:center;justify-content:center;margin:0}
.card{background:#16284a;border:1px solid rgba(201,168,76,.35);border-radius:12px;padding:2rem;max-width:440px;width:90%;text-align:center}
h1{font-size:1.3rem;color:#e3c36a;margin-top:0}button{font-size:1rem;font-weight:bold;border:0;border-radius:8px;padding:.8rem 1.6rem;cursor:pointer;color:#fff}
.ok{background:#1f8f4e}.no{background:#b23b3b}p{line-height:1.5}</style></head>
<body><div class="card"><h1>${title}</h1>${body}</div></body></html>`,
  };
}

exports.handler = async (event) => {
  const secret = getEnv('ACCESS_TOKEN_SECRET');
  const isPost = event.httpMethod === 'POST';

  let token, action;
  if (isPost) {
    const form = new URLSearchParams(event.isBase64Encoded ? Buffer.from(event.body || '', 'base64').toString() : event.body || '');
    token = form.get('token');
    action = form.get('action');
  } else {
    const q = event.queryStringParameters || {};
    token = q.token;
    action = q.action;
  }

  if (action !== 'approve' && action !== 'reject') return page('Invalid link', '<p>This link is not valid.</p>', 400);
  const claim = verifyApprovalToken(token, secret);
  if (!claim) return page('Link expired', '<p>This request link is invalid or has expired (7 days).</p>', 400);

  const safeEmail = escapeHtml(claim.email);

  if (!isPost) {
    const label = action === 'approve' ? 'Approve' : 'Reject';
    const cls = action === 'approve' ? 'ok' : 'no';
    const text = action === 'approve'
      ? `<p><strong>${safeEmail}</strong> will receive a private link (valid 24 hours) to your full profile, contact details and CV.</p>`
      : `<p><strong>${safeEmail}</strong> will not receive access. Nothing is sent to them.</p>`;
    return page(`${label} access request?`,
      `${text}<form method="POST"><input type="hidden" name="token" value="${escapeHtml(token)}">
       <input type="hidden" name="action" value="${action}"><button class="${cls}" type="submit">${label}</button></form>`);
  }

  if (action === 'reject') {
    return page('Request rejected', `<p>No access was given to <strong>${safeEmail}</strong>.</p>`);
  }

  const siteUrl = getEnv('SITE_URL') || 'https://dimosk.netlify.app';
  const accessToken = makeToken(claim.email, secret);
  const link = `${siteUrl}/.netlify/functions/verify-access?token=${encodeURIComponent(accessToken)}`;

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${getEnv('RESEND_API_KEY')}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: getEnv('RESEND_FROM_EMAIL'),
      to: claim.email,
      subject: 'Your access link — Dimokritos Kallionakis Portfolio',
      html: `<p>Hi,</p><p>Thank you for your interest. Your request has been approved. Click the link below to view my full contact details and download my CV:</p><p><a href="${link}">${link}</a></p><p>This link expires in 24 hours.</p><p>Kind regards,<br>Dimokritos Kallionakis</p>`,
    }),
  });

  if (!res.ok) {
    console.error('Resend error:', await res.text());
    return page('Email failed', `<p>Approved, but the email to <strong>${safeEmail}</strong> could not be sent. Please try the button again later.</p>`, 502);
  }

  return page('Access approved ✅', `<p>A private access link (valid 24 hours) was sent to <strong>${safeEmail}</strong>.</p>`);
};
