from tweepy import OAuthHandler,Stream
from tweepy.streaming import StreamListener
from kafka_client import get_kafka_client
import json

import credentials


class TweetProducer(StreamListener):
    def __init__(self):
        self.__client=get_kafka_client()
    
    def on_data(self,data):    
        if self.check_geo_tagging(json.loads(data)):
            topic=self.__client.topics['twitterstream']
            producer=topic.get_sync_producer()
            producer.produce(data.encode('utf-8'))
    
    def check_geo_tagging(self,data:dict)->bool:
        return True if data['place'] else True

    def on_error(self,status):
        print(status)
        return False

if __name__ == "__main__":
    auth = OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
    producer_obj=TweetProducer()
    stream_obj=Stream(auth,producer_obj)
    stream_obj.filter(track=['nasa'],is_async=True)