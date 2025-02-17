const config = {
  apiBaseUrl: process.env.NODE_ENV === 'production'
    ? 'https://federal-ai-dashboard-api.onrender.com/api'
    : 'http://localhost:5001/api'
};

export default config;
