from src.database.model import *
from sqlalchemy import select, or_
from src.auth.hashing import *
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


async def get_current_user(user_id: int, session: AsyncSession):
    try:
        result = await session.execute(select(UserModel).where(UserModel.id == user_id))
        current_user = result.scalars().first()

        return current_user
    except Exception as e:
        return {'error': e}


async def check_mail_and_username(session: AsyncSession, username: str, mail: str) -> bool:
    result = await session.execute(select(UserModel).where(or_(UserModel.username == username, UserModel.mail == mail)))
    user = result.scalars().all()

    if len(user) == 0:
        return True
    else:
        return False


async def search_user(username: str, password: str, session: AsyncSession):

    result = await session.execute(select(UserModel).where(UserModel.username == username))
    user = result.scalars().first()

    if user:
        is_verify = await verify_password(password=password, save_hash=user.hash_password, save_salt=user.salt)

        if user and is_verify:
            return user

    else:
        return None
