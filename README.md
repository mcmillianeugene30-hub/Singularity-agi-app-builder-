# 🌌 Singularity AGI: Full-Stack AI App Builder (2026 Edition)

Welcome to the **Singularity AGI Operator Manual**. This toolkit allows you to generate, build, and deploy full-stack Next.js/Supabase applications using only free API tiers from **OpenRouter**, **Groq**, and **Google Gemini**.

---

## 🚀 1. Prerequisites

Ensure you have the following installed locally:
- **Python 3.10+**
- **Git**
- **Node.js 20+** (for running the generated Next.js apps)

### Get Your Free API Keys:
1.  **OpenRouter**: [openrouter.ai](https://openrouter.ai/) (Create an account and get a free key).
2.  **Groq Cloud**: [console.groq.com](https://console.groq.com/) (Generate a free API key).
3.  **Google AI Studio**: [aistudio.google.com](https://aistudio.google.com/) (Generate a Gemini 3.1 Pro/Flash key).
4.  **GitHub Token**: [github.com/settings/tokens](https://github.com/settings/tokens) (Needs `repo` scope).
5.  **Netlify Token**: [app.netlify.com/user/settings/applications](https://app.netlify.com/user/settings/applications) (Personal access token).

---

## 🛠️ 2. Setup & Installation

1.  **Clone this repository** (or copy the files provided).
2.  **Install dependencies**:
    ```bash
    pip install requests argparse python-dotenv
    ```
3.  **Configure Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    OPENROUTER_API_KEY=your_key_here
    GROQ_API_KEY=your_key_here
    GEMINI_API_KEY=your_key_here
    GITHUB_TOKEN=your_github_token
    NETLIFY_TOKEN=your_netlify_token
    ```

---

## 🏗️ 3. Usage: Building Your App

Run the `main.py` script with your app description.

### Example: Generate Only (Local Build)
```bash
python main.py --prompt "A task management app for remote teams with real-time chat and Supabase auth."
```

### Example: Build & Auto-Deploy
```bash
python main.py --prompt "A coffee shop landing page with an online ordering system and admin dashboard." --deploy
```

---

## 🖥️ 5. Dashboard (Web UI)

We have provided a modern, high-performance dashboard built with **Next.js**, **Tailwind CSS**, and **FastAPI**. This allows you to visualize the build process and manage your AI provider status.

### Running the Backend API:
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Configure environment variables (see `.env.example`):
    ```bash
    cp .env.example .env
    # Edit .env with your API keys
    ```
3.  Start the API server:
    ```bash
    uvicorn api:app --reload
    ```
    The API will be available at `http://localhost:8000`.

### Running the Frontend Dashboard:
1.  Navigate to the `dashboard/` directory.
2.  Install Node dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    Open `http://localhost:3000` to access your Singularity AGI Dashboard.

## 🌐 Production Deployment

The Singularity AGI App Builder is now ready for production deployment!

### Quick Start - Deploy Frontend to Netlify:

1. **Build the dashboard**:
   ```bash
   cd dashboard
   npm install
   npm run build
   ```

2. **Deploy to Netlify**:
   - Go to [app.netlify.com](https://app.netlify.com)
   - Click "Add new site" → "Deploy manually"
   - Upload the `/dashboard/out` folder OR connect your GitHub repository
   - Configure build settings (see `netlify.toml`)

3. **Deploy Backend** (Required for full functionality):
   - Deploy to [Railway](https://railway.app) or [Render](https://render.com)
   - See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide

### Deployment Options:

1. **Frontend Only (Quick)**: Deploy dashboard to Netlify
2. **Full Deployment**: Deploy backend to Railway + frontend to Netlify (Recommended)
3. **Serverless**: Convert to serverless functions (Advanced)

For detailed deployment instructions, troubleshooting, and configuration, see **[DEPLOYMENT.md](DEPLOYMENT.md)**.

---

## 🧠 6. How It Works (The Singularity Pipeline)

1.  **Smart Rotation (`smart_router.py`)**: Rotates between providers to bypass free-tier rate limits.
2.  **Architect Phase (`architect.py`)**: Decomposes your prompt into a full project plan (JSON).
3.  **Coder Phase (`coder.py`)**: Generates source code for every file in the plan.
4.  **Deployer Phase (`deployer.py`)**: Creates a GitHub repo, pushes the code, and triggers a Netlify site build.

---

## ⚠️ 5. Best Practices & Limitations

- **Rate Limits**: The "Smart Router" will automatically try the next provider if one hits a limit (429 error).
- **Prompt Clarity**: Be specific. Instead of "build a store", use "build a Next.js e-commerce site with Tailwind CSS and Supabase database for a clothing brand."
- **Manual Tweaks**: AI-generated code may occasionally need minor adjustments. Always check the `output/` folder before final deployment.

---

## 📜 License
Singularity AGI is open-source and intended for educational and rapid prototyping purposes.
