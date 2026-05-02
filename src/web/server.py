import datetime

import uvicorn
from datetime import *

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response

from schemes import *

from src.database.db import check_mail_and_username
from src.database.dep import SessionDep
from src.database.db import get_current_user
from src.database.db import create_table
from src.database.db import drop_table
from src.database.model import UserModel
from src.database.db import search_user

from src.auth.hashing import *
from src.auth.jwt_token_settings import *


limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title='SimpleAuth')

app.state.limiter = limiter #type: ignore
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) #type: ignore

app.add_middleware(CORSMiddleware, #type: ignore
                   allow_origins=['*'],
                   allow_methods=['*'],
                   allow_headers=['*'])


@app.get('/', tags=['system'], summary='base information')
async def base_endpoint():
    return 'Welcome to SimpleAuth'

@app.post('/create_table_db', tags=['database'], summary='create table')
async def create_table_db():
    await create_table()
    return 'table created'


@app.post('/drop_table_db', tags=['database'], summary='drop table')
async def drop_table_db():
    await drop_table()
    return 'table destroyed'

@app.post('/create_account', tags=['user'], summary='User create new account')
@limiter.limit('5/minute')
async def create_account(creds: CreateUser, session: SessionDep, request: Request):
    password, salt = await hash_password(password=creds.password)
    new_user = UserModel(
        first_name = creds.first_name,
        username = creds.username,
        mail = creds.mail,
        create_at = datetime.now(timezone.utc),
        hash_password = password,
        salt = salt
    )

    valid_mail = str(creds.mail)

    if await check_mail_and_username(session, username=creds.username, mail=valid_mail):
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        access_token = security.create_access_token(uid=new_user.username)
        account_id = new_user.id
        account_first_name = new_user.first_name
        account_create_at = new_user.create_at
        account_username = new_user.username

        return {
            'account_ID': account_id,
            'account_first_name': account_first_name,
            'account_username': account_username,
            'account_create_at': account_create_at,
            'access_token': access_token
        }


    elif not await check_mail_and_username(session, username=creds.username, mail=valid_mail):
        raise HTTPException(status_code=400, detail='This user already exists')

@app.get('/get_account/{user_id}', tags=['user'], summary='Get user account (user_id)')
@limiter.limit('5/minute')
async def get_account(user_id: int, session: SessionDep, request: Request):
    try:
        user = await get_current_user(user_id=user_id, session=session)

        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        if user:
            return {
                'account_id': user.username,
                'account_first_name': user.first_name,
                'account_create_at': user.create_at,
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@app.post('/login', tags=['user'], summary='login in account (password)')
@limiter.limit('5/minute')
async def login(creds: Login, session: SessionDep, request: Request, response: Response):
    user = await search_user(username=creds.username, password=creds.password, session=session)

    if not user:
        raise HTTPException(status_code=401, detail='Incorrect data')

    else:
        access_token = security.create_access_token(uid=creds.username,fresh=True)
        refresh_token = security.create_refresh_token(uid=creds.username)

        security.set_access_cookies(access_token, response)
        security.set_refresh_cookies(refresh_token, response)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer',
        }

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='127.0.0.8')
