from sqlalchemy import Column, String, SmallInteger, DATETIME
from sqlalchemy.ext.declarative import declarative_base

# 创建对象基类
Base = declarative_base()


# 定义element表对象
class Page_module(Base):
    # 表名
    __tablename__ = 'page_module'
    # 表结构
    id = Column(SmallInteger, primary_key=True)
    module_name = Column(String(50))
    created_at = Column(DATETIME)
    updated_at = Column(DATETIME)
    deleted_at = Column(DATETIME)
