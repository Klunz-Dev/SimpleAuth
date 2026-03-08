import uvicorn
from fastapi import FastAPI
from src.web.schemes import *
from src.database.dep import SessionDep
from src.database.db import get_current_user
from src.database.db import create_table
from src.database.db import drop_table
from datetime import *
from src.database.model import UserModel
from src.auth.hashing import *
from src.auth.jwt_token_settings import *

app = FastAPI(title='SimpleAuth')

@app.get('/', tags=['system'], summary='base information')
async def base_endpoint():
    return 'SimpleAuth'

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

@app.get('/get_account/{user_id}', tags=['user'], summary='Get user account (user_id)')
async def get_account(user_id: int, session: SessionDep):
    try:
        current_user = await get_current_user(user_id, session)

        return {
            'id': current_user.id,
            'username': current_user.username,
            'first name': current_user.first_name,
            'mail': current_user.mail,
            'create_at': current_user.create_at
        }

    except Exception as e:
        print(e)
        return {'error': e}

if __name__ == '__main__':

    uvicorn.run(app, port=8080, host='127.0.0.8')
