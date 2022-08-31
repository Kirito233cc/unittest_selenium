from sqlalchemy import Column, String, SmallInteger, DATETIME
from sqlalchemy.ext.declarative import declarative_base

# 创建对象基类
Base = declarative_base()


# 定义element表对象
class Page_module_detail(Base):
    # 表名
    __tablename__ = 'page_module_detail'
    # 表结构
    id = Column(SmallInteger, primary_key=True)
    page_module_id = Column(SmallInteger)
    element_id = Column(SmallInteger)
    operate_type = Column(SmallInteger)
    send_msg = Column(String(255))
    operate_step = Column(SmallInteger)
    created_at = Column(DATETIME)
    updated_at = Column(DATETIME)
    deleted_at = Column(DATETIME)
