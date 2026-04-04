# 🚀 Quick Start Guide - Netlify Deployment

This guide helps you deploy the Singularity AGI Dashboard to Netlify in under 5 minutes.

## Prerequisites

- GitHub account
- Netlify account (free tier works)
- Node.js 18+ installed locally

## Step 1: Prepare Your Repository

1. **Fork or clone** this repository to your GitHub
2. **Verify the dashboard structure**:
   ```bash
   ls -la dashboard/
   # Should show: app/, package.json, next.config.js, tsconfig.json, etc.
   ```

## Step 2: Deploy to Netlify

### Option A: Manual Deploy (Fastest)

1. **Build locally**:
   ```bash
   cd dashboard
   npm install
   npm run build
   ```

2. **Upload to Netlify**:
   - Go to [app.netlify.com](https://app.netlify.com)
   - Click "Add new site" → "Deploy manually"
   - Drag and drop the `dashboard/out` folder
   - Your site will be live in seconds!

### Option B: Git Deploy (Recommended for Updates)

1. **Connect GitHub to Netlify**:
   - In Netlify dashboard: "Add new site" → "Import an existing project"
   - Select your GitHub repository
   - Configure build settings:
     - **Branch**: `main` (or your branch name)
     - **Build command**: `cd dashboard && npm install && npm run build`
     - **Publish directory**: `dashboard/out`

2. **Add environment variable** (optional, for connecting to backend):
   - Site settings → Environment variables → Add variable
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: Your backend URL (e.g., `https://your-api.railway.app`)

3. **Deploy**:
   - Click "Deploy site"
   - Netlify will build and deploy automatically

## Step 3: Access Your Dashboard

Once deployed, you'll get a URL like:
- `https://yoursite.netlify.app`

Open it in your browser! You should see the Singularity AGI Dashboard.

## Step 4: Connect to Backend (Optional)

The dashboard needs a running backend to function fully. Here's how to set it up:

### Quick Test Mode (No Backend)

The dashboard will load and show the UI, but building apps won't work without the backend.

### Connect to Running Backend

1. **Deploy backend to Railway** (Free):
   ```bash
   # Follow the full DEPLOYMENT.md guide
   railway init
   railway up
   ```

2. **Update Netlify environment**:
   - Go to Netlify site settings → Environment variables
   - Add: `NEXT_PUBLIC_API_URL=https://your-backend.railway.app`

3. **Redeploy**:
   - Netlify will automatically redeploy with the new variable

## Troubleshooting

### Build Fails

**Error**: "Command failed with exit code 1"

**Solution**:
```bash
# Check Node version (must be 18+)
node --version

# Try building locally first
cd dashboard
npm install
npm run build

# Check for errors
```

### Blank Page After Deploy

**Error**: Page loads but shows blank screen

**Solution**:
1. Check browser console (F12) for errors
2. Verify `next.config.js` has `output: 'export'`
3. Ensure `tsconfig.json` exists in dashboard folder

### Can't Connect to Backend

**Error**: "WebSocket error occurred"

**Solution**:
1. Verify backend is running
2. Check `NEXT_PUBLIC_API_URL` is set correctly
3. Test backend API: `curl https://your-backend-url.com/docs`

## Custom Domain (Optional)

1. In Netlify: Domain settings → Add custom domain
2. Buy or use existing domain
3. Update DNS records as instructed
4. Your custom domain will be live!

## Next Steps

- Deploy the backend following [DEPLOYMENT.md](DEPLOYMENT.md)
- Test building a sample app
- Customize the dashboard design
- Add authentication/security

## Support

- Netlify docs: [docs.netlify.com](https://docs.netlify.com)
- Full deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- GitHub issues: Report issues in the repository
