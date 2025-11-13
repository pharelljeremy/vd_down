import streamlit as st
import yt_dlp
import os

# Folder where downloads will be saved on the server
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

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
                    'preferedformat': 'mp4',  # Note: 'preferedformat' typo in yt-dlp docs, but it works
                }],
            }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
        return filename, None
    except Exception as e:
        return None, str(e)

st.title("YouTube Video/Audio Downloader")

url = st.text_input("Enter YouTube Video URL:")

is_audio_only = st.checkbox("Download as MP3 (Audio Only)")

if st.button("Download"):
    if not url.strip():
        st.error("Please enter a valid YouTube URL.")
    else:
        with st.spinner("Downloading..."):
            filepath, error = download_video(url, DOWNLOAD_FOLDER, is_audio_only)
            if error:
                st.error(f"Error: {error}")
            else:
                st.success("Download complete!")
                # Read the file bytes for download button
                with open(filepath, "rb") as f:
                    file_bytes = f.read()
                st.download_button(
                    label="Click to download video/audio file",
                    data=file_bytes,
                    file_name=os.path.basename(filepath),
                    mime="application/octet-stream"
                )


#yeah yeah yeah hey hey bruh wt
