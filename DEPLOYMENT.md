# 🚀 Production Deployment Guide: Render + Netlify

This guide explains how to deploy the Singularity AGI App Builder in production using a split architecture:

- **Backend**: FastAPI WebSocket server on Render (supports WebSockets, free tier)
- **Frontend**: Next.js dashboard on Netlify (static hosting)

## Architecture Overview

```
┌─────────────────────────┐
│   Netlify (Frontend)    │
│   - Next.js Dashboard   │
│   - Static Files        │
│   - WebSocket Client    │
└──────────┬──────────────┘
           │
           │ WebSocket (wss://)
           │
┌──────────▼──────────────┐
│   Render (Backend)      │
│   - FastAPI Server      │
│   - WebSocket Handler   │
│   - AI Integration      │
│   - Build Pipeline      │
└─────────────────────────┘
```

## Prerequisites

- GitHub account with repository access
- Render account (free tier available at [render.com](https://render.com))
- Netlify account (free tier available at [netlify.com))
- AI API keys (OpenRouter, Groq, Gemini)
- GitHub Personal Access Token (with `repo` scope)
- Netlify Personal Access Token (with `deploy` scope)

---

## Part 1: Deploy Backend to Render

### Step 1: Prepare GitHub Repository

Ensure your code is pushed to GitHub with all the deployment files:

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### Step 2: Deploy to Render

1. **Sign up/login to [Render](https://dashboard.render.com)**

2. **Create a new Web Service**:
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure the Service**:
   - **Name**: `singularity-agi-backend`
   - **Region**: Choose nearest region
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables** (in the "Advanced" section):
   ```
   OPENROUTER_API_KEY=your_openrouter_key
   GROQ_API_KEY=your_groq_key
   GEMINI_API_KEY=your_gemini_key
   GITHUB_TOKEN=your_github_pat
   NETLIFY_TOKEN=your_netlify_token
   ```

5. **Click "Deploy Web Service"**

### Step 3: Verify Backend Deployment

1. Render will deploy your service (typically takes 2-5 minutes)
2. Once deployed, you'll get a URL like: `https://singularity-agi-backend.onrender.com`
3. Test the health endpoint:
   ```bash
   curl https://singularity-agi-backend.onrender.com/health
   ```
   Should return: `{"status":"healthy","service":"singularity-agi-backend"}`

### Step 4: Verify WebSocket Support

Render's free tier supports WebSockets. To test:

```bash
# Using wscat (install with: npm install -g wscat)
wscat -c https://singularity-agi-backend.onrender.com/ws/build
```

### Important Render Notes

- **Free Tier Limitations**:
  - Web services sleep after 15 minutes of inactivity
  - Cold starts take 30-60 seconds
  - 512MB RAM limit
  - 512 hours/month free

- **WebSocket Support**:
  - Render supports WebSocket connections on the free tier
  - No additional configuration needed
  - Automatically handles upgrade requests

- **Environment Variables**:
  - Never commit `.env` files
  - Always use Render's dashboard for sensitive data
  - Variables are encrypted at rest

---

## Part 2: Deploy Frontend to Netlify

### Step 1: Update Dashboard Configuration

1. **Create environment variable file** (local):
   ```bash
   cd dashboard
   cp .env.local.example .env.local
   ```

2. **Edit `.env.local`** with your Render backend URL:
   ```env
   NEXT_PUBLIC_API_URL=https://singularity-agi-backend.onrender.com
   ```

### Step 2: Deploy to Netlify

**Option A: Deploy via Netlify Dashboard**

1. Go to [app.netlify.com](https://app.netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect your GitHub repository
4. Configure build settings:
   - **Build command**: `cd dashboard && npm install && npm run build`
   - **Publish directory**: `dashboard/out`
   - **Branch**: `main`
5. Add environment variable:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://singularity-agi-backend.onrender.com`
6. Click "Deploy site"

**Option B: Deploy via Netlify CLI**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Initialize
netlify init

# Deploy
netlify deploy --prod
```

### Step 3: Verify Frontend Deployment

1. Netlify will deploy in 1-2 minutes
2. You'll get a URL like: `https://singularity-agi-dashboard.netlify.app`
3. Open the URL and verify:
   - Dashboard loads correctly
   - No console errors
   - "System Online" indicator shows green

### Step 4: Test Backend Connection

1. In the dashboard, enter a simple prompt like: "Build a todo app"
2. Click "Launch App"
3. Watch the logs for:
   - `[*] Connecting to: wss://singularity-agi-backend.onrender.com/ws/build`
   - `[+] WebSocket connected. Sending build request...`
   - Build progress messages

---

## Part 3: Connecting Frontend & Backend

### URL Formats

The frontend dashboard needs to connect to the Render backend using specific URL formats:

| Type | Format | Example |
|------|--------|---------|
| **HTTP API** | `https://your-render-url.onrender.com` | `https://singularity-agi-backend.onrender.com` |
| **WebSocket** | `wss://your-render-url.onrender.com/ws/build` | `wss://singularity-agi-backend.onrender.com/ws/build` |
| **Health Check** | `https://your-render-url.onrender.com/health` | `https://singularity-agi-backend.onrender.com/health` |
| **API Info** | `https://your-render-url.onrender.com/` | `https://singularity-agi-backend.onrender.com/` |

**Important Notes**:
- Always use `wss://` (secure WebSocket) in production, not `ws://`
- Always use `https://` (secure HTTP) in production, not `http://`
- The dashboard automatically converts HTTP to WS for WebSocket connections

### Connection Testing

The dashboard includes a built-in "Test Connection" button that:

1. Calls the `/health` endpoint on your Render backend
2. Displays connection status (Connected/Disconnected)
3. Shows the API URL being used
4. Logs detailed connection information

**To test the connection**:
1. Open your Netlify-deployed dashboard
2. Click "Test Connection" in the top-right header
3. Check the logs section for results

**Manual testing with cURL**:
```bash
# Test root endpoint (shows API info)
curl https://your-render-url.onrender.com/

# Test health endpoint
curl https://your-render-url.onrender.com/health

# With verbose output for debugging
curl -v https://your-render-url.onrender.com/health
```

### CORS Configuration

The backend (`api.py`) has CORS configured to allow connections from any origin:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, limit to your Netlify domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For production security**, restrict CORS to your specific Netlify domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-dashboard-name.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variable Requirements

**Backend (Render)**:
All required environment variables must be set in Render's environment configuration. See [Part 4: Environment Variables Setup](#part-4-environment-variables-setup) below for the complete list.

**Frontend (Netlify)**:
Only one environment variable is required for the frontend to connect to the backend:

| Variable | Required | Example Value |
|----------|----------|---------------|
| `NEXT_PUBLIC_API_URL` | ✅ Yes | `https://singularity-agi-backend.onrender.com` |

**Important**: The `NEXT_PUBLIC_` prefix is required for the variable to be available in the browser. Without this prefix, the dashboard cannot connect to the backend.

### Common Connection Issues

**Issue 1: "Not Found" on Render URL**
- **Cause**: Backend hasn't finished deploying or startup command is incorrect
- **Solution**: Check Render logs, verify `Procfile` contains: `web: uvicorn api:app --host 0.0.0.0 --port $PORT`

**Issue 2: Dashboard shows "Disconnected"**
- **Cause**: Wrong `NEXT_PUBLIC_API_URL` or backend is down
- **Solution**: Verify the URL matches your Render URL exactly, test backend directly in browser

**Issue 3: CORS errors in browser console**
- **Cause**: Backend blocking requests from Netlify domain
- **Solution**: Check CORS configuration in `api.py`, ensure `allow_origins` includes your Netlify domain

**Issue 4: WebSocket connection fails**
- **Cause**: Using `ws://` instead of `wss://` or backend is sleeping
- **Solution**: Ensure secure WebSocket URLs, check if backend is running (not in cold start)

**Issue 5: Environment variables not working**
- **Cause**: Variables not saved or deployment not triggered
- **Solution**: Redeploy after setting variables on Render and Netlify

### WebSocket URL Handling

The dashboard automatically converts HTTP to WS:

```typescript
const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const wsUrl = apiUrl.replace(/^http/, "ws") + "/ws/build";
```

This means:
- `http://localhost:8000` → `ws://localhost:8000/ws/build`
- `https://singularity-agi-backend.onrender.com` → `wss://singularity-agi-backend.onrender.com/ws/build`

---

## Part 4: Environment Variables Setup

### Backend (Render)

Set these in Render's "Environment" tab:

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `OPENROUTER_API_KEY` | OpenRouter API key | [openrouter.ai/keys](https://openrouter.ai/keys) |
| `GROQ_API_KEY` | Groq API key | [console.groq.com](https://console.groq.com) |
| `GEMINI_API_KEY` | Google Gemini API key | [makersuite.google.com](https://makersuite.google.com) |
| `GITHUB_TOKEN` | GitHub Personal Access Token | GitHub Settings → Developer Settings → Personal Access Tokens |
| `NETLIFY_TOKEN` | Netlify Personal Access Token | Netlify User Settings → Applications → Personal Access Tokens |

### Frontend (Netlify)

Set this in Netlify's "Site Settings" → "Environment Variables":

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://singularity-agi-backend.onrender.com` |

---

## Part 5: Troubleshooting

### Backend Issues (Render)

**Problem**: Service won't start

**Solutions**:
1. Check Render build logs
2. Verify `requirements.txt` exists and is complete
3. Ensure start command is: `uvicorn api:app --host 0.0.0.0 --port $PORT`
4. Verify all environment variables are set

**Problem**: Health check failing

**Solutions**:
1. Verify `/health` endpoint exists in `api.py`
2. Check if port binding is correct (`0.0.0.0` not `127.0.0.1`)
3. Review service logs for errors

**Problem**: WebSocket connections fail

**Solutions**:
1. Verify Render supports WebSocket (free tier does)
2. Check CORS settings allow your Netlify domain
3. Test WebSocket manually with `wscat`
4. Verify no firewall blocking

### Frontend Issues (Netlify)

**Problem**: Build fails

**Solutions**:
1. Check Node version (should be 18+)
2. Verify `next.config.js` has `output: 'export'`
3. Ensure all dependencies are in `package.json`
4. Review Netlify build logs

**Problem**: Can't connect to backend

**Solutions**:
1. Verify `NEXT_PUBLIC_API_URL` is set correctly in Netlify
2. Check browser console for errors
3. Test backend directly: `curl https://your-backend-url.onrender.com/health`
4. Verify CORS allows your Netlify domain

**Problem**: WebSocket errors in logs

**Solutions**:
1. Check the connection URL in logs
2. Verify backend is running (not sleeping)
3. Test WebSocket manually
4. Check if HTTPS/WSS is being used (required for production)

### Common Issues

**Problem**: "Backend is sleeping" errors

**Solutions**:
1. Render free tier services sleep after 15 minutes of inactivity
2. First request will take 30-60 seconds to wake up
3. Consider upgrading to paid tier for always-on service

**Problem**: Rate limits on AI providers

**Solutions**:
1. Monitor Smart Router rotation in logs
2. Check API key limits in each provider dashboard
3. Implement request queuing or upgrade to paid plans

**Problem**: Deployment tokens invalid

**Solutions**:
1. Regenerate tokens in provider dashboards
2. Ensure tokens have correct scopes:
   - GitHub: `repo` scope
   - Netlify: `deploy` scope
3. Update environment variables in Render

---

## Part 6: Monitoring and Maintenance

### Backend Monitoring (Render)

1. **Access Logs**:
   - Go to your service in Render dashboard
   - Click "Logs" tab
   - Filter by: "Server", "Build", or specific dates

2. **Health Checks**:
   - Render automatically checks `/health` endpoint
   - Configure custom health check in service settings
   - Get email alerts on service failures

3. **Metrics**:
   - Monitor CPU usage, memory, response times
   - Check WebSocket connection count
   - Track build success rates

### Frontend Monitoring (Netlify)

1. **Build Logs**:
   - Go to "Deploys" tab in Netlify dashboard
   - View detailed build output
   - Download logs for analysis

2. **Analytics**:
   - Enable Netlify Analytics for traffic insights
   - Monitor page views, unique visitors
   - Track build success rates

3. **Functions**:
   - Monitor edge function usage
   - Check execution times
   - Review error rates

---

## Part 7: Security Best Practices

### Backend Security

1. **Environment Variables**:
   - Never commit `.env` files
   - Use Render's encrypted storage
   - Rotate keys regularly

2. **CORS**:
   - Restrict to your Netlify domain
   - Disable `allow_origins=["*"]` in production

3. **Rate Limiting**:
   - Implement rate limiting on `/ws/build` endpoint
   - Consider using `slowapi` for FastAPI rate limiting

4. **Authentication**:
   - Add API key authentication for build requests
   - Implement JWT tokens for user sessions

### Frontend Security

1. **HTTPS**:
   - Netlify automatically provides HTTPS
   - Redirect all HTTP to HTTPS

2. **Headers**:
   - Already configured in `netlify.toml`
   - `X-Frame-Options: DENY`
   - `X-Content-Type-Options: nosniff`
   - `X-XSS-Protection: 1; mode=block`

3. **Environment Variables**:
   - Use `NEXT_PUBLIC_` prefix for client-side variables
   - Never expose sensitive data in client-side code

---

## Part 8: Cost Estimation

### Render (Backend)

| Plan | Cost | Features |
|------|------|----------|
| Free | $0/month | 512MB RAM, 0.1 CPU, 512 hours/month |
| Starter | $7/month | 512MB RAM, 0.5 CPU, Always-on |
| Standard | $25/month | 2GB RAM, 1 CPU, Always-on |

### Netlify (Frontend)

| Plan | Cost | Features |
|------|------|----------|
| Free | $0/month | 100GB bandwidth, 300 build minutes |
| Pro | $19/month | 400GB bandwidth, 1000 build minutes |
| Business | $99/month | 1000GB bandwidth, Unlimited builds |

### AI Provider Costs

| Provider | Free Tier | Paid Tier |
|----------|-----------|-----------|
| OpenRouter | Limited credits | $5/1M tokens |
| Groq | Limited requests/day | $0.59/1M tokens |
| Gemini | Limited tokens/day | Variable pricing |

### Total Estimated Cost

**Free Tier Setup**:
- Backend: $0 (Render free)
- Frontend: $0 (Netlify free)
- AI Providers: $0-50/month (depending on usage)

**Production Setup**:
- Backend: $7/month (Render Starter)
- Frontend: $19/month (Netlify Pro)
- AI Providers: $50-200/month (depending on usage)

---

## Part 9: Scaling Strategy

### When to Upgrade

**Signs you need to upgrade**:
- Frequent build failures due to timeouts
- Backend sleeping causing poor UX
- Exceeding free tier limits on AI providers
- High traffic requiring more resources

### Scaling Options

**Backend**:
- Upgrade to Render Starter ($7/month) for always-on service
- Add caching layer (Redis) for frequently used data
- Implement build queue to handle concurrent requests
- Consider horizontal scaling with load balancer

**Frontend**:
- Upgrade to Netlify Pro for more bandwidth
- Use Netlify Edge Functions for faster responses
- Implement CDN caching for static assets
- Add A/B testing and feature flags

**AI Providers**:
- Upgrade to paid tiers for higher rate limits
- Implement intelligent caching of AI responses
- Use cheaper models for simple tasks
- Add fallback providers for redundancy

---

## Part 10: Backup and Disaster Recovery

### Backup Strategy

**Code Backup**:
- GitHub repository stores all code
- Use GitHub branches for development
- Tag releases for production versions

**Data Backup**:
- Generated apps stored in GitHub via Deployer
- Netlify provides rollback to previous deployments
- Render provides logs for debugging

### Disaster Recovery

**If Backend Goes Down**:
1. Check Render service status
2. Review service logs
3. Redeploy if necessary
4. Use Git to restore from known good state

**If Frontend Goes Down**:
1. Check Netlify build logs
2. Redeploy from GitHub
3. Use Netlify rollback feature
4. Verify environment variables

**If AI Provider Fails**:
1. Smart Router automatically fails over
2. Monitor logs for provider switching
3. Update API keys if needed
4. Implement circuit breaker pattern

---

## Quick Reference

### Render Service URL
```
https://singularity-agi-backend.onrender.com
```

### Netlify Site URL
```
https://singularity-agi-dashboard.netlify.app
```

### Health Check Endpoint
```
https://singularity-agi-backend.onrender.com/health
```

### WebSocket Endpoint
```
wss://singularity-agi-backend.onrender.com/ws/build
```

### API Documentation
```
https://singularity-agi-backend.onrender.com/docs
```

---

## Next Steps

1. ✅ Complete backend deployment to Render
2. ✅ Complete frontend deployment to Netlify
3. ✅ Configure environment variables
4. ✅ Test end-to-end build process
5. ✅ Set up monitoring and alerts
6. ✅ Document your specific URLs and settings
7. ✅ Share with team/users

---

## Support and Resources

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Netlify Documentation**: [docs.netlify.com](https://docs.netlify.com)
- **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Next.js Documentation**: [nextjs.org/docs](https://nextjs.org/docs)
- **Project Issues**: Check GitHub issues for this repo

---

**Deployed and ready to build! 🚀**
