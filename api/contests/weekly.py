import feedparser

def getWeeklyContests() -> dict:
    
    # Fetch RSS feed
    rss = feedparser.parse("https://www.contestcalendar.com/calendar.rss")
    
    # Format data
    return [
        {
            "name": entry["title"], 
            "id": int(entry["id"].split("=")[-1]),
            "summary": entry["summary"]
        }
        for entry in rss["entries"]
    ]