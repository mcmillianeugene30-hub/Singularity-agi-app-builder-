# Singularity AGI - Production Deployment Guide

This guide will help you deploy the Singularity AGI backend to production using various platforms.

## Prerequisites

Before deploying, ensure you have:
- All AI API keys (OpenRouter, Groq, Gemini)
- Deployment platform tokens (GitHub, Netlify, Vercel, Railway, Render)
- Supabase project URL and service key
- Neon API key (optional, for database branching)

## Quick Deployment Options

### 1. Render.com (Recommended)

Render is the recommended platform for the backend API.

#### Steps:
1. **Create a Render account**: [render.com](https://render.com)
2. **Create a new Web Service**
   - Connect your GitHub repository
   - Select the `render.yaml` configuration (or use manual settings)
   - Set environment variables (see below)
3. **Configure Environment Variables**:
   ```
   PORT=8000
   WORKERS=1
   ENVIRONMENT=production
   PYTHONUNBUFFERED=1
   ALLOWED_ORIGINS=https://your-frontend-domain.com

   # AI Keys
   OPENROUTER_API_KEY=your_key
   GROQ_API_KEY=your_key
   GEMINI_API_KEY=your_key

   # Deployment Tokens
   GITHUB_TOKEN=your_token
   NETLIFY_TOKEN=your_token
   VERCEL_TOKEN=your_token
   RAILWAY_TOKEN=your_token
   RENDER_API_KEY=your_token

   # Database
   SUPABASE_URL=your_url
   SUPABASE_SERVICE_KEY=your_key
   NEON_API_KEY=your_key
   ```
4. **Deploy** - Render will automatically build and deploy your service
5. **Get your URL** - Your backend will be available at `https://your-app-name.onrender.com`

#### Environment-Specific URLs:
- Production: Update `ALLOWED_ORIGINS` with your frontend URL
- Development: Set `ALLOWED_ORIGINS=*` for testing

### 2. Docker Deployment

Deploy using Docker on any cloud provider (AWS, GCP, Azure, DigitalOcean, etc.).

#### Build the Docker Image:
```bash
docker build -t singularity-agi-backend .
```

#### Run Locally:
```bash
docker run -d \
  --name singularity-api \
  -p 8000:8000 \
  --env-file .env \
  singularity-agi-backend
```

#### Push to Docker Hub:
```bash
docker tag singularity-agi-backend your-dockerhub-username/singularity-agi-backend
docker push your-dockerhub-username/singularity-agi-backend
```

#### Docker Compose (Recommended):
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - ENVIRONMENT=production
      - PYTHONUNBUFFERED=1
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 3. Heroku Deployment

1. **Install Heroku CLI**:
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku

   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and Create App**:
   ```bash
   heroku login
   heroku create singularity-agi-backend
   ```

3. **Set Environment Variables**:
   ```bash
   heroku config:set PORT=8000
   heroku config:set WORKERS=1
   heroku config:set ENVIRONMENT=production
   heroku config:set ALLOWED_ORIGINS=https://your-frontend-domain.com

   # Set your API keys
   heroku config:set OPENROUTER_API_KEY=your_key
   heroku config:set GROQ_API_KEY=your_key
   heroku config:set GEMINI_API_KEY=your_key
   heroku config:set GITHUB_TOKEN=your_token
   heroku config:set NETLIFY_TOKEN=your_token
   # ... (set all other variables)
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

### 4. Railway Deployment

1. **Create Railway account**: [railway.app](https://railway.app)
2. **New Project** → **Deploy from GitHub repo**
3. **Set environment variables** in the Railway dashboard
4. **Railway will automatically deploy**

## Environment Variables Reference

### Required Variables:
- `OPENROUTER_API_KEY` - OpenRouter API key
- `GROQ_API_KEY` - Groq API key
- `GEMINI_API_KEY` - Google Gemini API key
- `GITHUB_TOKEN` - GitHub personal access token

### Optional Variables (with defaults):
- `PORT` - Server port (default: 8000)
- `WORKERS` - Number of workers (default: 1)
- `ENVIRONMENT` - Environment (production/development, default: production)
- `ALLOWED_ORIGINS` - CORS allowed origins (default: *)
- `LOG_LEVEL` - Logging level (default: INFO)

### Deployment Tokens:
- `NETLIFY_TOKEN` - Netlify API token
- `VERCEL_TOKEN` - Vercel API token
- `RAILWAY_TOKEN` - Railway API token
- `RENDER_API_KEY` - Render API key

### Database:
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_SERVICE_KEY` - Supabase service role key
- `NEON_API_KEY` - Neon database API key

## Monitoring and Logs

### Render Dashboard:
- View logs in the Render dashboard
- Monitor CPU, memory, and response time
- Set up alerts for failures

### Health Checks:
```bash
# Check health endpoint
curl https://your-app-name.onrender.com/health

# Get API info
curl https://your-app-name.onrender.com/

# View Swagger docs
# Open: https://your-app-name.onrender.com/docs
```

## Scaling Considerations

### Free Tier Limitations:
- Render Free: 512MB RAM, 0.1 CPU, sleeps after 15min inactivity
- Railway Free: 512MB RAM, restarts daily
- Heroku Eco: 512MB RAM, sleeps after 30min inactivity

### Production Recommendations:
- **Workers**: Increase `WORKERS` based on CPU cores (1-4)
- **Memory**: Minimum 1GB RAM for production
- **Database**: Use managed PostgreSQL (Supabase, Neon)
- **CDN**: Use Cloudflare or similar for API caching
- **Monitoring**: Set up Sentry for error tracking

### Multi-Key Rotation:
For high-traffic deployments, add multiple API keys to avoid rate limits:
```
OPENROUTER_API_KEY=key1
OPENROUTER_API_KEY_1=key2
OPENROUTER_API_KEY_2=key3
```

## Troubleshooting

### Build Failures:
- Ensure `requirements.txt` is up to date
- Check Python version compatibility (3.10+)
- Verify all dependencies install successfully

### Runtime Errors:
- Check logs for missing environment variables
- Verify API keys are valid and active
- Ensure database connections work

### CORS Issues:
- Set `ALLOWED_ORIGINS` to your exact frontend domain
- For development, use `ALLOWED_ORIGINS=*`
- Verify the frontend is calling the correct API URL

### Performance Issues:
- Increase `WORKERS` for concurrent requests
- Use a larger instance size
- Implement caching for expensive operations
- Monitor AI API rate limits

## Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use service role keys** (not anon keys) for backend
3. **Restrict CORS origins** in production
4. **Rotate API keys regularly**
5. **Monitor for unauthorized access**
6. **Use HTTPS only**
7. **Implement rate limiting** (add `slowapi` or similar)
8. **Keep dependencies updated**

## Frontend Deployment

After deploying the backend, deploy the Next.js dashboard:

### Vercel (Recommended for Frontend):
1. Connect your GitHub repository
2. Set root directory to `dashboard`
3. Add environment variable:
   - `NEXT_PUBLIC_API_URL=https://your-backend-api.onrender.com`
4. Deploy!

### Netlify:
1. Connect your GitHub repository
2. Set base directory to `dashboard`
3. Build command: `npm run build`
4. Publish directory: `.next`
5. Add environment variables as needed

## Support and Documentation

- API Documentation: `https://your-api-url/docs` (Swagger UI)
- Architecture: See `singularity_agi_architecture.html`
- README: See `README.md`

## Next Steps

1. Deploy backend to Render
2. Deploy frontend to Vercel
3. Configure environment variables
4. Test the WebSocket connection
5. Monitor build logs and deployments
6. Set up alerts for failures
7. Scale based on traffic

Happy deploying! 🚀
