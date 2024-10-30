# Podcast-to-Summary Generator

A simple Streamlit application that allows users to transcribe podcast audio files and generate summaries. Users can either upload an audio file or enter a podcast link to download the audio for transcription.

## Features

- **Audio Upload**: Upload audio files in MP3, WAV, or M4A formats.
- **Podcast Link**: Enter a link to download audio directly from a podcast.
- **Transcription**: Automatically transcribes the audio to text using Google Speech Recognition.
- **Summarization**: Generates an extractive summary of the transcribed text, allowing users to choose the number of sentences and summary style (paragraph or bullet points).
- **Feedback Mechanism**: Users can rate the quality of the transcription and provide additional comments.

## Technologies Used

- [Streamlit](https://streamlit.io/) for the web application framework.
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) for audio transcription.
- [pydub](https://github.com/jiaaro/pydub) for audio file manipulation.
- [spaCy](https://spacy.io/) for natural language processing and text summarization.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading audio from podcasts.

## Installation

To run this project locally, follow these steps:

1. Clone this repository:

   ```bash
   git clone https://github.com/deleonkyle/podcast-to-summary-generator.git
   cd podcast-to-summary-generator
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install streamlit SpeechRecognition pydub spacy yt-dlp
   ```

4. Download the spaCy model:

   ```bash
   python -m spacy download en_core_web_sm
   ```

5. Set the path for FFmpeg if needed (ensure FFmpeg is installed):

   On Windows:
   ```bash
   set PATH=%PATH%;C:\path\to\ffmpeg\bin
   ```

   On macOS/Linux:
   ```bash
   export PATH=$PATH:/path/to/ffmpeg/bin
   ```

## Running the Application

To start the Streamlit application, run:

```bash
streamlit run app.py
```

Open your web browser and go to `http://localhost:8501` to access the application.

## Usage

1. **Select Input Method**: Choose to upload an audio file or enter a podcast link.
2. **Transcription**: Once the audio is uploaded or downloaded, the app will transcribe it automatically.
3. **Summary Generation**: Choose the number of sentences for the summary and select the style (paragraph or bullet points).
4. **Feedback**: Rate the quality of the transcription and provide additional comments.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the contributors of the libraries and frameworks used in this project.
```
