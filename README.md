# 🌌 Singularity AGI: Full-Stack AI App Builder

**Production-ready AI-powered application builder** - Generate, build, and deploy full-stack Next.js/Supabase applications using free API tiers from OpenRouter, Groq, and Google Gemini.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 📖 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## ✨ Features

### 🤖 AI-Powered Development
- **Smart Multi-Agent System**: Specialized agents for architecture, coding, security, and documentation
- **Multi-Provider Routing**: Automatic failover between OpenRouter, Groq, and Gemini
- **Self-Healing Builds**: Automatically detects and fixes errors during build process
- **Continuous Learning**: Learns from successful patterns stored in Supabase

### 🚀 Production-Ready
- **Docker Support**: Fully containerized for easy deployment
- **Multi-Platform Deployment**: One-click deploy to Netlify, Vercel, Railway, or Render
- **Health Monitoring**: Built-in health checks and monitoring
- **Auto-Scaling**: Worker-based architecture for high-traffic deployments
- **Security Best Practices**: Non-root containers, CORS configuration, secret management

### 🎨 Advanced Capabilities
- **Auto-Bug Detection**: Proactive security scanning and syntax checking
- **Code Refinement**: Automatic optimization and best practices enforcement
- **Multi-Modal Generation**: UI mockups and architecture diagrams
- **Database Orchestration**: Automated schema generation and migrations
- **Version Rollback**: Snapshot and revert to previous working versions

---

## 🚀 Quick Start

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/your-username/singularity-agi.git
cd singularity-agi

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

### 3. Start the Backend

```bash
# Using Python
python api.py

# Or using the production startup script
./start.sh

# Or using Docker
docker build -t singularity-agi .
docker run -p 8000:8000 --env-file .env singularity-agi
```

### 4. Access the API

- **API Root**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Redoc**: http://localhost:8000/redoc

---

## 🏗️ Architecture

### Core Pipeline
```
User Prompt → Architect → Coder → Healer → Deployer → Live App
                  ↓           ↓         ↓         ↓
            Blueprint   Code Gen  Bug Fix  Deployment
```

### AI Agents
- **Smart Router**: Multi-provider routing with key rotation
- **Architect**: Decomposes prompts into JSON blueprints
- **Coder**: Multi-agent code generation (Frontend, Backend, Security)
- **Healer**: Self-healing build loops
- **Linter**: Proactive bug detection and auto-fixing
- **Refiner**: Code optimization and best practices
- **Deployer**: Multi-platform deployment automation

### Database & Storage
- **Supabase**: Platform database for projects and build logs
- **Neon**: Database branching for isolated development environments
- **Migration Engine**: Automated SQL schema generation

---

## 📋 Prerequisites

### System Requirements
- **Python**: 3.10 or higher
- **Git**: Latest version
- **Node.js**: 20+ (for running generated apps)
- **Docker**: (optional, for containerized deployment)

### Required API Keys

