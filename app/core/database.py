from app.core import configuration
import pymongo
client  = pymongo.MongoClient(configuration.APP_MONGO_URI)
db = client.get_database(configuration.APP_MONGO_DB)