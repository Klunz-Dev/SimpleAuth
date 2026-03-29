from pydantic import BaseModel, Field, EmailStr

class CreateUser(BaseModel):
    first_name: str = Field(..., title="You're first name", min_length=1, max_length=16)
    username: str = Field(..., title="You're username", min_length=1, max_length=16)
    mail: EmailStr = Field(..., title="You're mail")
    password: str = Field(..., title="You're password (min: 8, max: 32)", min_length=8, max_length=32)

class GetUser(BaseModel):
    username: str = Field(..., title="You're username", min_length=1, max_length=16)
    password: str = Field(..., title="You're password (min: 8, max: 32)", min_length=8, max_length=32)