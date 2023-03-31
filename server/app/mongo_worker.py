from pymongo import MongoClient

client = None

def get_database(db_name='test'):
    global client
    if client is None:
        print("start login", flush=True)
        client = MongoClient("mongodb://root:example@mongo:27017")
        print("end login", flush=True)
    return client[db_name]

def get_collection(collection_name, db_name='test'):
    db = get_database(db_name)
    return db[collection_name]

def mongo_add_message(message, collection_name, db_name='test'):
    collection = get_collection(collection_name, db_name)
    result = collection.insert_one(message)
    return str(result.inserted_id)

def mongo_get_messages(lastRecieved, collection_name, db_name='test'):
    collection = get_collection(collection_name, db_name)
    filter = {}
    if lastRecieved is not None:
        filter["_id"] = {"$gt": ObjectId(lastRecieved)}
    result = list(collection.find(filter, {"_id": False}))
    return result
