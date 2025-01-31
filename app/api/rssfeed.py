import feedparser

def fetch_rss_feed(url):
    feed = feedparser.parse(url)

    # Collect the title and link of each article
    articles = []
    for entry in feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary
        }
        articles.append(article)

    return articles
