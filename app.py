import streamlit as st
from yt_dlp import YoutubeDL

def download_audio(url, is_playlist=False):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        if is_playlist:
            info_list = ydl.extract_info(url, download=True)
            downloaded_files = [ydl.prepare_filename(entry).replace('.webm', '.mp3') for entry in info_list['entries']]
            return downloaded_files
        else:
            info = ydl.extract_info(url, download=True)
            return [ydl.prepare_filename(info).replace('.webm', '.mp3')]

def main():
    st.title("🎵 YouTube to MP3 Fast 🎧")
    st.write("Convert your favorite YouTube videos or playlists into MP3s easily!")

    # Choose between Single Video or Playlist
    option = st.radio(
        "What would you like to download?",
        ("Single Video", "Playlist"),
        horizontal=True
    )

    url = st.text_input("Enter YouTube URL:")

    if st.button("Download MP3"):
        if url.strip() == "":
            st.error("Please enter a valid YouTube URL.")
        else:
            try:
                is_playlist = (option == "Playlist")
                st.info(f"Downloading... Please wait! {'(Playlist Mode)' if is_playlist else ''}")
                downloaded_files = download_audio(url, is_playlist=is_playlist)
                
                if is_playlist:
                    st.success(f"Playlist downloaded! Total files: {len(downloaded_files)}")
                    for file_name in downloaded_files:
                        with open(file_name, "rb") as file:
                            st.download_button(
                                label=f"Download {file_name}",
                                data=file,
                                file_name=file_name,
                                mime="audio/mpeg"
                            )
                else:
                    file_name = downloaded_files[0]
                    st.success(f"Video downloaded: {file_name}")
                    with open(file_name, "rb") as file:
                        st.download_button(
                            label="Download MP3",
                            data=file,
                            file_name=file_name,
                            mime="audio/mpeg"
                        )

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
