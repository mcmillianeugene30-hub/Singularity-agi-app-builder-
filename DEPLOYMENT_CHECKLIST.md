# 📋 Production Deployment Checklist

This checklist will help you deploy the Singularity AGI App Builder to production using Render (backend) and Netlify (frontend).

## Pre-Deployment Checklist

### Code Preparation
- [ ] All code is committed to GitHub
- [ ] `render.yaml` exists and is configured correctly
- [ ] `requirements.txt` includes all dependencies
- [ ] `api.py` has `/health` endpoint
- [ ] CORS is configured in `api.py`
- [ ] `netlify.toml` is updated for dashboard-only build
- [ ] `dashboard/.env.local.example` exists
- [ ] `dashboard/package.json` has correct dependencies
- [ ] `dashboard/next.config.js` has `output: 'export'`

### Environment Variables
- [ ] OpenRouter API key obtained
- [ ] Groq API key obtained
- [ ] Gemini API key obtained
- [ ] GitHub Personal Access Token created (with `repo` scope)
- [ ] Netlify Personal Access Token created (with `deploy` scope)
- [ ] All keys are ready to add to Render

### Account Setup
- [ ] Render account created
- [ ] Netlify account created
- [ ] Both accounts are verified
- [ ] GitHub repository is accessible by both platforms

---

## Backend Deployment (Render)

### Step 1: Connect Repository
- [ ] Login to Render dashboard
- [ ] Click "New" → "Web Service"
- [ ] Connect your GitHub repository
- [ ] Authorize Render to access your repository

### Step 2: Configure Service
- [ ] Name: `singularity-agi-backend`
- [ ] Region selected (closest to you)
- [ ] Branch: `main`
- [ ] Runtime: `Python 3`
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables
- [ ] `OPENROUTER_API_KEY` added
- [ ] `GROQ_API_KEY` added
- [ ] `GEMINI_API_KEY` added
- [ ] `GITHUB_TOKEN` added
- [ ] `NETLIFY_TOKEN` added
- [ ] All variables are marked as "Not sync"

### Step 4: Deploy
- [ ] Click "Deploy Web Service"
- [ ] Monitor build logs
- [ ] Wait for successful deployment
- [ ] Note the service URL (e.g., `https://singularity-agi-backend.onrender.com`)

### Step 5: Verify Backend
- [ ] Test health endpoint: `curl https://your-backend-url.onrender.com/health`
- [ ] Check service is "Live" in Render dashboard
- [ ] Review logs for any errors
- [ ] Test WebSocket connection (optional, using wscat)

---

## Frontend Deployment (Netlify)

### Step 1: Prepare Configuration
- [ ] Copy `dashboard/.env.local.example` to `dashboard/.env.local`
- [ ] Update `NEXT_PUBLIC_API_URL` with Render backend URL
- [ ] Commit `.env.local.example` (not `.env.local`)
- [ ] Push to GitHub

### Step 2: Connect Repository
- [ ] Login to Netlify dashboard
- [ ] Click "Add new site" → "Import an existing project"
- [ ] Connect your GitHub repository
- [ ] Authorize Netlify to access your repository

### Step 3: Configure Build Settings
- [ ] Build command: `cd dashboard && npm install && npm run build`
- [ ] Publish directory: `dashboard/out`
- [ ] Branch: `main`
- [ ] Node version: 18

### Step 4: Add Environment Variables
- [ ] Click "Site Settings" → "Environment Variables"
- [ ] Add `NEXT_PUBLIC_API_URL`
- [ ] Set value to your Render backend URL
- [ ] Click "Save"

### Step 5: Deploy
- [ ] Click "Deploy site"
- [ ] Monitor build logs
- [ ] Wait for successful deployment
- [ ] Note the site URL (e.g., `https://singularity-agi-dashboard.netlify.app`)

### Step 6: Verify Frontend
- [ ] Open the Netlify URL
- [ ] Verify dashboard loads correctly
- [ ] Check browser console for errors
- [ ] Verify "System Online" indicator is green

---

## Integration Testing

### Test Backend-Frontend Connection
- [ ] Open dashboard in browser
- [ ] Enter a simple test prompt (e.g., "Build a todo app")
- [ ] Click "Launch App"
- [ ] Watch logs for WebSocket connection
- [ ] Verify backend URL in logs is correct

### Test Build Process
- [ ] Check for "WebSocket connected" message
- [ ] Check for "Planning your app" message
- [ ] Check for "Project blueprint generated" message
- [ ] Check for "Multi-agent build complete" message
- [ ] Check for "Project healed and verified" message (if heal enabled)
- [ ] Check for "App built successfully" message

