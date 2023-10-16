from fastapi import FastAPI, status, HTTPException, APIRouter, Depends
from database.db import database, Article
from schema.schema import ArticleSchemaIn, ArticleSchemaOut, UserSchemaOut
from typing import List
from routers.auth import get_current_user
import json

articleRouter = APIRouter(
    tags=["Articles"]
)


@articleRouter.get('/articles', response_model=List[ArticleSchemaOut])
async def get_articles():
    query = Article.select()
    return await database.fetch_all(query=query)


@articleRouter.get('/articles/{id}', response_model=ArticleSchemaOut)
async def get_article_by_id(id: int, currenUser: UserSchemaOut = Depends(get_current_user)):
    query = Article.select().where(id == Article.c.id)
    find_article = await database.fetch_one(query=query)
    if not find_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Article Not Found')
    return find_article


@articleRouter.post('/articles', status_code=status.HTTP_201_CREATED)
async def insert_data(article: ArticleSchemaIn, currenUser: UserSchemaOut = Depends(get_current_user)):
    query = Article.insert().values(
        title=article.title,
        description=article.description
    )

    last_record_id = await database.execute(query)
    article_dict = json.loads(article.model_dump_json())
    return {**article_dict, "id": last_record_id}


@articleRouter.put('/articles/{id}', status_code=status.HTTP_200_OK)
async def update_data(id: int, article: ArticleSchemaIn, currenUser: UserSchemaOut = Depends(get_current_user)):
    query = Article.update().where(id == Article.c.id).values(
        title=article.title,
        description=article.description
    )

    updated_record_id = await database.execute(query)
    article_dict = json.loads(article.model_dump_json())
    return {**article_dict}


@articleRouter.delete('/articles/{id}', status_code=status.HTTP_200_OK)
async def delete_data(id: int, currenUser: UserSchemaOut = Depends(get_current_user)):
    query = Article.delete().where(id == Article.c.id)
    updated_record_id = await database.execute(query)
    return {'message': 'Data is deleted'}
