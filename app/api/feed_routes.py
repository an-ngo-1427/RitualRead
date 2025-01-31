from flask import Blueprint
from .rssfeed import fetch_rss_feed
feed_routes = Blueprint('feed',__name__)

@feed_routes.route('/',methods=['GET'])
def getFeeds():
    articles = fetch_rss_feed('https://programmingdigest.net/newsletters.rss')

    return articles
