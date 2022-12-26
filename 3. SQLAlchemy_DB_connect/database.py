# sqlalchemy는 파이썬에서 데이터베이스를 다루는 툴이다.
# FastAPI에서는 sqlalchemy를 이용해 데이터베이스를 다룰 수 있다.
# ORM (Object Relation Mapping)은 객체를 데이터베이스 테이블과 매칭시켜주는 tool이다.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://user:password@postgresserver/db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# Base.metadata.create_all(bind=engine)     # 데이터베이스를 최초에 생성할 때 사용
# Base.metadata.bind = engine               # 이미 존재하는 데이터베이스에 연결할 때 사용
