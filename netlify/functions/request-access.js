const { getEnv } = require('./_lib/env');
const { makeToken } = require('./_lib/access-token');

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

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
  if (!EMAIL_RE.test(email)) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Please enter a valid email address' }) };
  }

  const secret = getEnv('ACCESS_TOKEN_SECRET');
  const siteUrl = getEnv('SITE_URL') || 'https://dimosk.netlify.app';
  const resendKey = getEnv('RESEND_API_KEY');
  const fromEmail = getEnv('RESEND_FROM_EMAIL');

  const token = makeToken(email, secret);
  const link = `${siteUrl}/.netlify/functions/verify-access?token=${encodeURIComponent(token)}`;

  const emailRes = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${resendKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: fromEmail,
      to: email,
      subject: 'Your access link — Dimokritos Kallionakis Portfolio',
      html: `<p>Hi,</p><p>Thanks for your interest. Click the link below to view full contact details and download the CV:</p><p><a href="${link}">${link}</a></p><p>This link expires in 24 hours.</p>`,
    }),
  });

  if (!emailRes.ok) {
    console.error('Resend error:', await emailRes.text());
    return { statusCode: 502, body: JSON.stringify({ error: 'Could not send the email right now, please try again later' }) };
  }

  return { statusCode: 200, body: JSON.stringify({ ok: true }) };
};
