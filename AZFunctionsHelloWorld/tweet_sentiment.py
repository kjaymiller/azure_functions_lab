import statistics
from collections import namedtuple
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import tweepy
import os

# Loads Credentials from KeyVault
key_vault_name = os.environ["KEY_VAULT_NAME"]
kv_uri = f"https://{key_vault_name}.vault.azure.net"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=kv_uri, credential=credential)
twitter_bearer = client.get_secret('TWITTERBEARER')

# Setup Tweepy API Client
client = tweepy.Client(bearer_token=twitter_bearer.value)
analyzer = SentimentIntensityAnalyzer()
TweetScore = namedtuple('TweetScore', ['tweet', 'score'])


def get_tweet_sentiment(username:str, max_results=5) -> dict:
    """Retrieves the <max_results> most recent tweets from the user <username> and returns a sentiment analysis of the tweets"""
    user = client.get_user(username=username)
    tweets = client.get_users_tweets(user.data.id, exclude='retweets')
    tweet_scores = [TweetScore(tweet.text, analyzer.polarity_scores(tweet.text)) for tweet in tweets.data]
    most_positive = max(tweet_scores, key=lambda x: x.score['pos'])
    most_negative = max(tweet_scores, key=lambda x: x.score['neg'])
    averate_score = statistics.mean([tweet.score['compound'] for tweet in tweet_scores])
    header = f"Results for {username}:"
    msg = f"""
    {header}
    {"-"*len(header)}
    Average Sentiment Score: {averate_score}
    {most_positive.tweet=} - {most_positive.score['pos']}
    {most_negative.tweet=} - {most_negative.score['neg']}
    """

    return msg


if __name__ == "__main__":
    print(get_tweet_sentiment('kjaymiller'))