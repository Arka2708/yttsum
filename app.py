import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Make it brief and crisp and to the point. Please provide the summary of the text given here:  """


# getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Transcript Summarizer")
youtube_link = st.text_input("Enter YouTube Video Link:")
transcript_text=""
summary=""
if youtube_link:
    video_id = youtube_link.split("=")[1].split("&")[0]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    if st.button("Get Detailed Summary") or 'summary' not in st.session_state:
        transcript_text=extract_transcript_details(youtube_link)
        if transcript_text:
            summary=generate_gemini_content(transcript_text,prompt)
            st.session_state['summary'] = summary
    
if 'summary' in st.session_state:
    st.markdown("##SUMMARY:")
    st.write(st.session_state['summary'])
    user_prompt = st.text_input("Enter your question about the video: ")
    if user_prompt:
        # Generate content based on the user's prompt and the initial transcript
        detailed_content = generate_gemini_content(summary, user_prompt)
        st.markdown("## Detailed Answer on Your prompt:")
        st.write(detailed_content)
    




