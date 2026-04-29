from src.database.model import *
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

db_url = 'sqlite+aiosqlite:///users.db'
async_engine = create_async_engine(url=db_url)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

async def get_session():
    async with async_session() as session:
        yield session

async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_current_user(user_name: str, session: AsyncSession):
    try:
        result = await session.execute(select(UserModel).where(UserModel.username == user_name))
        current_user = result.scalars().first()

        return current_user
    except Exception as e:
        return {'error': e}

async def check_mail_and_username(session: AsyncSession, username: str, mail: str) -> bool:
    result = await session.execute(select(UserModel).where(UserModel.username == username, UserModel.mail == mail))
    user = result.scalars().all()
    return user is not True