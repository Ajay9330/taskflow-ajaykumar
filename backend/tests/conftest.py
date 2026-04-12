import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from alembic.config import Config
from alembic import command
from testcontainers.postgres import PostgresContainer
from app.main import app
from app.database import Base, get_db
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres

@pytest.fixture(scope="session")
async def test_engine(postgres_container):
    # testcontainers provides sync URL
    sync_url = postgres_container.get_connection_url()
    
    # We need async driver for SQLAlchemy AsyncEngine
    async_url = sync_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")

    # Run Alembic migrations programmatically
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", async_url)
    # This runs the upgrade head logic in alembic
    command.upgrade(alembic_cfg, "head")

    engine = create_async_engine(async_url)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def test_db(test_engine):
    async_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

@pytest.fixture(scope="function")
async def client(test_db):
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
