import streamlit as st
from yt_dlp import YoutubeDL

def download_content(url, download_type, is_playlist=False):
    """
    Download audio or video based on user selection.

    Args:
        url (str): YouTube URL.
        download_type (str): 'mp3' for audio, 'mp4' for video.
        is_playlist (bool): True if the URL is a playlist.

    Returns:
        list: List of downloaded file paths.
    """
    ydl_opts = {
        'format': 'bestaudio/best' if download_type == 'mp3' else 'best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if download_type == 'mp3' else [],
        'outtmpl': '%(title)s.%(ext)s',
    }

    with YoutubeDL(ydl_opts) as ydl:
        if is_playlist:
            info_list = ydl.extract_info(url, download=True)
            downloaded_files = [
                ydl.prepare_filename(entry).replace('.webm', f'.{download_type}')
                for entry in info_list['entries']
            ]
            return downloaded_files
        else:
            info = ydl.extract_info(url, download=True)
            return [ydl.prepare_filename(info).replace('.webm', f'.{download_type}')]

def main():
    st.title("🎵 YouTube to MP3/MP4 Fast 🎬")
    st.write("Download your favorite YouTube videos or playlists as MP3 (audio) or MP4 (video) with ease!")

    # Format selection
    format_option = st.radio(
        "Choose the format you want to download:",
        ("MP3 (Audio)", "MP4 (Video)"),
        horizontal=True
    )
    download_type = 'mp3' if format_option == "MP3 (Audio)" else 'mp4'

    # Video or Playlist selection
    option = st.radio(
        "What would you like to download?",
        ("Single Video", "Playlist"),
        horizontal=True
    )
    is_playlist = (option == "Playlist")

    # URL input
    url = st.text_input("Enter YouTube URL:")

    if st.button("Download"):
        if url.strip() == "":
            st.error("Please enter a valid YouTube URL.")
        else:
            try:
                st.info(f"Downloading... Please wait! {'(Playlist Mode)' if is_playlist else ''}")
                downloaded_files = download_content(url, download_type, is_playlist=is_playlist)

                if is_playlist:
                    st.success(f"Playlist downloaded! Total files: {len(downloaded_files)}")
                    for file_name in downloaded_files:
                        with open(file_name, "rb") as file:
                            st.download_button(
                                label=f"Download {file_name}",
                                data=file,
                                file_name=file_name,
                                mime="audio/mpeg" if download_type == "mp3" else "video/mp4"
                            )
                else:
                    file_name = downloaded_files[0]
                    st.success(f"Video downloaded: {file_name}")
                    with open(file_name, "rb") as file:
                        st.download_button(
                            label="Download",
                            data=file,
                            file_name=file_name,
                            mime="audio/mpeg" if download_type == "mp3" else "video/mp4"
                        )

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
