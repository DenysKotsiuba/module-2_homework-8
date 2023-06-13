from configparser import ConfigParser

from mongoengine import connect


config = ConfigParser()
config.read("part_1/config.ini")

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'password')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

uri = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"
client = connect(host=uri, ssl=True)