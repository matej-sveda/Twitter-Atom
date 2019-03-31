from flask import Flask
import tweepy

app = Flask(__name__)

# load config from an object or module (config.py)
app.config.from_object('config')

# config variables from config.py
auth = tweepy.OAuthHandler(app.config['TWITTER_CONSUMER_KEY'],
                           app.config['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(app.config['TWITTER_ACCESS_TOKEN'],
                      app.config['TWITTER_ACCESS_SECRET'])

tweepy_api = tweepy.API(auth)

# function returns a list of 30 most recent tweets on user's dashboard
def get_dashboard_tweets(username):
    dashboard_tweets = []
    tweets = tweepy_api.user_timeline(username, tweet_mode='extended')
    while len(dashboard_tweets) < 30:
        for tweet in tweets:
            # tweets are added to a list only if they are not replies to another tweets
            if tweet.in_reply_to_status_id is None:
                dashboard_tweets.append(tweet)
                id_last = tweet.id
                if len(dashboard_tweets) == 30:
                    return dashboard_tweets

        tweets = tweepy_api.user_timeline(username, tweet_mode='extended', max_id = id_last - 1)

        # in case of dashboard containing less then 30 tweets, this condition controls the end of while-loop
        if dashboard_tweets[len(dashboard_tweets) - 1] == dashboard_tweets[len(dashboard_tweets) - 2]:
            return dashboard_tweets

# function returns up to 10 most recent replies to chosen tweet, problems described in dev_notes.txt file
def get_replies(user, reply_id):
    replies = []
    tweets = (tweepy_api.search(q=user, since_id=reply_id, count=100, tweet_mode='extended'))
    for tweet in tweets:
        if tweet.in_reply_to_status_id == reply_id:
            replies.append(tweet)
            if len(replies) == 10:
                return replies
    return replies


# endpoint calling 'get_feed' function, generating the Atom feed
@app.route('/dashboard.xml')
def get_feed():
    user = request.args.get('user', type=str)

