import yt_dlp
import streamlit as st
import os
import zipfile

def download_video(video_url, format_type, output_folder):
    """
    Downloads video or audio from YouTube using yt-dlp.

    Args:
        video_url (str): The URL of the YouTube video.
        format_type (str): 'audio' for MP3 or 'video' for MP4.
        output_folder (str): Path to the output folder for downloads.

    Returns:
        str: Path to the downloaded file.
    """
    file_template = f"{output_folder}/%(title)s.{'mp3' if format_type == 'audio' else 'mp4'}"

    ydl_opts = {
        'format': 'bestaudio/best' if format_type == 'audio' else 'best',
        'outtmpl': file_template,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format_type == 'audio' else [],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        downloaded_file = ydl.prepare_filename(info)
        if format_type == 'audio':
            downloaded_file = downloaded_file.replace(".webm", ".mp3").replace(".m4a", ".mp3")
        return downloaded_file

def create_zip(output_folder, zip_file_name):
    """
    Compresses all files in the output folder into a ZIP file.

    Args:
        output_folder (str): Path to the folder containing downloaded files.
        zip_file_name (str): Name of the resulting ZIP file.

    Returns:
        str: Path to the created ZIP file.
    """
    zip_path = f"{output_folder}/{zip_file_name}"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(output_folder):
            for file in files:
                if file.endswith(".mp3") or file.endswith(".mp4"):
                    zipf.write(os.path.join(root, file), arcname=file)
    return zip_path

def main():
    st.title("🎬 YouTube Video & Audio Downloader 📥")
    st.write("Download videos or extract audio from YouTube links effortlessly!")

    # Input field for the YouTube URL
    video_url = st.text_input("Enter YouTube Video URL:")

    # Format selection
    format_type = st.radio(
        "Choose the format you want to download:",
        ("MP4 (Video)", "MP3 (Audio)"),
        horizontal=True
    )
    selected_format = 'video' if format_type == "MP4 (Video)" else 'audio'

    # Prepare output folder
    output_folder = "downloads"
    os.makedirs(output_folder, exist_ok=True)

    if st.button("Download"):
        if not video_url.strip():
            st.error("Please enter a valid YouTube URL.")
        else:
            try:
                st.info("Processing... Please wait!")
                downloaded_file = download_video(video_url, selected_format, output_folder)
                st.success(f"Download ready! 🎉 File: {downloaded_file}")

                # Provide single file download button
                with open(downloaded_file, "rb") as file:
                    st.download_button(
                        label="⬇️ Download File",
                        data=file,
                        file_name=os.path.basename(downloaded_file),
                        mime="audio/mpeg" if selected_format == 'audio' else "video/mp4"
                    )

                # Create ZIP if multiple files exist
                zip_file_name = "downloaded_files.zip"
                zip_path = create_zip(output_folder, zip_file_name)
                with open(zip_path, "rb") as zip_file:
                    st.download_button(
                        label="⬇️ Download All Files as ZIP",
                        data=zip_file,
                        file_name=zip_file_name,
                        mime="application/zip"
                    )

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
