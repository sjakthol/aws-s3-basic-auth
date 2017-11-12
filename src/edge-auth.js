'use strict'

const CORRECT_AUTH = 'Basic c2FtaTpwNHM1dzByZCE='

exports.handler = (event, context, callback) => {
  const request = event.Records[0].cf.request
  if (!request.headers.authorization || request.headers.authorization.length === 0) {
    // No header present. Send auth request.
    return callback(null, {
      status: '401',
      statusDescription: 'Unauthorized',
      headers: {
        'www-authenticate': [{
          key: 'WWW-Authenticate',
          value: 'Basic realm="Restricted Access"'
        }]
      }
    })
  }

  const auth = request.headers.authorization[0].value
  if (auth === CORRECT_AUTH) {
    // Authentication was correct. Continue with the request
    return callback(null, request)
  }

  // Wrong username / password; deny access
  return callback(null, {
    status: '403',
    statusDescription: 'Forbidden'
  })
}
