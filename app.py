import streamlit as st
import yt_dlp
import os

def download_video(url, save_path, is_audio_only):
    try:
        if is_audio_only:
            ydl_opts = {
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'format': 'bestvideo[height<=1440]+bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "Download complete!"
    except Exception as e:
        return f"An error occurred: {e}"

st.title("YouTube Video/Audio Downloader")

url = st.text_input("Enter YouTube Video URL:")

is_audio_only = st.checkbox("Download as MP3 (Audio Only)")

# Streamlit does not have a folder picker, so we use a default folder or ask user to input path
save_path = st.text_input("Enter folder path to save downloads:", value=os.getcwd())

if st.button("Download"):
    if not url.strip():
        st.error("Please enter a valid YouTube URL.")
    elif not os.path.isdir(save_path):
        st.error("Please enter a valid folder path.")
    else:
        with st.spinner("Downloading..."):
            message = download_video(url, save_path, is_audio_only)
            if "complete" in message:
                st.success(message)
            else:
                st.error(message)

