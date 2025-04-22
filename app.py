import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
import speech_recognition as sr
import numpy as np
import tempfile
import json

questions = [
    "What is a Database?",
    "What is SQL?",
    "What are the datatypes?"
]

st.title("🎤 Speech-to-Text Transcription")

class AudioProcessor(AudioProcessorBase):
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.audio_buffer = frame.to_ndarray().flatten()
        return frame

transcriptions = []

for i, question in enumerate(questions, 1):
    st.subheader(f"Question {i}: {question}")
    webrtc_ctx = webrtc_streamer(key=f"audio_{i}", audio_processor_factory=AudioProcessor)

    if st.button(f"Transcribe Answer {i}"):
        if webrtc_ctx and webrtc_ctx.audio_processor:
            # Save audio to temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                audio_array = webrtc_ctx.audio_processor.audio_buffer.astype(np.int16)
                sr.AudioData(audio_array.tobytes(), 16000, 2)
                f.write(audio_array.tobytes())
                audio_path = f.name

            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio_data)
                st.success(f"Transcription: {text}")
                transcriptions.append({"question": question, "transcription": text})
            except Exception as e:
                st.error(f"Transcription failed: {e}")

if len(transcriptions) == len(questions):
    st.success("All answers recorded and transcribed.")
    st.download_button("Download Transcriptions", json.dumps(transcriptions, indent=4), "transcriptions.json", "application/json")
