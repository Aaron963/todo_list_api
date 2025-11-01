from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import current_app

# 基础模型类
Base = declarative_base()


def init_postgres(app):
    """初始化PostgreSQL连接"""
    engine = create_engine(app.config["POSTGRES_URI"])
    app.postgres_session = sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine)
    if app.config["DEBUG"]:
        Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话（依赖注入）"""
    db = current_app.postgres_session()
    try:
        yield db
    finally:
        db.close()
