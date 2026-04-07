# 🚀 Quick Start Guide - Production Deployment

This guide will help you deploy Singularity AGI to production in under 5 minutes.

## Option 1: Deploy to Render (Recommended - Free Tier)

### Step 1: Prepare Your Environment

1. **Get your API keys** (5 minutes):
   - [OpenRouter](https://openrouter.ai/) - Free key
   - [Groq](https://console.groq.com/) - Free key
   - [Gemini](https://aistudio.google.com/) - Free key
   - [GitHub Token](https://github.com/settings/tokens) - Repo scope

2. **Push code to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Production ready backend"
   git push origin main
   ```

### Step 2: Deploy to Render

1. **Create Render account**: [render.com](https://render.com)
2. **New Web Service**:
   - Connect your GitHub repository
   - Select `render.yaml` as the build configuration
3. **Set Environment Variables**:
   ```
   PORT=8000
   ENVIRONMENT=production
   ALLOWED_ORIGINS=https://your-frontend.vercel.app

   # Required AI Keys
   OPENROUTER_API_KEY=your_key
   GROQ_API_KEY=your_key
   GEMINI_API_KEY=your_key

   # Deployment Tokens
   GITHUB_TOKEN=your_token
   NETLIFY_TOKEN=your_token
   VERCEL_TOKEN=your_token
   RAILWAY_TOKEN=your_token

   # Database (optional)
   SUPABASE_URL=your_url
   SUPABASE_SERVICE_KEY=your_key
   ```

4. **Click Deploy** - Your API will be live in ~3 minutes!

### Step 3: Verify Deployment

```bash
# Check health endpoint
curl https://your-app.onrender.com/health

# View API docs
# Open: https://your-app.onrender.com/docs
```

---

## Option 2: Deploy with Docker

### Step 1: Build the Image

```bash
# Clone repository
git clone https://github.com/your-username/singularity-agi.git
cd singularity-agi

# Create .env file
cp .env.example .env
# Edit .env with your API keys

# Build Docker image
docker build -t singularity-agi .
```

### Step 2: Run the Container

```bash
docker run -d \
  --name singularity-api \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  singularity-agi
```

### Step 3: Verify

```bash
# Check health
curl http://localhost:8000/health

# View logs
docker logs -f singularity-api
```

---

## Option 3: Deploy to Heroku

### Step 1: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Deploy

```bash
# Login
heroku login

# Create app
heroku create singularity-agi-backend

# Set environment variables
heroku config:set PORT=8000
heroku config:set ENVIRONMENT=production
heroku config:set ALLOWED_ORIGINS=https://your-frontend.vercel.app
heroku config:set OPENROUTER_API_KEY=your_key
heroku config:set GROQ_API_KEY=your_key
heroku config:set GEMINI_API_KEY=your_key
# ... set all other variables

# Deploy
git push heroku main
```

---

## Post-Deployment Checklist

- [ ] Health check returns 200 OK
- [ ] API docs are accessible at `/docs`
- [ ] WebSocket endpoint is working
- [ ] Environment variables are loaded correctly
- [ ] Database connections work (if configured)
- [ ] Build process completes successfully
- [ ] Logs are being generated

---

## Common Issues

### Issue: Build fails with "Missing API keys"
**Solution**: Make sure all required environment variables are set in your deployment platform.

### Issue: CORS errors
**Solution**: Set `ALLOWED_ORIGINS` to your exact frontend domain (not `*` in production).

### Issue: Container crashes on startup
**Solution**: Check logs for missing dependencies or incorrect Python version.

### Issue: Rate limiting
**Solution**: Add multiple API keys (e.g., `OPENROUTER_API_KEY_1`, `OPENROUTER_API_KEY_2`).

---

## Next Steps

1. **Deploy the frontend dashboard** to Vercel
2. **Configure monitoring** (Sentry, LogRocket, etc.)
3. **Set up alerts** for failures
4. **Configure a custom domain**
5. **Set up CI/CD pipeline**

---

## Support

- **Full Documentation**: [README.md](README.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Production Checklist**: [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)
- **Health Check**: Run `python health_check.py`

---

**Deployment Time**: ~5-10 minutes
**Cost**: Free tier available on all platforms
**Support**: All platforms have free tiers suitable for development and testing

Happy deploying! 🚀
