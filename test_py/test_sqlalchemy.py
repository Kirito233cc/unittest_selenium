import configparser
import json
import uuid

import redis
from flask import Blueprint, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_object.table_user import User
from settings.settings import link


session = link.link_mysql()
print(session.query(User).filter(User.user_name == "xushengchao").one().user_name)