import argparse
from kafka import KafkaConsumer
from textblob import TextBlob
import json
from pymongo import MongoClient

def consumer(topic, database):
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'], value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    collection = database['tweet_info']
    for msg in consumer:
        tweets = json.loads(json.dumps(msg.value))
        # language detection and use of appropriate sentiment analysis module
        blob = TextBlob(tweets['text'])
        (tweets['sentiment'], tweets['subjectivity']) = blob.sentiment

        # keep only the first two decimal points of sentiment value and subjectivity
        tweets['sentiment'] = tweets['sentiment']
        tweets['subjectivity'] = tweets['subjectivity']
        tweets['topic'] = topic[:-6]
        tweets['cat_senti'] = 'Positive' if float(tweets['sentiment']) > 0.3 else 'Negative' if float(tweets['sentiment']) <-0.3 else 'Neutral'
        try:
            id = collection.insert_one(tweets)
            print("Data inserted with record ids", id)
        except:
            print("Could not insert")

if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description="Kafka topics")
    parser.add_argument("--topic", type=str, required=True, help="Topic name")
    args = parser.parse_args()
    
    try:
        client = MongoClient('localhost', 27017)
        database = client['tweet']
        print("Connected successfully")
    except:  
        print("Could not connect to MongoDB")

    consumer(args.topic, database)