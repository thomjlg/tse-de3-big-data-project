# coding=<UTF-8>
import pandas as pd
from pymongo import MongoClient
import json

def mongoimport(csv_path, db_name, coll_name, db_url, db_port=27017):
    client = MongoClient(db_url, db_port)
    db = client[db_name]
    coll = db[coll_name]
    data = pd.read_csv(csv_path)
    payload = json.loads(data.to_json(orient='records'))
    coll.delete_many({})
    coll.insert_many(payload)
    print("Insert termine")

mongoimport("./Data/predicted.csv", "big-data-machine-learning", "predictions", "mongodb+srv://mbergamin:ba6t32ms78tf@big-data-project.g26gj.mongodb.net/?retryWrites=true&w=majority")

