const { getEnv } = require('./_lib/env');
const { verifyToken } = require('./_lib/access-token');

exports.handler = async (event) => {
  const token = event.queryStringParameters && event.queryStringParameters.token;
  const secret = getEnv('ACCESS_TOKEN_SECRET');

  const claim = verifyToken(token, secret);
  if (!claim) {
    return {
      statusCode: 302,
      headers: { Location: '/?access=expired' },
      body: '',
    };
  }

  return {
    statusCode: 302,
    headers: {
      Location: '/protected/full-cv.html',
      'Set-Cookie': `access_token=${token}; Path=/; Max-Age=86400; HttpOnly; Secure; SameSite=Lax`,
    },
    body: '',
  };
};
