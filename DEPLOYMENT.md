# 🚀 Netlify Deployment Guide

## Overview
This guide explains how to deploy the Singularity AGI App Builder to Netlify.

## Architecture

### Frontend Dashboard (Next.js)
- **Technology**: Next.js 14 with TypeScript and Tailwind CSS
- **Deployment**: Static export (Netlify Pages)
- **Location**: `/dashboard` directory

### Backend API (FastAPI with WebSocket)
- **Technology**: Python FastAPI with Uvicorn
- **Note**: Cannot be deployed to Netlify (requires a server)
- **Recommended**: Deploy to Railway, Render, or Vercel (with serverless functions)

## Deployment Options

### Option 1: Deploy Frontend Only (Quick Start)

1. **Prepare the Dashboard**
   ```bash
   cd dashboard
   npm install
   npm run build
   ```

2. **Connect to Netlify**
   - Go to [app.netlify.com](https://app.netlify.com)
   - Click "Add new site" → "Deploy manually"
   - Upload the `/dashboard/out` folder or connect your GitHub repository

3. **Configure Netlify**
   - Build command: `cd dashboard && npm install && npm run build`
   - Publish directory: `dashboard/out`

4. **Important Notes**:
   - The dashboard will deploy but **won't work** without the backend
   - WebSocket connections require a running backend server
   - Use this option for UI testing only

### Option 2: Full Deployment (Recommended)

#### Step 1: Deploy Backend to Railway/Render

**Using Railway:**
1. Create a `Procfile` in project root:
   ```text
   web: uvicorn api:app --host 0.0.0.0 --port $PORT
   ```
2. Create a `requirements.txt`:
   ```text
   fastapi
   uvicorn
   requests
   python-dotenv
   pydantic
   ```
3. Push to GitHub and connect to Railway
4. Add environment variables in Railway dashboard:
     - `OPENROUTER_API_KEY`
     - `GROQ_API_KEY`
     - `GEMINI_API_KEY`
     - `GITHUB_TOKEN`
     - `NETLIFY_TOKEN`

**Using Render:**
1. Create a new Web Service
2. Connect your GitHub repository
3. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
   - Environment Variables: Same as above

#### Step 2: Deploy Frontend to Netlify

1. **Update Environment Variable**
   - In `dashboard/.env.production`:
     ```env
     NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
     ```
   - Replace with your actual backend URL

2. **Deploy to Netlify**
   - Connect your GitHub repository
   - Configure build settings (see `netlify.toml`)
   - Add environment variable: `NEXT_PUBLIC_API_URL`

3. **Test the Deployment**
   - Open your Netlify URL
   - Verify you can connect to the backend
   - Test a simple build command

### Option 3: Serverless Deployment (Advanced)

Convert the backend to serverless functions and deploy both on Vercel or use Netlify Functions.

## Environment Variables

### Required for Backend:
```env
OPENROUTER_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
GITHUB_TOKEN=your_github_token_here
NETLIFY_TOKEN=your_netlify_token_here
```

### Required for Frontend:
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

## Troubleshooting

### WebSocket Connection Issues

**Problem**: Dashboard shows "WebSocket error occurred"

**Solutions**:
1. Verify backend is running and accessible
2. Check CORS settings in `api.py`
3. Ensure `NEXT_PUBLIC_API_URL` is set correctly
4. Check firewall/security settings on backend server

### Build Errors

**Problem**: Next.js build fails on Netlify

**Solutions**:
1. Check Node version (should be 18+)
2. Verify `next.config.js` has `output: 'export'`
3. Ensure all dependencies are in `package.json`
4. Check build logs in Netlify dashboard

### API Key Issues

**Problem**: 401 or 403 errors when building apps

**Solutions**:
1. Verify all API keys are set in backend environment
2. Check API key validity and limits
3. Ensure tokens have proper scopes (GitHub: `repo`, Netlify: `deploy`)
4. Check Smart Router rotation logic in `smart_router.py`

## Monitoring

### Backend Monitoring
- Check Railway/Render logs for API errors
- Monitor rate limit usage across AI providers
- Watch for WebSocket connection issues

### Frontend Monitoring
- Use Netlify Analytics for traffic
- Check browser console for client-side errors
- Monitor build logs in Netlify dashboard

## Security Considerations

1. **Never commit `.env` files** - use `.env.example` as template
2. **Rotate API keys regularly** - especially if deploying to public repos
3. **Use environment-specific configs** - `.env.development`, `.env.production`
4. **Enable HTTPS** - required for WebSocket in production
5. **Implement rate limiting** - protect your AI provider quotas
6. **Secure WebSocket connections** - use WSS (WebSocket Secure)

## Cost Estimation

### Free Tier Limits (Current Setup):
- OpenRouter: Limited free credits
- Groq: Limited requests per day
- Gemini: Limited tokens per day
- Railway: $5 free credit per month
- Netlify: Free for static sites

### Potential Costs:
- Exceeding free tier limits on AI providers
- Backend hosting (if free tier exceeded)
- Custom domain names

## Next Steps

1. **Choose a deployment option** based on your needs
2. **Set up backend hosting** (Railway/Render recommended)
3. **Deploy frontend** to Netlify
4. **Configure environment variables** in both platforms
5. **Test end-to-end** by building a sample app
6. **Monitor logs and performance**

## Support

For issues or questions:
- Check logs in Railway/Render dashboard
- Review Netlify build logs
- Test backend API directly: `https://your-backend-url/docs`
- Verify WebSocket connection: Browser DevTools → Network → WS tab
