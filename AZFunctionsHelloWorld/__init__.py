import logging
import azure.functions as func
from . import tweet_sentiment


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    username = req.params.get('username')
    last = req.params.get('last', 5)
    
    if username:
        return func.HttpResponse(tweet_sentiment.get_tweet_sentiment(username, max_results=last))
    else:
        return func.HttpResponse(
             "Please pass a username on the query string or in the request body",
             status_code=400
        )
