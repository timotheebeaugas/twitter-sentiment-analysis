# -*- coding: utf8 -*-
import config, tweepy, time, csv
from datetime import date, timedelta, datetime  
from tweepy import OAuthHandler, Stream, StreamListener

# connection to Twitter API
auth = tweepy.OAuthHandler(
    config.twitterApi['key'], config.twitterApi['secret'])
auth.set_access_token(
    config.twitterApi['token'], config.twitterApi['tokenSecret'])

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        """ 
        exclusion of retweet to avoid identical posts
        retrieving full text of tweets 
        saving texts in a file
        """
        status = api.get_status(status.id, tweet_mode="extended")
        try:
            status.retweeted_status.full_text
        except AttributeError:  # Not a Retweet
            try:
                print('TEXT : ', status.full_text)
                todayDate = str(datetime.utcnow().date().today()) # current date storage to name the backup file
                f = open("input/"+todayDate+".csv", "a", newline='', encoding='utf-8')
                writer = csv.writer(f, delimiter=',')
                writer.writerow([status.created_at, status.full_text.replace("\n", " ")])
                f.close()
            except Exception as e:
                print(e)
                pass

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False

def startStream():
    """ 
    stream launch and forced restart with delay in case of errors 
    """
    i = int(1)
    while True: # reconnection loop to twitter api
        try: # streaming ranking
            myStreamListener = MyStreamListener()
            myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
            myStream.filter(track=['france']) # search operator
        except tweepy.TweepError: # disconnection of common errors
            myStream.disconnect()
            print("Sleeping",i,"sec")
            if i > 256:
                i = 1            
            time.sleep(i)
            i = i*2
            continue
        except: # disconnection for other errors
            myStream.disconnect()
            if i > 256:
                i = 1
            print("Sleeping",i,"sec")            
            time.sleep(i)
            i = i*2
            continue


