import time
import json

from kafka import KafkaConsumer
from pymongo import MongoClient


CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

consumer = KafkaConsumer('RawNewsCollection',
                         bootstrap_servers=['localhost:9092'],
                         enable_auto_commit=True,
                         group_id='mongo_db_client',
                         value_deserializer=lambda x: x.decode('utf-8'))

db_client = MongoClient(CONNECTION_STRING)
raw_collection = db_client['wnews_db']['raw_news']

raw_collection.delete_many({})

while True:
    for message in consumer:
        if message is not None:
            print(message.value)
            raw_collection.insert_one(json.loads(message.value))
    time.sleep(10)
