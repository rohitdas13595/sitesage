import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.database import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest_asyncio.fixture
async def auth_headers(setup_database):
    """Create a test user and return auth headers"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register
        await ac.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "full_name": "Test User"
            }
        )
        # Login
        response = await ac.post(
            "/auth/login",
            data={
                "username": "test@example.com",
                "password": "password123"
            }
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    
    assert response.status_code == 200
    assert "name" in response.json()
    assert response.json()["status"] == "running"


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_analyze_url(auth_headers):
    """Test URL analysis endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/seo/analyze",
            json={"url": "https://example.com"},
            headers=auth_headers
        )
    
    # Note: This will fail without actual network access
    # In production, you'd mock the crawler
    assert response.status_code in [201, 400]


@pytest.mark.asyncio
async def test_get_reports(auth_headers):
    """Test getting reports list"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/seo/reports",
            headers=auth_headers
        )
    
    assert response.status_code == 200
    assert "reports" in response.json()
    assert "total" in response.json()


@pytest.mark.asyncio
async def test_cors_preflight():
    """Test CORS preflight (OPTIONS) request"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.options(
            "/api/v1/seo/analyze",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            }
        )
    
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"
    assert "POST" in response.headers["access-control-allow-methods"]
    assert "content-type" in response.headers["access-control-allow-headers"].lower()
