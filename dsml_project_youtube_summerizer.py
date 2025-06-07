

'''
Important Note:

collab link : 

Before running the code, ensure that your device meets the following requirements:

1)High-End System Requirements: The application utilizes resource-intensive models such as voice-to-text processing, which demand significant computational power.

2)Optimized Performance: For faster and more efficient results, it is highly recommended to use Google Colab or a similar cloud-based environment. These platforms provide access to high-performance GPUs and TPUs, significantly enhancing the execution of heavy models.

Ensure all dependencies are properly installed for optimal functionality.

'''


# libraries

from pytube import YouTube
import os
import google.generativeai as genai
import requests
from pydub import AudioSegment

import yt_dlp
import io
from youtube_transcript_api import YouTubeTranscriptApi

import streamlit as st



# gemini ai part


genai.configure(api_key="AIzaSyCRvKJhg5GDvCboLlwKWGS-1OFDfE874Qo")      #your free gemini api key  

prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing two summaries: one short summary of 100 words and a second long summary of 500 words
including bullet points and a reference link at the end associated with the topic.
Please provide the summary of the text given here:  """




# Functions 










def get_youtube_video_text(video_url):
    """
    Retrieves captions from a YouTube video and returns the combined text.

    Args:
    video_url (str): The URL of the YouTube video.

    Returns:
    str: Combined text from the video captions or an error message.
    """
    try:
        # Extract the video ID from the URL
        video_id = video_url.split("v=")[-1].split("&")[0]

        # Get the transcript for the video
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine the text from the transcript
        combined_text = " ".join([entry['text'] for entry in transcript])

        return combined_text
    except Exception as e:
        return f"An error occurred: {str(e)}"
    




def quetions(text,link):
  try:
    model = model = genai.GenerativeModel("gemini-2.0-flash")

    prompt="this is data and youtube link from which data is extracted . Analys data and youtube link , generate 10 quetions out of it(only write quetions and mentioned related topic) "
    response = model.generate_content(prompt + ", data :"+text+" ,link :"+link)
    return response.text
  except Exception as e:
    return str(e)




def quality_content(text,link):
  try:
    prompt="You have given data and youtube link respectively , analys data and refer youtube link . From analisation and referenced rate this video out off 10 [formate ;(video rating : number)] . write 5 lines separated by bullets points mentioning reason of rating "
    model = model = genai.GenerativeModel("gemini-2.0-flash")

    response = model.generate_content(prompt + ", data :"+text+" ,link :"+link)
    return response.text
  except Exception as e:
        return f"Error: {str(e)}"
  





def related_links(text,link):
  try:
    prompt="you have give youtube link and data abot it , provide atleast 5 different youtube link related to link u had given (links in bullet points)"
    model = model = genai.GenerativeModel("gemini-2.0-flash")

    response = model.generate_content(prompt +" ,link :"+link+" data :"+text)
    return response.text
  except Exception as e:
        return f"Error: {str(e)}"



def generate_gemini_content(transcript_text, prompt):
    model = model = genai.GenerativeModel("gemini-2.0-flash")
  # Or another valid model

    response = model.generate_content(prompt + transcript_text)
    return response.text


# Streamlit application
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    try:
        yt = YouTube(youtube_link)
        video_id = yt.video_id
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    except Exception as e:
        st.error(f"Could not load the video: {str(e)}")

# Option of transcript summary
if st.button("Get Summary from transcript"):
    transcript_text = get_youtube_video_text(youtube_link)
    if transcript_text:
        st.markdown("## Summary from transcript :")
        st.write(generate_gemini_content(transcript_text, prompt))

# option of voice to text summary
# if st.button("Get Summary from voice"):
#     transcript_text = voice_text(youtube_link)
#     if transcript_text:
#         st.markdown("## Summary from  youtube_voice :")
#         st.write(transcript_text)



# Option to generate quetions
if st.button("Get Addition Quetion about this content"):
    transcript_text = quetions(get_youtube_video_text(youtube_link),youtube_link)
    if transcript_text:
        st.markdown("## Detailed Notes (using Gemini):")
        st.write(transcript_text)


# Option to rate quality
if st.button("Get quality content check"):
    transcript_text = quality_content((youtube_link),youtube_link)
    if transcript_text:
        st.markdown("## Detailed Notes (using Gemini):")
        st.write(transcript_text)



# Option to get additional links
# if st.button("Get Addition videos about related to this content"):
#     transcript_text = related_links(get_youtube_video_text(youtube_link),youtube_link)
#     if transcript_text:
#         st.markdown("## Detailed Notes (using Gemini):")
#         st.write(transcript_text)







      