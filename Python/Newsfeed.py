import feedparser
from dateutil import parser as date_parser
from dateutil.tz import gettz

sources_file = "RSS/Crypto.txt"

def format_date(original_date):
    try:
        date_obj = date_parser.parse(original_date, tzinfos={"EDT": gettz("America/New_York")})
        return date_obj.strftime("%d/%m/%Y")
    except ValueError:
        return "Invalid Date"

# Read RSS feed
with open(sources_file, "r") as file:
    rss_feed_urls = [line.strip() for line in file.readlines()]

# Store RSS outputs
valid_entries = []

# Iterate RSS feed
for rss_feed_url in rss_feed_urls:

    feed = feedparser.parse(rss_feed_url)

    # Validatioin
    if feed.bozo == 0:

        for entry in feed.entries:
            title = entry.get("title", "")
            date = entry.get("published", "")
            link = entry.get("link", "")

            # Exclude missing news subject, date or URL link
            if title and date and link:
                valid_entries.append({
                    "title": title,
                    "date": format_date(date),
                    "link": link
                })

# Sort the news by date
sorted_entries = sorted(valid_entries, key=lambda entry: entry["date"], reverse=True)

# Print entries
for entry in sorted_entries:
    print("Title:", entry["title"])
    print("Date:", entry["date"])
    print("Link:", entry["link"])
    print("")
