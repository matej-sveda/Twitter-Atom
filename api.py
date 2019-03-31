from flask import Flask, render_template
from tweepy_func import get_dashboard_tweets
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

# endpoint calling 'get_feed' function, generating the Atom feed
@app.route('/dashboard.xml')
def get_feed():
    user = request.args.get('user', type=str)
