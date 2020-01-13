import requests
import base64
import settings
import tweepy
import re
from textblob import TextBlob
from wordcloud import WordCloud

import matplotlib.pyplot as plt

class TwitterApi():

    #gets the access_token to make API requests.
    def get_access_token(self):
        '''
        Utility function to get the access token using the consumer API key and secret.
        '''
        key_secret = '{}:{}'.format(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET).encode('ascii')
        b64_encoded_key = base64.b64encode(key_secret)
        b64_encoded_key = b64_encoded_key.decode('ascii')
        auth_headers = {
            'Authorization': 'Basic {}'.format(b64_encoded_key),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

        auth_data = {
            'grant_type': 'client_credentials'
        }

        auth_resp = requests.post(settings.AUTH_URL, headers=auth_headers, data=auth_data)

        if auth_resp.status_code == 200:
            
            access_token = auth_resp.json()['access_token']
        else:

            access_token = None

        return access_token

    def search_for_tweets_by_handle(self, handle, count = 15):
        '''
        Utility function to query for tweets by count and @handle - handle can actually just be a whole query...
        '''
        access_token = self.get_access_token()
        if not access_token:

            return {}

        search_headers = {
            'Authorization': 'Bearer {}'.format(access_token)    
        }

        search_params = {
            'q': handle,
            'result_type': 'recent',
            'count': count
        }

        

        search_resp = requests.get(settings.SEARCH_URL, headers=search_headers, params=search_params)

        if search_resp.status_code == 200:

            return search_resp.json()

        return {}

    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
    
    
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'


    def get_tweets(self, handle): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
        all_text = ''
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.search_for_tweets_by_handle(handle)['statuses']
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet['text']
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet['text']) 
  
                # appending parsed tweet to tweets list 
                if  tweet['retweet_count'] > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet)
                else: 
                    tweets.append(parsed_tweet) 
                all_text += self.clean_tweet(tweet['text'])
            
            # return parsed tweets 
            return tweets, all_text
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
    
    
    def generate_word_cloud(self, all_text):
        '''
        Generates a word cloud based off the given text, ideally the text should be cleaned first.
        '''
        wordcloud = WordCloud(width=800, height=500,
                      random_state=21, max_font_size=110).generate(all_text)
        plt.figure(figsize=(20, 20))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis('off')
        plt.show()


twitter = TwitterApi()

tweets, all_text = twitter.get_tweets('@realDonaldTrump')

twitter.generate_word_cloud(all_text)
