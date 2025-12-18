# SiteSage 🚀

### Automated SEO & Performance Analyzer

**Author:** Rohit Kumar Das  
**GitHub:** [https://github.com/rohitdas13595/sitesage](https://github.com/rohitdas13595/sitesage)  
**Deployed App:** [https://sitesage.rohituno.com/](https://sitesage.rohituno.com/)  
**API Documentation:** [https://apisitesage.rohituno.com/docs](https://apisitesage.rohituno.com/docs)

---

## 🏗️ Infrastructure & Rationale

- **CI/CD: GitHub Actions**  
  Chosen for its deep integration with the GitHub ecosystem. It allows for automated testing, Docker image building, and secure deployment to the VPS without needing external third-party tools.
- **Hosting: Personal VPS**  
  Selected for full administrative control and performance. Unlike PaaS providers, a VPS allows for custom Docker orchestration, optimized resource allocation, and precise control over the reverse proxy (Nginx) and SSL configurations.

---

SiteSage is a production-grade web platform that analyzes website URLs for SEO quality and performance using AI-powered insights.

[![CI/CD Pipeline](https://github.com/rohitdas13595/sitesage/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/rohitdas13595/sitesage/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Key Features

- **🔍 Deep URL Analysis**: Extract SEO metadata, headers, images, and accessibility data.
- **📊 Performance Scoring**: Lighthouse-style scoring for SEO, Performance, and Best Practices.
- **🤖 AI Insights**: Gemini-powered recommendations and executive summaries.
- **📦 Batch Processing**: Analyze up to 10 URLs concurrently with async workers.
- **🎨 Modern UI**: Responsive dashboard built with Next.js 15 and shadcn/ui.
- **🛠️ Production Ready**: Fully containerized with Docker and automated CI/CD.

## 🛠️ Tech Stack

- **Frontend**: Next.js 15 (App Router), TypeScript, TailwindCSS, shadcn/ui.
- **Backend**: FastAPI, SQLAlchemy 2.0, PostgreSQL, Alembic.
- **AI/ML**: Google Gemini API, LangChain.
- **DevOps**: Docker Compose, GitHub Actions, Pytest.

---

## 🚀 Quick Start

### 🐳 Using Docker (Recommended)

1. **Clone & Setup**:
   ```bash
   git clone <repository-url>
   cd mdlc
   cp backend/.env.example backend/.env
   ```
2. **Launch**:
   ```bash
   docker compose up --build -d
   ```
3. **Access**:
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 💻 Local Development

- **Backend**: `cd backend && pip install -r requirements.txt && uvicorn main:app --reload`
- **Frontend**: `cd frontend && npm install && npm run dev`

---

## 🔐 Environment Variables

Key variables required in `backend/.env`:

- `DATABASE_URL`: PostgreSQL connection string.
- `GOOGLE_API_KEY`: Your Gemini API key.
- `SECRET_KEY`: For JWT authentication.
- `NEXT_PUBLIC_API_URL`: (Frontend) Backend API endpoint.

---

## 🧪 Testing & Quality

- **Backend**: `cd backend && pytest tests/ -v`
- **Frontend**: `cd frontend && npm run lint && npx tsc --noEmit`

---

## 📂 Project Structure

```text
├── backend/          # FastAPI + SQLAlchemy + AI Logic
├── frontend/         # Next.js + shadcn/ui Dashboard
├── .github/          # CI/CD (GitHub Actions)
└── docker-compose.yml # Orchestration
```

## 🤝 Contributing

1. Fork the repo.
2. Create a feature branch.
3. Submit a PR with passing tests.

---

**Built for Madeline & Co. Full-Stack Assessment.**
MIT License.
