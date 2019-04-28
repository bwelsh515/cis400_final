import twitter
import tweepy
import json
from textblob import TextBlob

CONSUMER_KEY = 'oedakYTzKYx3lFmXiR49mbMH5'
CONSUMER_SECRET = 'SfWHJrMPG3EYk20hbJEDv5rBAr28yCwur8vhyt3WiMDCLeknjB'
OAUTH_TOKEN = '1642025605-JtGSSNpNsOyl599zzC6W2CETx292Ofy5vzF3Oq7'
OAUTH_TOKEN_SECRET = "vQOlN1v5vFt04kMzBZgLeNJZdF8ORHCHC8M7mcwz8maYC"


def oauth_login():
    auth = twitter.oauth.OAuth(
        OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)

keyword = "Duke+Basketball"

tweets = tweepy.Cursor(api.search,
                       q=keyword + " -filter:retweets",
                       since="2019-01-01",
                       #    until="2019-03-01",
                       lang="en",
                       ).items(1)

total_polarity = 0.0
for tweet in tweets:
    favorites_count = tweet.favorite_count
    retweets_count = tweet.retweet_count
    follower_count = tweet.user.followers_count

    print(tweet.text)
    sentiment_of_tweet = TextBlob("         " + tweet.text)
    total_polarity += sentiment_of_tweet.sentiment.polarity
    # print(test.sentiment)

print('Total Polarity: ' + str(total_polarity))
print('Average Polarity: ' + str(total_polarity / 100))
