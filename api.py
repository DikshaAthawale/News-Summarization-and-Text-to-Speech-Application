from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
from utils import get_news_links, process_articles, comparative_analysis, hindi_text_to_speech
import os

app = FastAPI()

# ✅ Fetch and process news articles
@app.get("/news/{company}")
async def fetch_news(company: str, max_articles: int = Query(10)):
    """Fetch and process news articles."""
    links = get_news_links(company, max_articles)

    if not links:
        return JSONResponse(content={"error": "No articles found"}, status_code=404)

    # ✅ Concurrently process articles
    articles = process_articles(links)

    if not articles:
        return JSONResponse(content={"error": "Failed to process articles"}, status_code=500)

    # ✅ Comparative analysis
    analysis = comparative_analysis(articles)

    # ✅ Generate Hindi TTS for the combined summary
    combined_text = "\n\n".join([f"{a['Title']} - {a['Summary']}" for a in articles])
    tts_filename = "summary_hindi.mp3"
    hindi_text_to_speech(combined_text, tts_filename)

    # ✅ Prepare output
    results = {
        "articles": articles,   # ✅ Changed key to match Streamlit app
        "analysis": analysis,
        "tts_file": tts_filename if os.path.exists(tts_filename) else None
    }

    return JSONResponse(content=results, status_code=200)


# ✅ Text-to-Speech endpoint (GET request)
@app.get("/tts")
async def tts(text: str = Query(...), filename: str = "custom_tts_hindi.mp3"):
    """Convert text to Hindi speech."""
    output_file = hindi_text_to_speech(text, filename)

    if os.path.exists(output_file):
        return JSONResponse(content={"message": "TTS completed", "audio_file": output_file}, status_code=200)
    else:
        return JSONResponse(content={"error": "TTS failed"}, status_code=500)


# ✅ Download endpoint for audio files
@app.get("/download_audio")
async def download_audio(filename: str = Query("summary_hindi.mp3")):
    """Download the generated TTS audio file."""
    if os.path.exists(filename):
        return FileResponse(filename, media_type="audio/mpeg", filename=filename)
    else:
        return JSONResponse(content={"error": "File not found"}, status_code=404)
