import uvicorn
from aiohttp.abc import HTTPException
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemes import *
from src.database.dep import SessionDep
from src.database.db import get_current_user
from src.database.db import create_table
from src.database.db import drop_table
from datetime import *
from src.database.model import UserModel
from src.auth.hashing import *
from src.auth.jwt_token_settings import *

app = FastAPI(title='SimpleAuth')

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
async def create_account(creds: CreateUser, session: SessionDep):
    password, salt = await hash_password(password=creds.password)
    new_user = UserModel(
        first_name = creds.first_name,
        username = creds.username,
        mail = creds.mail,
        create_at = datetime.now().strftime('%H:%M:%S'),
        hash_password = password,
        salt = salt
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    access_token = security.create_access_token(uid=new_user.username)
    account_id = new_user.id
    account_first_name = new_user.first_name
    account_create_at = new_user.create_at

    return{
        'account ID': account_id,
        'account first name': account_first_name,
        'account create at': account_create_at,
        'access token': access_token
    }

@app.post('/get_account', tags=['user'], summary='Get user account (user_id)')
async def get_account(creds: GetUser, session: SessionDep):
    try:
        user = await get_current_user(user_name=creds.username, session=session)

        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        is_verified = await verify_password(
            password=creds.password,
            save_hash=user.hash_password,
            save_salt=user.salt
        )

        if user and is_verified:

            return {
                'account ID': user.username,
                'account first name': user.first_name,
                'account create at': user.create_at,
            }

    except Exception as e:
        return {'error': e}

if __name__ == '__main__':

    uvicorn.run(app, port=8080, host='127.0.0.8')
