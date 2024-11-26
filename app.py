import instaloader
import streamlit as st
import requests
import os

def download_instagram_video(post, file_path):
    """
    Download Instagram video from a Post object.

    Args:
        post (instaloader.Post): The Instagram Post object.
        file_path (str): Path to save the video file.

    Returns:
        str: Path to the downloaded video.
    """
    video_url = post.video_url
    response = requests.get(video_url, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return file_path

def extract_audio(video_path, audio_path):
    """
    Convert a video file to an audio file.

    Args:
        video_path (str): Path to the video file.
        audio_path (str): Path to save the audio file.

    Returns:
        str: Path to the extracted audio file.
    """
    os.system(f"ffmpeg -i \"{video_path}\" -q:a 0 -map a \"{audio_path}\" -y")
    return audio_path

def main():
    st.title("📸 Instagram Video & Audio Downloader 🎥")
    st.write("Download videos or extract audio from Instagram posts effortlessly!")

    # Format selection
    format_option = st.radio(
        "Choose the format you want to download:",
        ("MP4 (Video)", "MP3 (Audio)"),
        horizontal=True
    )
    download_type = 'video' if format_option == "MP4 (Video)" else 'audio'

    # URL input for Instagram
    url = st.text_input("Enter Instagram Post URL:")

    if st.button("Download"):
        if not url.strip():
            st.error("Please enter a valid Instagram URL.")
        else:
            try:
                st.info("Processing... Please wait!")
                loader = instaloader.Instaloader(dirname_pattern='downloads', filename_pattern="{shortcode}")
                shortcode = url.split("/")[-2]  # Extract shortcode
                post = instaloader.Post.from_shortcode(loader.context, shortcode)

                video_path = f"downloads/{shortcode}.mp4"
                download_instagram_video(post, video_path)

                if download_type == 'video':
                    st.success("Video is ready for download! 🎉")
                    with open(video_path, "rb") as video_file:
                        st.download_button(
                            label="⬇️ Download Video",
                            data=video_file,
                            file_name=f"{shortcode}.mp4",
                            mime="video/mp4"
                        )
                else:
                    audio_path = f"downloads/{shortcode}.mp3"
                    extract_audio(video_path, audio_path)
                    st.success("Audio is ready for download! 🎉")
                    with open(audio_path, "rb") as audio_file:
                        st.download_button(
                            label="🎵 Download Audio",
                            data=audio_file,
                            file_name=f"{shortcode}.mp3",
                            mime="audio/mpeg"
                        )

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)  # Ensure downloads folder exists
    main()
