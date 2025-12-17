# SiteSage - Automated SEO Performance Analyzer

[![CI/CD Pipeline](https://github.com/yourusername/sitesage/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/yourusername/sitesage/actions)

> A production-grade web platform that analyzes website URLs for SEO and performance quality with AI-powered insights.

## 🚀 Features

- **URL Analysis**: Crawl and extract SEO metadata from any website
- **SEO Scoring**: Comprehensive scoring based on best practices
- **AI Insights**: LangChain-powered recommendations and summaries
- **Batch Processing**: Analyze multiple URLs concurrently
- **Modern Dashboard**: Responsive Next.js frontend with shadcn/ui
- **RESTful API**: FastAPI backend with OpenAPI documentation
- **Containerized**: Full Docker Compose setup
- **CI/CD Pipeline**: Automated testing and deployment

## 🛠️ Tech Stack

### Frontend

- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **shadcn/ui** - UI components
- **date-fns** - Date formatting

### Backend

- **FastAPI** - Python web framework
- **LangChain** - AI orchestration
- **PostgreSQL** - Database
- **Alembic** - Database migrations
- **SQLAlchemy** - ORM
- **BeautifulSoup4** - Web scraping
- **aiohttp** - Async HTTP client

### DevOps

- **Docker & Docker Compose** - Containerization
- **GitHub Actions** - CI/CD
- **Pytest** - Backend testing
- **ESLint** - Frontend linting

## 📋 Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)
- OpenAI API key (optional, has fallback)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd mdlc
   ```

2. **Set up environment variables**

   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Edit backend/.env and add your OPENAI_API_KEY (optional)
   ```

3. **Start all services**

   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
# Make sure PostgreSQL is running
createdb sitesage

# Run migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 📚 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/v1/seo/analyze` - Analyze a single URL
- `POST /api/v1/seo/analyze/batch` - Analyze multiple URLs
- `GET /api/v1/seo/reports` - Get all reports (paginated)
- `GET /api/v1/seo/reports/{id}` - Get specific report
- `DELETE /api/v1/seo/reports/{id}` - Delete a report

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm run lint
npx tsc --noEmit  # Type checking
npm run build     # Build test
```

## 🗄️ Database Migrations

```bash
cd backend

# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Remove volumes (clean slate)
docker-compose down -v
```

## 📁 Project Structure

```
mdlc/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── services/     # Business logic
│   │   ├── models.py     # Database models
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── config.py     # Configuration
│   │   └── database.py   # Database setup
│   ├── alembic/          # Database migrations
│   ├── tests/            # Test files
│   ├── main.py           # Application entry point
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js app directory
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities
│   │   └── types/        # TypeScript types
│   ├── public/           # Static assets
│   ├── package.json
│   └── Dockerfile
├── .github/
│   └── workflows/        # CI/CD pipelines
└── docker-compose.yml
```

## 🎨 Features Breakdown

### Core Features ✅

- [x] URL crawling and data extraction
- [x] SEO analysis and scoring
- [x] AI insight generation with LangChain
- [x] Report generation and storage
- [x] Modern responsive dashboard
- [x] Batch URL processing
- [x] PostgreSQL with Alembic migrations
- [x] Docker containerization
- [x] CI/CD pipeline
- [x] Automated tests

### Bonus Features 🎁

- [x] shadcn/ui components
- [x] Grid and table view modes
- [x] Real-time loading states
- [x] Error handling
- [x] Responsive design
- [ ] PDF report generation
- [ ] Historical tracking
- [ ] Authentication
- [ ] AWS S3 integration

## 🔧 Configuration

### Environment Variables

#### Backend (`backend/.env`)

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
OPENAI_API_KEY=your-api-key
LLM_MODEL=gpt-3.5-turbo
DEBUG=False
```

#### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚀 Deployment

### Deploy to Render

1. Create a new PostgreSQL database
2. Create a new Web Service for backend
3. Create a new Static Site for frontend
4. Set environment variables
5. Deploy!

### Deploy to Railway

```bash
railway login
railway init
railway up
```

## 📊 Performance

- Async URL crawling for fast batch processing
- Database connection pooling
- Optimized Docker images with multi-stage builds
- Frontend code splitting and lazy loading
- Efficient caching strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📝 License

MIT License - feel free to use this project for learning or commercial purposes.

## 👨‍💻 Author

Built as a full-stack developer assessment project for Madeline & Co.

## 🙏 Acknowledgments

- FastAPI for the excellent Python framework
- Next.js team for the amazing React framework
- shadcn for the beautiful UI components
- LangChain for AI orchestration

---

**Note**: This is a production-ready application built with best practices in mind. All core requirements and several bonus features have been implemented.
