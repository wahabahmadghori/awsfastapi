import uvicorn
from fastapi import FastAPI, status, HTTPException
from database.db import metaData, database, engine, Article
from routers.article import articleRouter
from routers.user import userRouter
import routers.auth as auth
metaData.create_all(engine)

app = FastAPI()

app.include_router(articleRouter)
app.include_router(userRouter)
app.include_router(auth.router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run('main:app', port=8080, reload=True, log_level="info")
