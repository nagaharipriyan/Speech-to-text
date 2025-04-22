import streamlit as st
import sounddevice as sd
import numpy as np
import soundfile as sf
import speech_recognition as sr
from scipy.io.wavfile import write
import json
import time

# List of questions
# questions = [
#     "What is your name?",
#     "How old are you?",
#     "Where do you live?",
#     "What is your favorite hobby?",
#     "What do you do for a living?"
# ]

questions = [
    "What is a Database",
    "What is SQL",
    "What are the datatypes"
]

# Initialize an empty list to hold the results
transcriptions = []

# Streamlit UI
st.title("Speech-to-Text Transcription for Questions")

# Function to record audio after a delay
def record_audio_with_delay(duration, sample_rate=44100):
    time.sleep(10)  # Wait for 10 seconds before starting the recording
    st.write("🎙 Recording now...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    st.write("✅ Recording finished!")
    return audio

# Loop through the questions
for i, question in enumerate(questions, 1):
    st.subheader(f"Question {i}: {question}")
    
    # Automatically start recording after a 10-second delay
    st.write("🕐 Please wait for 10 seconds before recording...")
    
    # Record the audio after the 10-second wait
    audio = record_audio_with_delay(duration=5)
    
    # Save the audio as a WAV file
    wav_file_path = f'output_{i}.wav'
    write(wav_file_path, 44100, audio)
    st.write(f"💾 Saved as {wav_file_path}")

    # Use SpeechRecognition to transcribe the recorded audio
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)

    try:
        st.write("🔄 Transcribing...")

        # Transcribe audio using Google Web Speech API
        predicted_transcription = recognizer.recognize_google(audio_data)
        st.write(f"**Predicted Transcription for Question {i}:** {predicted_transcription}")

        # Save the question and transcription to the list
        transcriptions.append({"question": question, "transcription": predicted_transcription})

    except Exception as e:
        st.error(f"Error during transcription for Question {i}: {e}")

# Save the transcriptions to a JSON file once all questions are answered
if len(transcriptions) == len(questions):
    with open("transcriptions.json", "w") as f:
        json.dump(transcriptions, f, indent=4)
    st.write("✅ All transcriptions saved to 'transcriptions.json'")
    st.download_button("Download Answers", data=json.dumps(transcriptions), file_name="transcriptions.json", mime="application/json")