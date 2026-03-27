from typing import AsyncGenerator
from urllib.parse import urlparse, parse_qs

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.config import get_settings

settings = get_settings()

# Neon configuration: ai-foundry-products project, ai_consultancy schema
DB_SCHEMA = "ai_consultancy"

# Parse database URL and handle sslmode for asyncpg
parsed = urlparse(settings.database_url)
query_params = parse_qs(parsed.query)
ssl_mode = query_params.get('sslmode', ['require'])[0]

# Build clean URL without sslmode for asyncpg
DATABASE_URL = settings.database_url.replace(
    "postgresql://", "postgresql+asyncpg://"
).split('?')[0]

# SSL configuration for asyncpg
ssl_config = ssl_mode if ssl_mode != 'disable' else False

engine = create_async_engine(
    DATABASE_URL,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,
    echo=settings.app_debug,
    connect_args={
        "server_settings": {
            "search_path": DB_SCHEMA
        },
        "ssl": ssl_config,
    },
)

# Schema-aware metadata and base
metadata = MetaData(schema=DB_SCHEMA)
Base = declarative_base(metadata=metadata)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create schema and tables if they don't exist."""
    from sqlalchemy import text
    
    async with engine.begin() as conn:
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {DB_SCHEMA}"))
        await conn.run_sync(Base.metadata.create_all)
