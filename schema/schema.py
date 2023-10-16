from pydantic import BaseModel


class ArticleSchemaIn(BaseModel):
    title: str
    description: str


class ArticleSchemaOut(BaseModel):
    title: str
    description: str


class UserSchemaIn(BaseModel):
    username: str
    password: str


class UserSchemaOut(BaseModel):
    username: str


class LoginInSchema(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
