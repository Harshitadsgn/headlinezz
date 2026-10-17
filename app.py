from flask import Flask, render_template, request
import feedparser

app = Flask(__name__)

FEEDS = {
    "World": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "Technology": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "Business": "https://feeds.bbci.co.uk/news/business/rss.xml",
    "India": "https://www.thehindu.com/news/national/feeder/default.rss",
}

def get_headlines(url):
    feed = feedparser.parse(url)
    return [
        {
            "title": e.title,
            "link": e.link,
            "published": e.get("published", ""),
            "summary": e.get("summary", ""),
        }
        for e in feed.entries
    ]

@app.route("/")
def home():
    category = request.args.get("cat", "World")
    if category not in FEEDS:
        category = "World"

    keyword = request.args.get("q", "").strip().lower()

    headlines = get_headlines(FEEDS[category])
    if keyword:
        headlines = [h for h in headlines if keyword in h["title"].lower()]

    return render_template(
        "index.html",
        headlines=headlines,
        categories=FEEDS.keys(),
        current=category,
        keyword=keyword,
    )

if __name__ == "__main__":
        app.run(debug=True, port=8000)