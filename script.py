from textblob import TextBlob
import tweepy
from tweepy import OAuthHandler
import re

class TweetAnalyser(object):
    def __init__(self):
        consumer_key = 'xlP48KH0cZCKtU06iHOWnydaE'
        consumer_secret = 'tshtmUYNJjEdDFx33BNSMIG4OfhjUefvdrJTwbcxmP3LUid093'
        access_token = '2931085669-S3u0LoHMQSGsDJfWSmMo0tKES7Hs25fwag08dPq'
        access_token_secret = 'J5UyKE9QlTy22hYVB6qGz1a0qA9hSWwq0UnWdTAxZdKu0'
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Authentication Error. Please check auth creds!!!")
    def preprocess_tweet(self, tweet):
        '''
        Utility function to preprocess/clean tweet text by removing links, special characters using regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
    def analyse_tweet_sentiment(self, tweet):
        '''
        arg(s): Tweet
        function: This function creates the Tweet as TextBlob object which gives the sentiment by using sentiment method
        outuput: 
        '''
        analysis = TextBlob(self.preprocess_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    def get_tweets(self, query, count = 10):
        '''
        Main function for fetching tweets and using the analyse_tweet_sentiment method
        '''
        print("=============================Fetching tweets for: " + query + "=============================")
        print("\n\n")
        tweets = []
        try:
            # Fetch Tweets
            fetched_tweets = self.api.search(q = query, count = count)
 
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.analyse_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
 
        except tweepy.TweepError as e:
            print("Error : " + str(e))


api = TweetAnalyser()
print("Please enter the query you want to be analysed tweets for")
query = str(input())
tweets = api.get_tweets(query, count = 20000)

# Retrieving positive tweets
ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
# Calculating percentage of positive
print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
# Retrieving negative tweets
ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
# Calculating percentage of negative tweets
print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
# Calculating percentage of neutral tweets
temp = len(tweets) - len(ntweets) - len(ptweets)
print("Neutral tweets percentage: {} % ".format(100*(temp/len(tweets))))

# Printing first 5 positive tweets
print("\n\nPositive tweets:")
for tweet in ptweets[:10]:
    print(tweet['text'])

# Printing first 5 negative tweets
print("\n\nNegative tweets:")
for tweet in ntweets[:10]:
    print(tweet['text'])
 
