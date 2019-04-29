import twitter
import tweepy
import json
from textblob import TextBlob
import matplotlib.pyplot as plt

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

# Search Query
keyword = "Duke+Basketball"
number_of_tweets = 200

# Get all tweets for that query
tweets = tweepy.Cursor(api.search,
                       q=keyword + " -filter:retweets",
                       since="2019-01-01",
                       #    until="2019-03-01",
                       lang="en",
                       ).items(number_of_tweets)

total_unweighted_polarity = 0.0
total_weighted_polarity = 0.0

# Holds all weighted polarities for each tweet
list_of_weighted_polarities = list()
# Holds subjectivities for each tweet
list_of_subjectivities = list()

# Iterate through all tweets and extract analytical information
for tweet in tweets:
    favorites_count = tweet.favorite_count
    retweets_count = tweet.retweet_count
    followers_count = tweet.user.followers_count

    # Mikes Analytics
    impactOne = favorites_count * retweets_count
    impactTwo = favorites_count * retweets_count * followers_count

    # print(tweet.text)
    sentiment_of_tweet = TextBlob(tweet.text)
    polarity = sentiment_of_tweet.sentiment.polarity
    subjectivity = sentiment_of_tweet.sentiment.subjectivity

    total_unweighted_polarity += polarity
    weighted_polarity = polarity

    # If the user has a low number of followers, lower their weight
    # (This is because they could be a bot, so they should not be able
    # to impact the results as much as a human)
    if (followers_count < 100):
        weighted_polarity = polarity * 0.1

    # Weight the polarity based on subjectivity
    # The more subjective, the higher the weight
    if (subjectivity <= 0.25):
        weighted_polarity = weighted_polarity * 4
    elif (subjectivity <= 0.5):
        weighted_polarity = weighted_polarity * 3
    elif (subjectivity < - 0.75):
        weighted_polarity = weighted_polarity * 2
    else:
        weighted_polarity = weighted_polarity * 1

    total_weighted_polarity += weighted_polarity

    list_of_weighted_polarities.append(weighted_polarity)
    list_of_subjectivities.append(subjectivity)
    list_of_polarities.append(polarity)

# Get averages
average_unweighted_polarity = total_unweighted_polarity / number_of_tweets
average_weighted_polarity = total_weighted_polarity / number_of_tweets

# Print results
print('Total Polarity: ' + str(total_unweighted_polarity))
print('Average Polarity: ' + str(average_unweighted_polarity))
print('Total Weighted Polarity: ' + str(total_weighted_polarity))
print('Average Weighted Polarity: ' + str(average_weighted_polarity))

# Print out all weighted polarities
# stringList = ""
# for wp in list_of_weighted_polarities:
#     stringList += str(wp) + " "
# print("All Weighted Polarities: " + stringList)

# Display scatter plot
plt.figure(1)
plt.plot(list_of_weighted_polarities, 'rx')
plt.axhline(y=average_unweighted_polarity, label='mean')
plt.ylabel('Polarities')
plt.xlabel('Tweets')
plt.legend()
plt.title(str(keyword))

plt.figure(2)
plt.plot(list_of_polarities, list_of_subjectivities, 'rx')
plt.axhline(y=0.5)
plt.axvline(x=0.0)
plt.ylabel('Subjectiveness')
plt.xlabel('Polarity')
plt.legend()
plt.grid(True)
plt.title(str(keyword))

plt.show()
