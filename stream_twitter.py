from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import time
import json

ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            # print(data)
            # tweet = data.split(',"text"')[1].split('","source')[0]
            parsed = json.loads(data)
            created_at=parsed["created_at"]
            text=parsed["text"]           
            source=parsed["source"]
            r_count=str(parsed["retweet_count"])
            result1=parsed["user"]
            name=(result1["name"])
            final_result="Created_at:"+created_at+"\t||Name:"+name+"\t||Text:"+text+"\t||Source:"+source+"\t||Retweet_count:"+r_count
            print(final_result)            
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(final_result)
                tf.write("\n\n")
                # time.sleep(5)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
            # time.sleep(5)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    hash_tag_list = str(input("Enter keywords:"))
    fetched_tweets_filename = "tweets3.txt"
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
