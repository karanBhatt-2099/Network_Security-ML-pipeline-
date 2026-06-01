
from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://wwwkaranbhatt18_db_user:Kriyansh07@cluster0.gcjaske.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)