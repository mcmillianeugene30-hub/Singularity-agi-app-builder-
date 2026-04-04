# 🚀 Quick Start: Render + Netlify Deployment

Fast-track guide to deploy Singularity AGI App Builder to production.

## 1. Backend: Deploy to Render (5 minutes)

### Prerequisites
- Render account: https://render.com
- GitHub repository with this code
- 5 AI API keys (OpenRouter, Groq, Gemini, GitHub, Netlify)

### Steps

1. **Go to Render Dashboard**
   ```
   https://dashboard.render.com
   ```

2. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repo
   - Configure:
     - Name: `singularity-agi-backend`
     - Runtime: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables**
   Go to "Advanced" → "Environment" and add:
   ```
   OPENROUTER_API_KEY=your_key_here
   GROQ_API_KEY=your_key_here
   GEMINI_API_KEY=your_key_here
   GITHUB_TOKEN=your_github_pat_here
   NETLIFY_TOKEN=your_netlify_token_here
   ```

4. **Deploy**
   - Click "Deploy Web Service"
   - Wait 2-5 minutes
   - Get your URL: `https://singularity-agi-backend.onrender.com`

5. **Test**
   ```bash
   curl https://singularity-agi-backend.onrender.com/health
   ```

---

## 2. Frontend: Deploy to Netlify (3 minutes)

### Steps

1. **Go to Netlify Dashboard**
   ```
   https://app.netlify.com
   ```

2. **Create New Site**
   - Click "Add new site" → "Import an existing project"
   - Connect your GitHub repo
   - Configure:
     - Build command: `cd dashboard && npm install && npm run build`
     - Publish directory: `dashboard/out`

3. **Add Environment Variable**
   - Go to "Site Settings" → "Environment Variables"
   - Add:
     ```
     NEXT_PUBLIC_API_URL=https://singularity-agi-backend.onrender.com
     ```

4. **Deploy**
   - Click "Deploy site"
   - Wait 1-2 minutes
   - Get your URL: `https://singularity-agi-dashboard.netlify.app`

5. **Test**
   - Open your Netlify URL
   - Dashboard should load
   - "System Online" indicator should be green

---

## 3. Test Integration (2 minutes)

### Test Build Process

1. Open your Netlify dashboard URL
2. Enter a prompt: "Build a simple todo app"
3. Click "Launch App"
4. Watch logs:
   - `[+] WebSocket connected`
   - `[*] Planning your app`
   - `[+] Multi-agent build complete`

### Expected URLs

```
Backend: https://singularity-agi-backend.onrender.com
Frontend: https://singularity-agi-dashboard.netlify.app
WebSocket: wss://singularity-agi-backend.onrender.com/ws/build
```

---

## Common Issues & Fixes

### Issue: "Backend is sleeping"
**Fix**: Wait 30-60 seconds for Render service to wake up

### Issue: "WebSocket connection failed"
**Fix**:
1. Verify `NEXT_PUBLIC_API_URL` is set correctly in Netlify
2. Check backend is running: Test `/health` endpoint
3. Verify CORS allows your Netlify domain

### Issue: "Build failed - API key error"
**Fix**:
1. Check all environment variables in Render
2. Verify API keys are valid and not expired
3. Regenerate tokens if needed

---

## Cost Summary

### Free Tier
- **Backend**: $0/month (Render free)
- **Frontend**: $0/month (Netlify free)
- **AI Providers**: $0-50/month (depending on usage)

### Production Tier
- **Backend**: $7/month (Render Starter - always-on)
- **Frontend**: $19/month (Netlify Pro)
- **AI Providers**: $50-200/month

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Netlify
3. ✅ Test build process
4. ✅ Set up monitoring
5. ✅ Share your deployed URLs

---

## Need Help?

- **Render Docs**: https://docs.render.com
- **Netlify Docs**: https://docs.netlify.com
- **Full Deployment Guide**: See `DEPLOYMENT.md`
- **Detailed Checklist**: See `DEPLOYMENT_CHECKLIST.md`

---

**Ready to build! 🚀**

Total time: ~10 minutes
