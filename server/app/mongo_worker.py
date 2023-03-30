from pymongo import MongoClient

client = None

def get_database(db_name='test'):
    if client is None:
        client = MongoClient("mongodb+srv://root:example@localhost:27017")
    return client[name]

def get_collection(collection_name, db_name='test'):
    db = get_database(db_name)
    return db[collection_name]

def add_message(message, collection_name, db_name='test'):
    collection = get_collection(collection_name, db_name)
    result = collection.insert_one(message)
    return str(result.inserted_id)

def get_messages(lastRecieved, collection_name, db_name='test'):
    collection = get_collection(collection_name, db_name)
    result = list(collection.find({"_id": {"$gt": ObjectId(lastRecieved)}}, {"_id": False}))
