import redis
import configparser
import json
import uuid

config = configparser.ConfigParser()
config.read('../config/config.ini')
r_host = config['redis']['host']
r_port = config['redis']['port']
r_db = config['redis']['db']

r = redis.StrictRedis(r_host, r_port, r_db)
r_content = json.loads(r.get("xushengchao").decode('utf-8'))
r_content['token'] = uuid.uuid4().hex
r.set("xushengchao", json.dumps(r_content))

print(json.loads(r.get("xushengchao").decode("utf-8"))['pwd'])