import streamlit as st
from yt_dlp import YoutubeDL
import os

# Function to download MP3
def download_mp3(link):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            file_name = ydl.prepare_filename(info_dict).replace(".webm", ".mp3").replace(".m4a", ".mp3")
        return file_name, info_dict.get('title', 'Unknown Title')
    except Exception as e:
        return None, f"Error: {str(e)}"

# Streamlit app
def main():
    st.set_page_config(page_title="YouTube to MP3 Fast 🎵", page_icon="🎧")

    st.title("🎧 YouTube to MP3 Fast 🎵")
    st.write("Convert YouTube videos to MP3 quickly and easily! Paste a video link below to get started.")

    # Input field for YouTube link
    link = st.text_input("📋 Paste YouTube Video Link:", "")
    
    if st.button("🚀 Convert to MP3"):
        if link.strip():
            with st.spinner("Processing your request... ⏳"):
                file_path, message = download_mp3(link)
                if file_path:
                    st.success(f"✅ MP3 conversion complete: {message}")
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label="🎵 Download MP3",
                            data=file,
                            file_name=os.path.basename(file_path),
                            mime="audio/mpeg",
                        )
                else:
                    st.error(message)
        else:
            st.error("❌ Please provide a valid YouTube link.")

if __name__ == "__main__":
    # Ensure the downloads folder exists
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    main()
