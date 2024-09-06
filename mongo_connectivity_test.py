from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# Use localhost with the forwarded port
MONGO_URI = "mongodb://admin:password123@localhost:27017/?authSource=admin"

def test_mongo_connection():
    try:
        # Create a MongoClient instance with the URI
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Attempt to connect to the server
        client.admin.command('ping')
        print("MongoDB connection successful.")
        
        # Perform additional operations if needed
        # Example: Get a list of databases
        databases = client.list_database_names()
        print("Databases:", databases)

    except ConnectionFailure as e:
        print("Could not connect to MongoDB:", e)
    except OperationFailure as e:
        print("Authentication failed:", e)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Close the connection
        client.close()

if __name__ == "__main__":
    test_mongo_connection()
