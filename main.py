import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import spacy
import yt_dlp
import os
from collections import defaultdict

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

def download_audio(link):
    """Download audio from a given podcast link and convert it to .wav format."""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            'verbose': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            return 'downloaded_audio.wav'
    except Exception as e:
        st.error(f"Error downloading audio: {str(e)}")
        return None

def transcribe_audio(file_path):
    """Transcribe audio from a .wav file."""
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        return text
    except Exception as e:
        st.error(f"Error during transcription: {str(e)}")
        return None

def summarize_text(text, num_sentences=3, style="paragraph"):
    """Summarize the given text using extractive summarization."""
    try:
        doc = nlp(text)
        sentences = list(doc.sents)
        word_frequencies = defaultdict(int)

        for token in doc:
            if token.is_alpha:
                word_frequencies[token.text.lower()] += 1

        max_frequency = max(word_frequencies.values(), default=0)

        for word in word_frequencies.keys():
            word_frequencies[word] /= max_frequency

        sentence_scores = defaultdict(int)
        for i, sentence in enumerate(sentences):
            for token in sentence:
                if token.text.lower() in word_frequencies:
                    sentence_scores[i] += word_frequencies[token.text.lower()]

        summarized_sentences_indices = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        summary = ' '.join([str(sentences[i]) for i in sorted(summarized_sentences_indices)])

        # Format summary based on user selection
        if style == "bullet_points":
            summary = "\n- " + "\n- ".join(summary.split('. '))  # Convert to bullet points

        return summary

    except Exception as e:
        st.error(f"Error during summarization: {e}")
        return "Error: Unable to generate summary."

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Podcast-to-Summary Generator", layout="wide")
    st.title("Podcast-to-Summary Generator")
    st.write("Upload your podcast audio file or enter a podcast link to transcribe and generate a summary.")
    
    input_method = st.radio("Select input method:", ("Upload Audio File", "Enter Podcast Link"))

    if input_method == "Upload Audio File":
        audio_file = st.file_uploader("Upload a .wav audio file", type=["wav"])
        
        if audio_file is not None:
            with open("uploaded_audio.wav", "wb") as f:
                f.write(audio_file.getbuffer())
            
            st.audio("uploaded_audio.wav")

            st.write("### Transcription")
            with st.spinner("Transcribing... Please wait."):
                text = transcribe_audio("uploaded_audio.wav")
            
            if text:
                st.text_area("Transcribed Text", text, height=300)

                # Summary settings
                num_sentences = st.slider("Select number of sentences for the summary:", min_value=1, max_value=10, value=3)
                summary_style = st.radio("Select summary style:", ("Paragraph", "Bullet Points"))

                st.write("### Summary Generation")
                with st.spinner("Generating summary... Please wait."):
                    summary = summarize_text(text, num_sentences, style=summary_style.lower())
                st.text_area("Summary", summary, height=150)

                st.download_button("Download Summary", summary, file_name="summary.txt", mime="text/plain")
                
                # Feedback Section
                st.write("### Feedback")
                feedback = st.radio("Rate the quality of transcription:", options=[1, 2, 3, 4, 5])
                st.text_area("Additional comments (optional):", "")
                if st.button("Submit Feedback"):
                    st.success("Thank you for your feedback!")

            os.remove("uploaded_audio.wav")

    elif input_method == "Enter Podcast Link":
        podcast_link = st.text_input("Enter the podcast link:")
        
        if st.button("Download and Transcribe"):
            if podcast_link:
                st.write("### Downloading Audio...")
                with st.spinner("Downloading audio... Please wait."):
                    audio_file_path = download_audio(podcast_link)

                if audio_file_path:
                    st.audio(audio_file_path)

                    st.write("### Transcription")
                    with st.spinner("Transcribing... Please wait."):
                        text = transcribe_audio(audio_file_path)

                    if text:
                        st.text_area("Transcribed Text", text, height=300)

                        # Summary settings
                        num_sentences = st.slider("Select number of sentences for the summary:", min_value=1, max_value=10, value=3)
                        summary_style = st.radio("Select summary style:", ("Paragraph", "Bullet Points"))

                        st.write("### Summary Generation")
                        with st.spinner("Generating summary... Please wait."):
                            summary = summarize_text(text, num_sentences, style=summary_style.lower())
                        st.text_area("Summary", summary, height=150)

                        st.download_button("Download Summary", summary, file_name="summary.txt", mime="text/plain")

                        # Feedback Section
                        st.write("### Feedback")
                        feedback = st.radio("Rate the quality of transcription:", options=[1, 2, 3, 4, 5])
                        st.text_area("Additional comments (optional):", "")
                        if st.button("Submit Feedback"):
                            st.success("Thank you for your feedback!")

                    os.remove(audio_file_path)

    st.sidebar.header("Help")
    st.sidebar.write("### How to Use This App")
    st.sidebar.write(""" 
        1. **Upload Audio File**: Select this option to upload an audio file directly from your device.
        2. **Enter Podcast Link**: You can paste a link to a podcast here, and the app will download the audio for you.
        3. **Transcription**: Once the audio is uploaded or downloaded, the app will transcribe it automatically.
        4. **Summary Generation**: You can choose the number of sentences for the summary and the summarization method (extractive only).
        5. **Feedback**: Please rate the quality of transcription to help us improve the app.
    """)

if __name__ == "__main__":
    main()
