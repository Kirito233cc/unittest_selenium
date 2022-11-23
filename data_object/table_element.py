from sqlalchemy import Column, String, SmallInteger, DATETIME
from sqlalchemy.ext.declarative import declarative_base

# 创建对象基类
Base = declarative_base()


# 定义element表对象
class Element(Base):
    # 表名
    __tablename__ = 'element'
    # 表结构
    id = Column(SmallInteger, primary_key=True)
    element_name = Column(String(100))
    element_type = Column(SmallInteger)
    element_address = Column(String(250))
    remark = Column(String(255))
    created_at = Column(DATETIME)
    updated_at = Column(DATETIME)
    deleted_at = Column(DATETIME)
