from api import *

def test_get_dashboard_tweets():
    assert len(get_dashboard_tweets('TalkPython')) == 30