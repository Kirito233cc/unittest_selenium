from data_object.table_user import User
from config.settings import link


session = link.link_mysql()
print(session.query(User).filter(User.user_name == "xushengchao").one().user_name)