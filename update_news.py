import json
import time
import feedparser
from datetime import datetime

# RSS Feeds mapped to your exact frontend categories
FEEDS = {
    "top_stories": ["https://news.google.com/rss/search?q=viral+tiktok+OR+pop+culture+when:1d&hl=en-US&gl=US&ceid=US:en"],
    "us_trending": ["https://news.google.com/rss/search?q=trending+US+when:1d&hl=en-US&gl=US&ceid=US:en"],
    "uk_trending": ["https://news.google.com/rss/search?q=trending+UK+when:1d&hl=en-GB&gl=GB&ceid=GB:en"],
    "tiktok": ["https://news.google.com/rss/search?q=tiktok+trend+when:1d&hl=en-US&gl=US&ceid=US:en"],
    "twitter_x": ["https://news.google.com/rss/search?q=twitter+viral+OR+x+backlash+when:1d&hl=en-US&gl=US&ceid=US:en"],
    "instagram": ["https://news.google.com/rss/search?q=instagram+reels+viral+when:1d&hl=en-US&gl=US&ceid=US:en"],
    "youtube": ["https://news.google.com/rss/search?q=youtube+drama+OR+viral+video+when:1d&hl=en-US&gl=US&ceid=US:en"],
    "celebrity": ["https://news.google.com/rss/search?q=celebrity+drama+OR+scandal+when:1d&hl=en-US&gl=US&ceid=US:en"],
    "memes": ["https://news.google.com/rss/search?q=new+meme+when:1d&hl=en-US&gl=US&ceid=US:en"],
    "music": ["https://news.google.com/rss/search?q=viral+song+OR+tiktok+audio+when:1d&hl=en-US&gl=US&ceid=US:en"],
    "tech_culture": ["https://news.google.com/rss/search?q=internet+culture+OR+generative+ai+viral+when:1d&hl=en-US&gl=US&ceid=US:en"]
}

def fetch_feed_data():
    all_data = {}
    all_news_pool = []
    
    for category, urls in FEEDS.items():
        category_items = []
        for url in urls:
            parsed = feedparser.parse(url)
            for entry in parsed.entries[:15]: # Get top 15 per feed
                # Extract source from Google News format ("Title - Source")
                title_parts = entry.title.rsplit(' - ', 1)
                title = title_parts[0] if len(title_parts) > 1 else entry.title
                source = title_parts[1] if len(title_parts) > 1 else "Web News"
                
                # Convert pubDate to Unix timestamp
                try:
                    dt = datetime(*entry.published_parsed[:6])
                    timestamp = int(dt.timestamp())
                except:
                    timestamp = int(time.time())

                item = {
                    "id": entry.id if 'id' in entry else entry.link,
                    "title": title,
                    "source": source,
                    "link": entry.link,
                    "timestamp": timestamp
                }
                category_items.append(item)
                all_news_pool.append(item)
                
        # Sort category items newest first
        category_items.sort(key=lambda x: x['timestamp'], reverse=True)
        all_data[category] = category_items

    # Generate the 'all' category
    all_news_pool.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Remove duplicates from the 'all' feed
    unique_all = []
    seen_links = set()
    for item in all_news_pool:
        if item['link'] not in seen_links:
            unique_all.append(item)
            seen_links.add(item['link'])
            
    all_data["all"] = unique_all[:50] # Keep top 50 overall

    return all_data

if __name__ == "__main__":
    current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"Fetching viral news at {current_time}...")
    
    news_data = fetch_feed_data()
    
    output = {
        "last_updated": current_time,
        "data": news_data
    }
    
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("news.json generated successfully!")
