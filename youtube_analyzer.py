import os
from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.youtube import YouTubeTools

load_dotenv()

yt = YouTubeTools()

def get_video_info(url: str) -> str:
    """Fetch YouTube video metadata and truncated captions."""
    try:
        data = yt.get_youtube_video_data(url)
        captions = yt.get_youtube_video_captions(url)
        
        if not captions:
            captions = "No captions available for this video."
        elif len(captions) > 16000:
            captions = captions[:16000] + "\n...[Transcript truncated to fit Groq TPM rate limit]"
            
        return f"Metadata:\n{data}\n\nCaptions:\n{captions}"
    except Exception as e:
        return f"Error fetching video info: {str(e)}"

def build_youtube_agent():
    return Agent(
        name="YouTube Agent",
        model=Groq(id="openai/gpt-oss-120b"),
        tools=[get_video_info],
        instructions=dedent("""\
            You are an expert YouTube content analyst with a keen eye for detail! 🎓
            Follow these steps for comprehensive video analysis:
            1. Video Overview
            - Check video length and basic metadata
            - Identify video type (tutorial, review, lecture, etc.)
            - Note the content structure
            2. Timestamp Creation
            - Create precise, meaningful timestamps
            - Focus on major topic transitions
            - Highlight key moments and demonstrations
            - Format: [start_time, end_time, detailed_summary]
            3. Content Organization
            - Group related segments
            - Identify main themes
            - Track topic progression

            Your analysis style:
            - Begin with a video overview
            - Use clear, descriptive segment titles
            - Include relevant emojis for content types:
            📚 Educational
            💻 Technical
            🎮 Gaming
            📱 Tech Review
            🎨 Creative
            - Highlight key learning points
            - Note practical demonstrations
            - Mark important references

            Quality Guidelines:
            - Verify timestamp accuracy
            - Avoid timestamp hallucination
            - Ensure comprehensive coverage
            - Maintain consistent detail level
            - Focus on valuable content markers
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
