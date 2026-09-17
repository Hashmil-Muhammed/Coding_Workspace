export default function handler(request, response) {
  if (request.method !== 'POST') {
    return response.status(405).json({ error: 'Method Not Allowed' });
  }

  const { email, password } = request.body;
  const validEmail = process.env.ADMIN_EMAIL;
  const validPassword = process.env.ADMIN_PASSWORD;

  if (email === validEmail && password === validPassword) {
    // Basic success response.
    // The frontend will save a flag in sessionStorage to remain logged in.
    return response.status(200).json({ success: true });
  } else {
    return response.status(401).json({ success: false, error: 'Invalid credentials' });
  }
}
