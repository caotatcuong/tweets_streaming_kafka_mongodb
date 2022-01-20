import argparse
import json
from kafka import KafkaProducer
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''

class TweetListener(StreamListener):
    def __init__(self, topic):
        super().__init__()
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        
    def on_data(self, raw_data):
        try:
            json_data = json.loads(raw_data)
            send_data = '{}'
            json_send_data = json.loads(send_data)			

            json_send_data['text'] = json_data['text']                  
            json_send_data['creation_datetime'] = json_data['created_at']
            json_send_data['username'] = json_data['user']['name']
            json_send_data['location'] = json_data['user']['location'] 
            json_send_data['userDescr'] = json_data['user']['description']            
            json_send_data['followers'] = json_data['user']['followers_count']
            json_send_data['favorites'] = json_data['favorite_count']

            self.producer.send(self.topic, json.dumps(json_send_data).encode('utf-8'))

        except Exception as e:
            print(e)
            return False
        return True

def stream_tweets(topic, word):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    while True:
        # filter tweets contains word
        twitter_stream = Stream(auth, TweetListener(topic))
        twitter_stream.filter(track=word, languages = ['en'])

if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description="Kafka topics")
    parser.add_argument("--topic", type=str, required=True, help="Topic name")
    parser.add_argument("--word", type=str, required=True, help="Keywords to track")
    args = parser.parse_args()
    
    stream_tweets(args.topic, args.word)