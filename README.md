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
    VERCEL_TOKEN=your_vercel_token
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
1.  Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Start the API server:
    ```bash
    python api.py
    ```
    The API will be available at `http://localhost:8000`.

### 🚀 7. Netlify Deployment Fix
If you encounter a `pydantic-core` or Rust/Cargo error during Netlify deployment, ensure the `netlify.toml` file is in your root directory. The build command should be:
```bash
python -m pip install --upgrade pip setuptools wheel && python -m pip install -r requirements.txt
```
This ensures the environment uses prebuilt binary wheels and skips the Rust compilation step.

### Running the Frontend Dashboard (Vercel):
1.  Navigate to the `dashboard/` directory.
2.  Install dependencies and start the dev server:
    ```bash
    npm install
    npm run dev
    ```
3.  **Deploy to Vercel**:
    - Connect your GitHub repository to [Vercel](https://vercel.com).
    - Set the **Root Directory** to `dashboard`.
    - Add the environment variable: `NEXT_PUBLIC_API_URL` (pointing to your Render backend).

---

## 🧠 8. Advanced AGI & Singularity Features (2026 Edition)

Your builder now includes cutting-edge features for high-fidelity app generation:

### **Autonomous Capabilities:**
- **Self-Refining Code**: Proactively optimizes code for performance and best practices.
- **Auto-Bug Detection**: Security scanning and syntax checking before deployment.
- **Continuous Learning**: Learns from successful past patterns in your database.

### **Advanced AI:**
- **Code Reasoning**: Explains *why* architectural decisions were made.
- **Multi-Modal Generation**: Generates UI mockups and Mermaid.js architecture diagrams.
- **Predictive Suggestions**: Suggests features you might have missed.

### **Ops & Safety:**
- **Auto-Rollback**: Automatically reverts to the last working version if a build or deploy fails.
- **Live Monitoring**: Real-time health, latency, and database stats.
- **Plugin System**: Extend the AGI with custom agents and community templates.

### **Multi-Key Rotation (New in 2026):**
To avoid free-tier rate limits, you can now add multiple keys for each provider. The AGI will automatically rotate to the next key if it hits a limit.
Add them to your `.env` or Render environment like this:
```env
# Gemini Keys
GEMINI_API_KEY=key_1
GEMINI_API_KEY_1=key_2
GEMINI_API_KEY_2=key_3

# Groq Keys
GROQ_API_KEY=key_1
GROQ_API_KEY_1=key_2

# OpenRouter Keys
OPENROUTER_API_KEY=key_1
OPENROUTER_API_KEY_1=key_2
```
The system will search for `PREFIX`, `PREFIX_1`, `PREFIX_2`, and so on.

```bash
python main.py --prompt "A high-frequency trading dashboard" --lint --refine --reason --multimodal --db --heal --deploy
```

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
