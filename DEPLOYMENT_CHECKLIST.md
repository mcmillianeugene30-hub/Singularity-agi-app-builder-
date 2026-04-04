# 📋 Production Deployment Checklist

Use this checklist to verify your Singularity AGI App Builder is ready for production deployment.

## ✅ Pre-Deployment Checklist

### Frontend (Dashboard)
- [x] Next.js 14 installed
- [x] TypeScript configured
- [x] Tailwind CSS configured
- [x] Static export enabled in next.config.js
- [x] Build tested successfully (`npm run build`)
- [x] `out/` directory generated
- [x] package.json with all dependencies
- [x] tsconfig.json for type checking
- [x] Environment variable support (`NEXT_PUBLIC_API_URL`)
- [x] Responsive design verified
- [x] WebSocket connection handling

### Backend (FastAPI)
- [x] FastAPI installed
- [x] WebSocket endpoint configured
- [x] CORS enabled
- [x] Environment variables documented (.env.example)
- [x] requirements.txt with all dependencies
- [x] Procfile for deployment
- [x] Dockerfile for containerization
- [x] docker-compose.yml for local dev
- [x] Health check configured

### Deployment Configuration
- [x] netlify.toml configured
- [x] Build command set: `cd dashboard && npm install && npm run build`
- [x] Publish directory: `dashboard/out`
- [x] Security headers configured
- [x] Redirects for SPA behavior
- [x] Node version specified (18)

### Documentation
- [x] README.md updated with deployment section
- [x] DEPLOYMENT.md - Comprehensive guide
- [x] QUICKSTART.md - 5-minute quick start
- [x] NETLIFY_READY.md - Status overview
- [x] Environment variable templates (.env.example)

### Git & Version Control
- [x] .gitignore configured
  - Python: __pycache__, .venv, *.pyc, .env
  - Node: node_modules, .next, out, .env
- [x] Dashboard .gitignore configured
- [x] All new configuration files created
- [x] No secrets committed

## 🚀 Deployment Steps

### Step 1: Deploy Frontend to Netlify

**Option A: Manual Upload**
```bash
cd dashboard
npm run build
# Upload /dashboard/out folder to Netlify
```

**Option B: Git Integration**
1. Push code to GitHub
2. Connect repository to Netlify
3. Configure build settings
4. Deploy

### Step 2: Deploy Backend to Railway/Render

**Option A: Railway**
```bash
railway init
railway up
# Add environment variables in dashboard
```

**Option B: Render**
1. Create new Web Service
2. Connect GitHub repository
3. Configure build and start commands
4. Add environment variables

### Step 3: Connect Frontend to Backend

1. Get backend URL from Railway/Render
2. Add `NEXT_PUBLIC_API_URL` to Netlify environment variables
3. Redeploy frontend
4. Test WebSocket connection
5. Build a sample app to verify full pipeline

## 🔍 Post-Deployment Verification

### Frontend Checks
- [ ] Dashboard loads at Netlify URL
- [ ] UI displays correctly on desktop
- [ ] UI displays correctly on mobile (responsive)
- [ ] No console errors in browser
- [ ] All icons and assets load
- [ ] Tailwind styles applied correctly

### Backend Checks
- [ ] API responds at `/docs` (FastAPI docs)
- [ ] WebSocket endpoint accessible at `/ws/build`
- [ ] Health check passes
- [ ] CORS headers properly set
- [ ] Environment variables loaded

### Integration Checks
- [ ] Frontend can connect to backend via WebSocket
- [ ] Build requests sent successfully
- [ ] Real-time logs display correctly
- [ ] Provider status updates work
- [ ] Error handling functions properly

### End-to-End Checks
- [ ] Submit a simple build prompt
- [ ] WebSocket connection established
- [ ] Build process initiates
- [ ] Logs display in real-time
- [ ] Build completes successfully
- [ ] Output generated (if backend has required keys)

## 🔐 Security Checklist

### Environment Variables
- [ ] .env files NOT committed to git
- [ ] .env.example provided for reference
- [ ] API keys stored in platform secrets
- [ ] NEXT_PUBLIC_API_URL uses HTTPS
- [ ] No hardcoded credentials

### Headers & CORS
- [ ] Security headers configured
- [ ] CORS properly restricted (currently * for dev)
- [ ] HTTPS enforced in production
- [ ] WebSocket uses WSS (WebSocket Secure)

### API Keys
- [ ] GitHub token has minimum required scopes (repo)
- [ ] Netlify token has deployment permissions
- [ ] AI provider keys have proper quotas
- [ ] Keys rotated if compromised

## 📊 Monitoring & Maintenance

### Set Up Monitoring
- [ ] Backend logs accessible (Railway/Render dashboard)
- [ ] Netlify build logs configured
- [ ] Error tracking (optional: Sentry, etc.)
- [ ] Performance monitoring (optional)

### Regular Tasks
- [ ] Monitor API provider rate limits
- [ ] Review backend logs weekly
- [ ] Check Netlify build status
- [ ] Update dependencies monthly
- [ ] Rotate API keys quarterly

## 🆘 Troubleshooting Guide

### Common Issues

**Build fails on Netlify**
→ Check Node version (must be 18+)
→ Verify `next.config.js` has `output: 'export'`
→ Check build logs for specific errors

**WebSocket connection fails**
→ Verify backend is running
→ Check `NEXT_PUBLIC_API_URL` is correct
→ Test backend API directly
→ Check CORS settings

**App generation fails**
→ Verify all API keys are set
→ Check API provider quotas
→ Review Smart Router logs
→ Test API keys individually

**Blank page on frontend**
→ Check browser console for errors
→ Verify static files were generated
→ Check Netlify build logs
→ Ensure proper file permissions

## 📞 Support Resources

- **Documentation**: README.md, DEPLOYMENT.md, QUICKSTART.md
- **Status**: NETLIFY_READY.md
- **Checklist**: This file
- **Issues**: Report in GitHub repository

## ✨ Success Metrics

Your deployment is successful when:
1. ✅ Dashboard loads on Netlify URL
2. ✅ Backend API responds to health checks
3. ✅ WebSocket connection established
4. ✅ Sample build command initiated
5. ✅ Real-time logs display
6. ✅ Build process completes
7. ✅ No critical errors in logs

---

**Last Updated**: April 4, 2026
**Status**: ✅ Ready for Production Deployment