### Test Deployment (Optional)
- [ ] If deployment tokens are valid
- [ ] Check for "Deploying to GitHub and Netlify" message
- [ ] Verify GitHub repo was created
- [ ] Verify Netlify site was created

---

## Post-Deployment Checklist

### Monitoring Setup
- [ ] Bookmark Render dashboard for backend monitoring
- [ ] Bookmark Netlify dashboard for frontend monitoring
- [ ] Set up email alerts for service failures (Render)
- [ ] Enable Netlify Analytics (optional)

### Documentation
- [ ] Save backend URL for reference
- [ ] Save frontend URL for reference
- [ ] Document environment variables used
- [ ] Create user documentation (if applicable)

### Security Review
- [ ] Verify CORS is restricted to your Netlify domain (production)
- [ ] Confirm no sensitive data in client-side code
- [ ] Verify all API keys are stored in Render, not committed
- [ ] Check that `.env` files are in `.gitignore`

### Performance Check
- [ ] Test dashboard load time
- [ ] Test WebSocket connection latency
- [ ] Test with concurrent build requests
- [ ] Monitor resource usage in Render

---

## Troubleshooting Checklist

### If Backend Deployment Fails
- [ ] Check `requirements.txt` exists and is complete
- [ ] Verify Python version compatibility
- [ ] Review build logs for specific errors
- [ ] Check environment variables are all set
- [ ] Verify start command is correct

### If Frontend Deployment Fails
- [ ] Check Node version (should be 18+)
- [ ] Verify `next.config.js` has `output: 'export'`
- [ ] Review build logs for specific errors
- [ ] Check all dependencies are in `package.json`
- [ ] Verify `NEXT_PUBLIC_API_URL` is set

### If WebSocket Connection Fails
- [ ] Verify backend URL is correct
- [ ] Check if backend is running (not sleeping)
- [ ] Verify CORS allows your Netlify domain
- [ ] Test WebSocket manually with wscat
- [ ] Check browser console for errors

### If Build Process Fails
- [ ] Check all AI API keys are valid
- [ ] Verify API keys are not expired
- [ ] Check for rate limit errors
- [ ] Review backend logs for specific errors
- [ ] Test each API provider individually

### If Deployment (to GitHub/Netlify) Fails
- [ ] Verify GitHub token has `repo` scope
- [ ] Verify Netlify token has `deploy` scope
- [ ] Check tokens are not expired
- [ ] Verify token permissions
- [ ] Check for quota limits

---

## Maintenance Checklist

### Weekly
- [ ] Check Render service logs for errors
- [ ] Check Netlify build logs for errors
- [ ] Monitor AI provider usage and limits
- [ ] Review build success rates

### Monthly
- [ ] Review and rotate API keys if needed
- [ ] Update dependencies (both Python and Node)
- [ ] Review and optimize build times
- [ ] Check for security vulnerabilities

### Quarterly
- [ ] Review scaling needs
- [ ] Evaluate upgrade options
- [ ] Update documentation
- [ ] Backup critical configuration

---

## URLs to Save

```
Backend (Render):
- Service Dashboard: https://dashboard.render.com/services/[service-id]
- API URL: https://singularity-agi-backend.onrender.com
- Health Check: https://singularity-agi-backend.onrender.com/health
- WebSocket: wss://singularity-agi-backend.onrender.com/ws/build
- API Docs: https://singularity-agi-backend.onrender.com/docs

Frontend (Netlify):
- Site Dashboard: https://app.netlify.com/sites/[site-id]
- Site URL: https://singularity-agi-dashboard.netlify.app
```

---

## Quick Commands

### Test Backend Health
```bash
curl https://singularity-agi-backend.onrender.com/health
```

### Test WebSocket (requires wscat)
```bash
npm install -g wscat
wscat -c https://singularity-agi-backend.onrender.com/ws/build
```

### Locally Test Frontend with Production Backend
```bash
cd dashboard
echo "NEXT_PUBLIC_API_URL=https://singularity-agi-backend.onrender.com" > .env.local
npm run dev
```

### Build Frontend Locally
```bash
cd dashboard
npm run build
```

---

## Support Resources

- **Render Documentation**: https://docs.render.com
- **Netlify Documentation**: https://docs.netlify.com
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **Next.js Documentation**: https://nextjs.org/docs

---

## Notes

```
[Deployment Date]: _______________
[Backend URL]: ___________________
[Frontend URL]: __________________
[Render Service ID]: ____________
[Netlify Site ID]: ______________
[Issues Encountered]: __________
```

---

**Deployment Complete! 🎉**

Remember: The Render free tier service will sleep after 15 minutes of inactivity. First build may take 30-60 seconds to wake up the service.
