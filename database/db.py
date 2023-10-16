import os
from dotenv import load_dotenv
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    create_engine
)

from databases import Database

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(
    DATABASE_URL
)

metaData = MetaData()

Article = Table(
    'articles',
    metaData,
    Column("id", Integer, primary_key=True),
    Column("title", String(200)),
    Column("description", String(500))
)

User = Table(
    'users',
    metaData,
    Column("id", Integer, primary_key=True),
    Column("username", String(50)),
    Column("password", String(500))
)

database = Database(DATABASE_URL)
