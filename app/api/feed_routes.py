from flask import Blueprint,render_template
from .rssfeed import fetch_rss_feed
feed_routes = Blueprint('feed',__name__)

@feed_routes.route('/',methods=['GET'])
def index():
    return 'testing'
