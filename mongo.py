import pymongo
import json

# Connect to MongoDB
client = pymongo.MongoClient('mongodb+srv://gowtham07:gowtham07@adscluster.rd2bauu.mongodb.net/')
db = client["adscluster"]  

# Load JSON data from file
try:
    with open('sorted_water_distance.json') as f:
        data = json.load(f)
    print("Data loaded successfully from JSON file:")
    print(data)
except Exception as e:
    print("Error loading JSON file:", e)
    data = {}

# Define the collection
collection = db["sorted_water"]

# Insert data into collection
if data:
    collection.insert_one(data)
    print("Data inserted successfully into MongoDB collection.")
else:
    print("Data is empty or invalid.")
