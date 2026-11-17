import streamlit as st
from youtube_analyzer import build_youtube_agent

st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="🎥",
    layout="centered"
)

st.title("🎥 AI YouTube Video Analyzer")
st.write("Paste a YouTube link below to get a structured breakdown, timestamps, and key takeaways.")

@st.cache_resource
def get_agent():
    return build_youtube_agent()

agent = get_agent()

video_url = st.text_input("Enter YouTube Video Link", placeholder="https://youtube.com...")
button = st.button("Analyze Video", type="primary")

if button:
    if not video_url.strip():
        st.warning("Please enter a valid YouTube URL first.")
    else:
        with st.spinner("Fetching transcript and analyzing video..."):
            try:
                response = agent.run(f"Analyze this video: {video_url.strip()}")
                st.divider()
                st.subheader("Analysis Report")
                st.markdown(response.content)
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
