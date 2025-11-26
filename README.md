# 🤖 HookSense - AI Code Reviewer

> An intelligent, automated code review system powered by LLMs that integrates seamlessly with GitHub to provide instant, high-quality code reviews on every pull request.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16.0-black.svg)](https://nextjs.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## ✨ Features

- **🔄 Automatic PR Reviews** - Automatically triggered on pull request creation and updates
- **🧠 Multiple LLM Support** - OpenAI GPT-4, Google Gemini, or fine-tuned local models
- **📊 Real-time Dashboard** - Track metrics, review history, and system performance
- **🎯 Smart Code Analysis** - AST-based Python code analysis with contextual understanding
- **💡 Actionable Feedback** - Line-specific suggestions with detailed explanations
- **🔧 Self-Improving** - Collects feedback to continuously improve review quality
- **⚡ Scalable Architecture** - Celery-based async processing with Redis backend
- **🐳 Docker Ready** - One-command deployment with Docker Compose

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐
│  GitHub Webhook │────────▶│  FastAPI Backend │
└─────────────────┘         └────────┬─────────┘
                                     │
                            ┌────────▼─────────┐
                            │  Celery Worker   │
                            └────────┬─────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
            ┌───────▼──────┐  ┌─────▼─────┐  ┌──────▼──────┐
            │  LLM Provider │  │  Database │  │  Code       │
            │  (GPT/Gemini) │  │ (Postgres)│  │  Analyzer   │
            └──────────────┘  └───────────┘  └─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- GitHub account with repository access
- OpenAI API key or Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-code-reviewer.git
   cd ai-code-reviewer
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Launch with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the dashboard**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Configuration

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/codereview

# Redis
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# LLM Provider (choose one)
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here

# Or use local model
USE_LOCAL_LLM=false

# GitHub
GITHUB_TOKEN=your_github_token_here
```

## 🔌 GitHub Integration

### Setting up Webhooks

1. Go to your GitHub repository settings
2. Navigate to **Webhooks** → **Add webhook**
3. Configure:
   - **Payload URL**: `https://your-domain.com/webhook`
   - **Content type**: `application/json`
   - **Events**: Select "Pull requests"
4. Save and test the webhook

### How It Works

1. Developer creates or updates a PR
2. GitHub sends webhook event to your backend
3. Celery worker fetches PR diff and analyzes code
4. LLM generates comprehensive review
5. Review posted as PR comment with suggestions
6. Metrics updated in dashboard

## 📊 Dashboard Features

The Next.js dashboard provides:

- **Metrics Overview**: Total reviews, issues found, average review time
- **Recent Activity**: Latest reviews with status indicators
- **Review History**: Detailed view of all past reviews
- **Performance Analytics**: Track improvement over time

## 🧪 Advanced Features

### Fine-tuning with Custom Data

Train the system on your team's code review patterns:

```bash
# Collect review data with feedback
python backend/app/train.py

# Or train local model with QLoRA
python backend/app/train_local.py
```

### Local LLM Support

Run completely offline with a fine-tuned CodeLlama model:

```bash
# Set in .env
USE_LOCAL_LLM=true

# Model automatically loads from models/local_finetuned
```

### Code Analysis

The system performs deep static analysis:
- Function and class extraction
- Import dependency analysis
- Code complexity metrics
- Pattern detection

## 🛠️ Development

### Project Structure

```
.
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── main.py      # API endpoints
│   │   ├── worker.py    # Celery tasks
│   │   ├── llm.py       # LLM providers
│   │   ├── analysis.py  # Code analyzer
│   │   └── models.py    # Database models
│   └── Dockerfile
├── frontend/            # Next.js dashboard
│   ├── app/
│   │   └── page.tsx    # Main dashboard
│   └── Dockerfile.dev
├── data/
│   └── fine_tuning/    # Training data
└── docker-compose.yml
```

### Running Locally

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
celery -A app.worker.celery worker --loglevel=info
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### API Endpoints

- `GET /` - Health check
- `POST /webhook` - GitHub webhook handler
- `GET /metrics` - System metrics
- `GET /reviews` - Recent reviews
- `POST /feedback` - Submit review feedback

## 🚢 Deployment

### Render.com (Recommended)

1. Connect your GitHub repository
2. Use `render.yaml` for configuration
3. Add environment variables in Render dashboard
4. Deploy with one click

### Self-hosted

Use `docker-compose.yml` for production deployment with proper secrets management.

## 🧠 Supported LLM Providers

| Provider | Model | Cost | Speed | Quality |
|----------|-------|------|-------|---------|
| OpenAI | GPT-4 Turbo | $$$ | Fast | Excellent |
| Google | Gemini Pro | $$ | Fast | Great |
| Local | CodeLlama-7B | Free | Medium | Good |

## 📈 Performance

- Average review time: 1-3 seconds
- Concurrent PR processing: 10+
- API response time: <100ms
- Database queries optimized with indexes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend powered by [Next.js](https://nextjs.org/)
- LLM integrations via [OpenAI](https://openai.com/) and [Google AI](https://ai.google/)
- Code analysis using Python's AST module

## 💬 Support

- 📧 Email: aryanghate29@gmail.com
- 🐛 Issues: Raise an issue in the repo

---

Made with ❤️ by developers, for developers
