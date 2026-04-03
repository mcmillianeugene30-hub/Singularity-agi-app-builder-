# Singularity AGI Deployment Automation (Free Tier)

This guide explains how to automate full-stack deployments using GitHub Actions and Netlify's free tier.

### 1. Project Structure (Next.js)
Your generated app should follow this structure:
```text
/my-ai-app
  /app (Next.js App Router)
  /components (UI components)
  /lib (Supabase/Neon clients)
  /public (Static assets)
  package.json
  netlify.toml
  next.config.js
```

### 2. Netlify Configuration (`netlify.toml`)
This file tells Netlify how to build and where to find the output.
```toml
[build]
  command = "npm run build"
  publish = ".next"

[[plugins]]
  package = "@netlify/plugin-nextjs"
```

### 3. GitHub Action for Deployment (`.github/workflows/deploy.yml`)
Automate the build and deploy process on every push.
```yaml
name: Deploy Singularity App

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install Dependencies
        run: npm install
        
      - name: Build App
        run: npm run build
        env:
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
          
      - name: Deploy to Netlify
        uses: ntl/action-netlify-deploy@v2
        with:
          publish-dir: .next
          production-deploy: true
          github-token: ${{ secrets.GITHUB_TOKEN }}
          netlify-site-id: ${{ secrets.NETLIFY_SITE_ID }}
          netlify-auth-token: ${{ secrets.NETLIFY_AUTH_TOKEN }}
```

### 4. Free Backend Strategy
- **Database**: Use [Supabase](https://supabase.com) (Free tier: 500MB DB, Auth, Storage).
- **Edge Functions**: Netlify Functions (Free tier: 125k requests/month).
- **Environment Variables**: Store your API keys (OpenRouter, Groq, Gemini) in Netlify's dashboard and GitHub Secrets.

### 5. Smart Routing during Build
If your app needs AI generation *during* the build process (e.g., generating static content), include the `smart_router.py` logic in a pre-build script (`node prebuild.js` or `python prebuild.py`).
