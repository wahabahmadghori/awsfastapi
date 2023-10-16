from fastapi import APIRouter, status
from database.db import User, database
from schema.schema import UserSchemaIn, UserSchemaOut
from passlib.hash import pbkdf2_sha256
import json
from typing import List
userRouter = APIRouter(
    tags=["Users"]
)


@userRouter.get("/users", response_model=List[UserSchemaOut])
async def get_users():
    query = User.select()
    return await database.fetch_all(query=query)


@userRouter.post('/users', status_code=status.HTTP_201_CREATED,
                 response_model=UserSchemaOut)
async def create_user(user: UserSchemaIn):
    hashPassword = pbkdf2_sha256.hash(user.password)
    query = User.insert().values(
        username=user.username,
        password=hashPassword
    )
    lastUserId = await database.execute(query=query)
    user_dict = json.loads(user.model_dump_json())
    return {**user_dict}
