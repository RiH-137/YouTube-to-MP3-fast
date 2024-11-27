import streamlit as st
from yt_dlp import YoutubeDL
import zipfile
import os
import re


def sanitize_filename(filename):
    """
    Sanitize the filename by removing invalid characters.
    Args:
        filename (str): Original filename.
    Returns:
        str: Sanitized filename.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def download_content(url, download_type, is_playlist=False):
    """
    Download audio or video based on user selection.

    Args:
        url (str): YouTube URL.
        download_type (str): 'mp3' for audio, 'mp4' for video.
        is_playlist (bool): True if the URL is a playlist.

    Returns:
        list: List of successfully downloaded file paths.
    """
    ydl_opts = {
        'format': 'bestaudio/best' if download_type == 'mp3' else 'best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if download_type == 'mp3' else [],
        'outtmpl': '%(title)s.%(ext)s',  # Save to current working directory
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        },
    }

    downloaded_files = []

    with YoutubeDL(ydl_opts) as ydl:
        if is_playlist:
            info_list = ydl.extract_info(url, download=False)
            for entry in info_list['entries']:
                try:
                    if entry:  # Check if entry is valid
                        video_url = entry.get('url', None)
                        if not video_url:
                            raise ValueError("Missing video URL in playlist entry.")

                        info = ydl.extract_info(video_url, download=True)
                        downloaded_file = sanitize_filename(ydl.prepare_filename(info)).replace('.webm', f'.{download_type}')
                        downloaded_files.append(downloaded_file)
                        st.success(f"Downloaded: {entry.get('title', 'Unknown Title')}")
                except Exception as e:
                    st.warning(f"Skipping {entry.get('title', 'Unknown Title')} due to error: {e}")
        else:
            info = ydl.extract_info(url, download=True)
            downloaded_file = sanitize_filename(ydl.prepare_filename(info)).replace('.webm', f'.{download_type}')
            downloaded_files.append(downloaded_file)

    return downloaded_files


def create_zip(file_list, zip_name):
    """
    Create a ZIP file containing the provided files.

    Args:
        file_list (list): List of file paths to include in the ZIP.
        zip_name (str): Name of the ZIP file.

    Returns:
        str: Path to the ZIP file.
    """
    zip_path = os.path.join(os.getcwd(), zip_name)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in file_list:
            zipf.write(file, os.path.basename(file))
    return zip_path


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
                with st.spinner("Downloading... Please wait!"):
                    downloaded_files = download_content(url, download_type, is_playlist=is_playlist)

                if is_playlist:
                    if downloaded_files:
                        zip_name = "playlist_download.zip"
                        zip_path = create_zip(downloaded_files, zip_name)

                        st.success(f"Playlist downloaded! Total files: {len(downloaded_files)}")
                        with open(zip_path, "rb") as zipf:
                            st.download_button(
                                label="Download All as ZIP",
                                data=zipf,
                                file_name=zip_name,
                                mime="application/zip"
                            )
                    else:
                        st.warning("No files were successfully downloaded from the playlist.")
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