| Service | Purpose | Free Tier |
|---------|---------|-----------|
| [OpenRouter](https://openrouter.ai/) | AI provider | Yes |
| [Groq](https://console.groq.com/) | Fast LLM inference | Yes |
| [Google Gemini](https://aistudio.google.com/) | AI provider | Yes |
| [GitHub](https://github.com/settings/tokens) | Code hosting | Yes |

### Optional Deployment Tokens
- **Netlify**: [Get Token](https://app.netlify.com/user/settings/applications)
- **Vercel**: [Get Token](https://vercel.com/account/tokens)
- **Railway**: [Get Token](https://railway.app/account/tokens)
- **Render**: [Get Token](https://dashboard.render.com/user/settings/api-tokens)

### Database Services
- **Supabase**: [Get Credentials](https://supabase.com/dashboard)
- **Neon**: [Get API Key](https://console.neon.tech/)

---

## 🔧 Installation

### Local Development

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Start the server
python api.py
```

### Docker Installation

```bash
# Build the image
docker build -t singularity-agi .

# Run the container
docker run -d \
  --name singularity-api \
  -p 8000:8000 \
  --env-file .env \
  singularity-agi

# View logs
docker logs -f singularity-api
```

### Frontend Dashboard

```bash
# Navigate to dashboard directory
cd dashboard

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
npm start
```

---

## 💻 Usage

### CLI Usage

```bash
# Basic build
python main.py --prompt "A task management app for remote teams"

# Build with all features
python main.py --prompt "Coffee shop ordering system" \
  --deploy \
  --heal \
  --docs \
  --refine \
  --lint \
  --db \
  --reason \
  --multimodal
```

### API Usage

#### WebSocket Build

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/build');

ws.onopen = () => {
  ws.send(JSON.stringify({
    prompt: "Build a modern e-commerce site",
    deploy: "netlify",
    heal: true,
    docs: true,
    refine: true,
    lint: true
  }));
};

ws.onmessage = (event) => {
  console.log('Build log:', event.data);
};
```

#### REST API

```bash
# Get all projects
curl http://localhost:8000/projects

# Get monitoring status
curl http://localhost:8000/monitor

# Health check
curl http://localhost:8000/health
```

---

## 🚢 Deployment

### Quick Deploy to Render (Recommended)

1. **Create Render Account**: [render.com](https://render.com)
2. **Connect GitHub Repository**
3. **Deploy using `render.yaml` configuration**
4. **Set environment variables** (see `.env.example`)
5. **Your API will be live** at `https://your-app.onrender.com`

👉 **Full Deployment Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)

### Supported Platforms

| Platform | Status | Documentation |
|----------|--------|---------------|
| Render | ✅ Recommended | [render.yaml](render.yaml) |
| Docker | ✅ Supported | [Dockerfile](Dockerfile) |
| Heroku | ✅ Supported | [Procfile](Procfile) |
| Railway | ✅ Supported | Built-in support |
| Vercel | ✅ Frontend only | Dashboard |
| Netlify | ✅ Frontend only | Dashboard |

---

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc documentation |
| GET | `/projects` | Get all projects |
| GET | `/monitor` | Get monitoring status |
| WS | `/ws/build` | WebSocket build endpoint |

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## ⚙️ Configuration

### Environment Variables

```bash
# Server Configuration
PORT=8000                    # Server port
WORKERS=1                    # Number of workers
ENVIRONMENT=production       # Environment
ALLOWED_ORIGINS=*            # CORS origins

# AI Provider Keys
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

### Multi-Key Rotation

To avoid rate limits, add multiple keys:

```bash
OPENROUTER_API_KEY=key1
OPENROUTER_API_KEY_1=key2
OPENROUTER_API_KEY_2=key3

GROQ_API_KEY=key1
GROQ_API_KEY_1=key2
```

The system will automatically rotate keys when limits are reached.

---

## 🔧 Troubleshooting

### Build Failures

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Docker Issues

```bash
# Rebuild without cache
docker build --no-cache -t singularity-agi .

# Check logs
docker logs singularity-api

# Enter container
docker exec -it singularity-api bash
```

### API Key Errors

- Verify keys in `.env` file
- Check for extra spaces or quotes
- Ensure keys are active and not expired
- Test keys individually with provider APIs

### CORS Issues

- Set `ALLOWED_ORIGINS` to your frontend domain
- For development, use `ALLOWED_ORIGINS=*`
- Check browser console for specific CORS errors

---

## 📈 Performance Optimization

### Production Tips

1. **Increase Workers**: Set `WORKERS=4` for higher concurrency
2. **Use Redis**: Add caching for expensive operations
3. **CDN**: Use Cloudflare for API response caching
4. **Monitor**: Set up Sentry for error tracking
5. **Scale**: Use larger instances for production

### Free Tier Limits

| Provider | Requests/Day | Requests/Minute |
|----------|--------------|------------------|
| OpenRouter | 50 | 20 |
| Groq | 1000 | 30 |
| Gemini | 250 | 20 |

**Tip**: Use multi-key rotation to multiply these limits!

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Test your changes thoroughly
- Update documentation as needed

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **OpenRouter**: Multi-provider AI routing
- **Groq**: Fast LLM inference
- **Google**: Gemini AI models
- **Supabase**: Database and auth platform
- **Neon**: Serverless PostgreSQL
- **FastAPI**: Modern web framework

---

## 📞 Support

- **Documentation**: [README.md](README.md), [DEPLOYMENT.md](DEPLOYMENT.md)
- **Issues**: [GitHub Issues](https://github.com/your-username/singularity-agi/issues)
- **Discord**: [Join our community](#)

---

## 🗺️ Roadmap

- [ ] Web UI for configuration
- [ ] Real-time build visualization
- [ ] Custom template marketplace
- [ ] Team collaboration features
- [ ] Advanced monitoring dashboard
- [ ] Mobile app support

---

**Built with ❤️ by the Singularity AGI Team**

*Generate full-stack applications in minutes, not hours.*
