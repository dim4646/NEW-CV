// Step 1: a visitor asks for access. Nothing is sent to the visitor yet —
// the owner gets a Telegram message (TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID) and/or an email
// (OWNER_EMAIL) with Approve / Reject buttons.
const { getEnv } = require('./_lib/env');
const { makeApprovalToken, escapeHtml } = require('./_lib/approval-token');

const EMAIL_RE = /^[^\s@<>"']+@[^\s@<>"']+\.[^\s@<>"']+$/;

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ error: 'Method not allowed' }) };
  }

  let email;
  try {
    ({ email } = JSON.parse(event.body || '{}'));
  } catch {
    return { statusCode: 400, body: JSON.stringify({ error: 'Invalid request body' }) };
  }

  email = (email || '').trim().toLowerCase();
  if (!EMAIL_RE.test(email) || email.length > 254) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Please enter a valid email address' }) };
  }

  const secret = getEnv('ACCESS_TOKEN_SECRET');
  const siteUrl = getEnv('SITE_URL') || 'https://dimosk.netlify.app';
  const resendKey = getEnv('RESEND_API_KEY');
  const fromEmail = getEnv('RESEND_FROM_EMAIL');
  const ownerEmail = getEnv('OWNER_EMAIL');

  const tgToken = getEnv('TELEGRAM_BOT_TOKEN');
  const tgChat = getEnv('TELEGRAM_CHAT_ID');

  if (!ownerEmail && !(tgToken && tgChat)) {
    console.error('No owner notification channel set (OWNER_EMAIL or TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID)');
    return { statusCode: 500, body: JSON.stringify({ error: 'Access requests are temporarily unavailable' }) };
  }

  const token = makeApprovalToken(email, secret);
  const decideUrl = `${siteUrl}/.netlify/functions/approve-access?token=${encodeURIComponent(token)}`;
  const safeEmail = escapeHtml(email);
  const when = new Date().toLocaleString('en-AU', { timeZone: 'Australia/Brisbane' });

  const html = `
    <div style="font-family:Arial,sans-serif;font-size:15px;color:#14213d">
      <p><strong>New CV access request</strong></p>
      <p><strong>${safeEmail}</strong> asked to see your full profile, contact details and CV.<br>
      <span style="color:#666">${escapeHtml(when)} (Brisbane time)</span></p>
      <p>
        <a href="${decideUrl}&action=approve" style="background:#1f8f4e;color:#fff;padding:10px 18px;border-radius:6px;text-decoration:none;font-weight:bold">✅ Approve</a>
        &nbsp;
        <a href="${decideUrl}&action=reject" style="background:#b23b3b;color:#fff;padding:10px 18px;border-radius:6px;text-decoration:none;font-weight:bold">❌ Reject</a>
      </p>
      <p style="color:#666;font-size:13px">Each button opens a confirmation page — nothing happens until you confirm there.
      If you do nothing, the person gets no access. These buttons expire in 7 days.</p>
    </div>`;

  let delivered = false;

  // Telegram: instant notification with Approve / Reject buttons
  if (tgToken && tgChat) {
    try {
      const tg = await fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: tgChat,
          text: `🔔 CV access request\n\n${email}\nwants to see your full profile, contact details and CV.\n${when} (Brisbane)`,
          reply_markup: {
            inline_keyboard: [[
              { text: '✅ Approve', url: `${decideUrl}&action=approve` },
              { text: '❌ Reject', url: `${decideUrl}&action=reject` },
            ]],
          },
        }),
      });
      if (tg.ok) delivered = true;
      else console.error('Telegram error:', await tg.text());
    } catch (err) {
      console.error('Telegram error:', err);
    }
  }

  // Email: backup notification
  if (ownerEmail) {
    const emailRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${resendKey}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: fromEmail,
        to: ownerEmail,
        reply_to: email,
        subject: `CV access request from ${email}`,
        html,
      }),
    });
    if (emailRes.ok) delivered = true;
    else console.error('Resend error:', await emailRes.text());
  }

  if (!delivered) {
    return { statusCode: 502, body: JSON.stringify({ error: 'Could not send your request right now, please try again later' }) };
  }

  return { statusCode: 200, body: JSON.stringify({ ok: true, pending: true }) };
};
