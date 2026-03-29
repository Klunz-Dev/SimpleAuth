from src.database.db import get_session
from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

SessionDep = Annotated[AsyncSession, Depends(get_session)]
