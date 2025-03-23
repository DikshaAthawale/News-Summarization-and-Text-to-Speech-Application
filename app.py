import streamlit as st
import requests
import json

# ✅ Backend URL
API_BASE_URL = "http://127.0.0.1:8000"

st.title("📰 News Summarization & TTS App")

# ✅ Sidebar input for company name and max articles
company = st.sidebar.text_input("Enter Company Name", value="Tesla")
max_articles = st.sidebar.slider("Number of Articles", 1, 20, 10)

# ✅ Fetch News Button
if st.sidebar.button("Fetch News"):
    with st.spinner("Fetching and processing articles..."):
        response = requests.get(f"{API_BASE_URL}/news/{company}?max_articles={max_articles}")

        if response.status_code == 200:
            data = response.json()

            # ✅ Display articles
            st.subheader("📰 Articles Summary")
            for i, article in enumerate(data["articles"], 1):
                st.write(f"### 📰 Article {i}")
                st.write(f"**Title:** {article['Title']}")
                st.write(f"**Link:** [{article['Link']}]({article['Link']})")
                st.write(f"**Summary:** {article['Summary']}")
                st.write(f"**Sentiment:** {article['Sentiment']}")
                st.write(f"**Topics:** {', '.join(article['Topics']) if article['Topics'] else 'No topics'}")
                st.write("---")

            # ✅ Display comparative analysis
            st.subheader("📊 Comparative Analysis")

            sentiment_dist = data["analysis"]["Sentiment Distribution"]
            st.write("### Sentiment Distribution")
            st.bar_chart(sentiment_dist)

            coverage_differences = data["analysis"]["Coverage Differences"]
            st.write("### Coverage Differences")
            for diff in coverage_differences:
                st.write(f"**{diff['Comparison']}**")
                st.write(f"Impact: {diff['Impact']}")
                st.write("---")

            topic_overlap = data["analysis"]["Topic Overlap"]
            st.write("### Topic Overlap")
            st.write(f"**Common Topics:** {', '.join(topic_overlap['Common Topics'])}")
            st.write("### Unique Topics Per Article")
            for idx, topics in enumerate(topic_overlap["Unique Topics per Article"], 1):
                st.write(f"**Article {idx}:** {', '.join(topics) if topics else 'No unique topics'}")

            # ✅ Display and download TTS
            st.subheader("🗣️ Hindi Text-to-Speech (TTS)")
            tts_file = data.get("tts_file")

            if tts_file:
                st.success("✅ Hindi TTS generated successfully!")
                st.audio(tts_file)
                st.download_button(
                    label="Download Hindi Audio",
                    data=requests.get(f"{API_BASE_URL}/download_audio").content,
                    file_name="summary_hindi.mp3",
                    mime="audio/mpeg"
                )
            else:
                st.warning("⚠️ No TTS audio file found.")

        else:
            st.error("❌ Failed to fetch news articles.")

# ✅ TTS Section for custom text
st.sidebar.subheader("🗣️ Custom Hindi Text-to-Speech")
text = st.sidebar.text_area("Enter text for TTS")

if st.sidebar.button("Generate TTS"):
    with st.spinner("Generating Hindi speech..."):
        # ✅ Use GET request for TTS
        tts_response = requests.get(f"{API_BASE_URL}/tts?text={text}")

        if tts_response.status_code == 200:
            audio_file = tts_response.json().get("audio_file")

            if audio_file:
                st.success("✅ TTS generated successfully!")
                st.audio(audio_file)
                st.download_button(
                    label="Download Audio",
                    data=requests.get(f"{API_BASE_URL}/download_audio").content,
                    file_name="custom_tts_hindi.mp3",
                    mime="audio/mpeg"
                )
            else:
                st.warning("⚠️ No TTS audio file generated.")
        else:
            st.error("❌ TTS generation failed.")
