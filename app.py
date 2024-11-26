import streamlit as st
from yt_dlp import YoutubeDL

# Function to download MP3 from YouTube
def download_mp3(link, is_playlist):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        # Use yt-dlp to handle downloading
        with YoutubeDL(ydl_opts) as ydl:
            if is_playlist:
                ydl.download([link])  # Downloads entire playlist
            else:
                ydl.download([link])  # Downloads single video

        return "🎉 Download complete! Check the 'downloads' folder."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Streamlit app
def main():
    # App Title with Emojis
    st.title("🎵 YouTube to MP3 Fast 🎧")
    st.subheader("🚀 Convert your favorite YouTube videos or playlists to MP3 in just a few clicks!")

    # Instructions
    st.markdown(
        """
        - Paste the **YouTube link** below (video or playlist).
        - Click **Download MP3** and let the magic happen! 🪄
        """
    )

    # User inputs
    link = st.text_input("🎥 Enter YouTube link:", "")
    is_playlist = st.radio("Is this a Playlist or a Single Video? 🤔", ("Single Video", "Playlist"))

    # Download button
    if st.button("🎵 Download MP3"):
        if link.strip():
            message = download_mp3(link, is_playlist == "Playlist")
            st.success(message)
        else:
            st.error("🚨 Please provide a valid YouTube link.")

    # Footer
    st.markdown(
        """
        ---
        Thanks to me... Rishi Ranjan 🤖
        Made with ❤️ using [Streamlit](https://streamlit.io) and [yt-dlp](https://github.com/yt-dlp/yt-dlp).
        """
    )

if __name__ == "__main__":
    main()
