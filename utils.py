import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from textblob import TextBlob
from collections import Counter
import os

# ✅ Fetch Articles using Bing RSS Feed
def fetch_articles(company, max_articles=10):
    """Fetch articles using Bing RSS feeds"""
    base_url = f"https://www.bing.com/news/search?q={company}&format=rss"

    try:
        response = requests.get(base_url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")

        articles = []
        for item in items[:max_articles]:
            title = item.title.text
            link = item.link.text
            description = item.description.text

            # ✅ Perform sentiment analysis
            sentiment = TextBlob(description).sentiment.polarity
            if sentiment > 0:
                sentiment_label = "Positive"
            elif sentiment < 0:
                sentiment_label = "Negative"
            else:
                sentiment_label = "Neutral"

            # ✅ Extract noun phrases as topics
            blob = TextBlob(description)
            topics = list(set(blob.noun_phrases))

            articles.append({
                "Title": title,
                "Link": link,
                "Summary": description,
                "Sentiment": sentiment_label,
                "Topics": topics
            })

        return articles

    except Exception as e:
        print(f"⚠️ Error fetching RSS feed: {e}")
        return []


# ✅ Comparative Analysis
def comparative_analysis(articles):
    """Perform comparative analysis on articles"""
    sentiment_distribution = Counter([a['Sentiment'] for a in articles])
    topic_overlap = []

    for i in range(len(articles)):
        for j in range(i + 1, len(articles)):
            common_topics = set(articles[i]["Topics"]) & set(articles[j]["Topics"])
            topic_overlap.append({
                "Comparison": f"{articles[i]['Title']} and {articles[j]['Title']}",
                "Common Topics": list(common_topics),
                "Impact": "Potential market effect due to coverage."
            })

    analysis = {
        "Sentiment Distribution": dict(sentiment_distribution),
        "Coverage Differences": topic_overlap,
        "Topic Overlap": {
            "Common Topics": list(set.intersection(*[set(a['Topics']) for a in articles])),
            "Unique Topics per Article": [
                list(set(a['Topics']) - set.intersection(*[set(b['Topics']) for b in articles if b != a]))
                for a in articles
            ]
        }
    }

    return analysis


# ✅ Hindi Text-to-Speech (TTS)
def hindi_text_to_speech(text, output_folder="output"):
    """Convert Hindi text to speech using gTTS"""
    try:
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, "summary_hindi.mp3")

        # ✅ Generate speech
        tts = gTTS(text=text, lang='hi')
        tts.save(output_file)

        return output_file

    except Exception as e:
        print(f"⚠️ TTS Error: {e}")
        return None
