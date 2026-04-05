# 🔧 Environment Setup Guide

This guide helps you configure the Singularity AGI App Builder for production deployment on Render (backend) and Netlify (frontend).

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting Your Render URL](#getting-your-render-url)
3. [Setting Environment Variables on Render](#setting-environment-variables-on-render)
4. [Setting NEXT_PUBLIC_API_URL on Netlify](#setting-next_public_api_url-on-netlify)
5. [Testing the Connection](#testing-the-connection)
6. [Common Issues and Solutions](#common-issues-and-solutions)

---

## Prerequisites

Before you begin, ensure you have:

- ✅ GitHub account with repository access
- ✅ Render account ([render.com](https://render.com))
- ✅ Netlify account ([netlify.com](https://netlify.com))
- ✅ All required API keys (OpenRouter, Groq, Gemini, GitHub, Netlify)

---

## Getting Your Render URL

After deploying your backend to Render:

1. **Navigate to your Render Dashboard**
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Find your `singularity-agi-backend` service

2. **Copy the Render URL**
   - Your URL will be in the format: `https://your-service-name.onrender.com`
   - Click the URL to open it in a new tab
   - You should see the API information JSON response

3. **Test the Root Endpoint**
   ```bash
   curl https://your-render-url.onrender.com/
   ```
   Expected response:
   ```json
   {
     "message": "Singularity AGI API",
     "version": "1.0.0",
     "endpoints": {
       "health": "/health",
       "websocket": "/ws/build",
       "docs": "/docs"
     }
   }
   ```

4. **Test the Health Endpoint**
   ```bash
   curl https://your-render-url.onrender.com/health
   ```
   Expected response:
   ```json
   {
     "status": "healthy",
     "service": "singularity-agi-backend"
   }
   ```

---

## Setting Environment Variables on Render

1. **Open Your Render Service**
   - Go to your service dashboard
   - Click on the service name

2. **Navigate to Environment Variables**
   - Scroll down to the "Environment" section
   - Click "Add Environment Variable"

3. **Add the Required Variables**

   | Variable Name | Description | How to Get |
   |---------------|-------------|------------|
   | `OPENROUTER_API_KEY` | OpenRouter API key | [openrouter.ai/keys](https://openrouter.ai/keys) |
   | `GROQ_API_KEY` | Groq API key | [console.groq.com](https://console.groq.com) |
   | `GEMINI_API_KEY` | Google Gemini API key | [aistudio.google.com](https://aistudio.google.com) |
   | `GITHUB_TOKEN` | GitHub Personal Access Token | Create at [github.com/settings/tokens](https://github.com/settings/tokens) with `repo` scope |
   | `NETLIFY_TOKEN` | Netlify Personal Access Token | Create at [app.netlify.com/user/settings/applications](https://app.netlify.com/user/settings/applications) |

4. **Save Changes**
   - After adding all variables, click "Save Changes"
   - **Important**: This will trigger a new deployment of your backend

5. **Verify Environment Variables**
   - After the deployment completes, test the health endpoint again
   - If it returns healthy, your environment variables are set correctly

---

## Setting NEXT_PUBLIC_API_URL on Netlify

This is the critical step that connects your frontend dashboard to your Render backend.

1. **Open Your Netlify Site Dashboard**
   - Go to [app.netlify.com](https://app.netlify.com)
   - Select your deployed dashboard site

2. **Navigate to Site Configuration**
   - Click "Site configuration" in the left sidebar
   - Scroll down to "Environment variables"

3. **Add the NEXT_PUBLIC_API_URL Variable**
   - Click "Add a variable"
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://your-render-url.onrender.com` (your Render backend URL)
   - Click "Save"

4. **Redeploy the Site**
   - Netlify will prompt you to redeploy
   - Click "Trigger deploy" → "Deploy site"
   - Wait for the deployment to complete

5. **Verify the Connection**
   - Open your Netlify dashboard URL
   - Click the "Test Connection" button in the header
   - You should see a green "Connected" status

---

## Testing the Connection

### Using the Dashboard

1. Open your Netlify-deployed dashboard
2. Click the "Test Connection" button in the top-right header
3. Check the logs section for connection status:
   - `[✓] Backend connected successfully` - Everything works!
   - `[✗] Connection failed` - Check your API URL and backend status

### Using cURL (Command Line)

```bash
# Test root endpoint
curl https://your-render-url.onrender.com/

# Test health endpoint
curl https://your-render-url.onrender.com/health

# Test with verbose output for debugging
curl -v https://your-render-url.onrender.com/health
```

### Using a Browser

Simply navigate to your Render URL in a browser:
- `https://your-render-url.onrender.com/` - Shows API info
- `https://your-render-url.onrender.com/health` - Shows health status
- `https://your-render-url.onrender.com/docs` - Shows API documentation (if enabled)

---

## Common Issues and Solutions

### Issue 1: "Not Found" Error on Render

**Symptoms**: When you visit your Render URL, you see a 404 Not Found page

**Causes**:
- Backend hasn't finished deploying
- Incorrect port configuration
- Missing startup command

**Solutions**:
1. Check Render logs for deployment errors
2. Ensure your `Procfile` contains: `web: uvicorn api:app --host 0.0.0.0 --port $PORT`
3. Make sure `api.py` is in the root directory
4. Wait 2-5 minutes for deployment to complete

### Issue 2: Connection Timeout from Dashboard

**Symptoms**: Dashboard shows "Disconnected" when testing connection

**Causes**:
- Wrong API URL in Netlify environment variables
- Backend is down or still deploying
- CORS issues

**Solutions**:
1. Verify `NEXT_PUBLIC_API_URL` matches your Render URL exactly
2. Check if Render backend is running (visit the URL directly)
3. Ensure there's no trailing slash in the URL
4. Check Render service logs for errors

### Issue 3: WebSocket Connection Failed

**Symptoms**: Dashboard connects to health endpoint but WebSocket fails when building

**Causes**:
- Render free tier WebSocket limits
- Incorrect WebSocket URL format

**Solutions**:
1. Ensure WebSocket URL format is: `wss://your-render-url.onrender.com/ws/build`
2. Note: Render free tier supports WebSockets but may have connection limits
3. If issues persist, consider upgrading to Render Starter plan ($7/mo)

### Issue 4: Environment Variables Not Working

**Symptoms**: Backend returns errors about missing API keys

**Causes**:
- Environment variables not saved
- Deployment not triggered after adding variables
- Variable names have typos

**Solutions**:
1. Double-check variable names match exactly (case-sensitive)
2. Ensure you clicked "Save Changes" after adding variables
3. Trigger a manual deployment if needed
4. Check Render logs to see which variables are loaded

### Issue 5: CORS Errors in Browser Console

**Symptoms**: Browser shows CORS errors when dashboard tries to connect

**Causes**:
- CORS middleware not configured correctly
- Wrong origin headers

**Solutions**:
1. The `api.py` file should have CORS configured with `allow_origins=["*"]`
2. If using a specific domain, add it to `allow_origins`
3. Clear browser cache and reload

### Issue 6: Dashboard Shows Old Connection Status

**Symptoms**: Connection status doesn't update after changing API URL

**Causes**:
- Netlify environment variables not deployed
- Browser cache

**Solutions**:
1. Redeploy Netlify site after changing environment variables
2. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
3. Open in an incognito/private window to test

---

## Quick Troubleshooting Checklist

- [ ] Backend URL is accessible in browser
- [ ] `/health` endpoint returns `{"status":"healthy"}`
- [ ] All environment variables are set on Render
- [ ] `NEXT_PUBLIC_API_URL` is set correctly on Netlify
- [ ] Netlify site has been redeployed after setting variables
- [ ] Browser console shows no CORS errors
- [ ] Render service logs show no errors
- [ ] You're using HTTPS URLs (not HTTP) in production

---

## Next Steps

Once everything is connected:

1. ✅ Test a simple build through the dashboard
2. ✅ Check build logs for successful execution
3. ✅ Verify generated apps appear in the output folder
4. ✅ Test the deployment feature (if tokens are configured)

For deployment-specific issues, see [DEPLOYMENT.md](DEPLOYMENT.md).

---

## Need Help?

If you're still experiencing issues:

1. Check the [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment steps
2. Review Render logs: Go to your service → Logs tab
3. Review Netlify logs: Go to your site → Deploys → Click a deployment → Functions logs
4. Test locally first: Ensure everything works with `uvicorn api:app --reload` before deploying
