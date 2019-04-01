from flask import Flask, request, jsonify
import tweepy
from werkzeug.contrib.atom import AtomFeed

app = Flask(__name__)

# load config from an object or module (config.py)
app.config.from_object('config')

# config variables from config.py
auth = tweepy.OAuthHandler(app.config['TWITTER_CONSUMER_KEY'],
                           app.config['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(app.config['TWITTER_ACCESS_TOKEN'],
                      app.config['TWITTER_ACCESS_SECRET'])

tweepy_api = tweepy.API(auth)

# function returns a list of 30 most recent tweets on user's dashboard, doesn't work for tweets with less than 30 tweets,
# this problem is described in dev_notes.txt file
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
def feeds():
    error = {"Error": "Somenthing went wrong, check your input."}

    try:
        user = request.args.get('user', type=str)
        feed = AtomFeed(title="Last 30 tweets from {} dashboard".format(user),
                        feed_url='https://twitter.com/{}'.format(user), url='https://twitter.com')

        # Sort post by created date
        tweets = get_dashboard_tweets(user)

        for tweet in tweets:
            feed.add("TWEET", tweet.full_text,
                     content_type='html',
                     author= tweet.user.name,
                     url='https://twitter.com/{}/status/{}'.format(tweet.user.screen_name, tweet.id),
                     updated=tweet.created_at
                    )

        return feed.get_response(), 200
    
    except:
        return jsonify(error), 404
