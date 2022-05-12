import pymongo

# set a 5-second connection timeout
client = pymongo.MongoClient('localhost', 27017)

DATABASE = "bigdata_housing"
COLLECTION = "housing"

db = None
coll_housing = None

try:
    # print(client.server_info())
    db = client[DATABASE]
    coll_housing = db[COLLECTION]
    coll_task = 
except Exception:
    print("Unable to connect to the server.")