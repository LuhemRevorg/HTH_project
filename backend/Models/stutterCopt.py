# Use a pipeline as a high-level helper
from transformers import pipeline
import pandas as pd
from pydub import AudioSegment
import os
import ffmpeg

def main_st():
    audio='/Users/rhychaw/hackathon/Rhythm/Models/harvard.wav' 
    #'/Users/rhychaw/hackathon/Rhythm/backend/uploads/recording.wav'
    pipe = pipeline("audio-classification", model="HareemFatima/distilhubert-finetuned-stutterdetection")

    result = pipe('/Users/rhychaw/hackathon/Rhythm/Models/harvard.wav')

    # Replace this with your stuttering detection function
    def stuttering_detection(audio_chunk):
        # Simulated output (replace with your actual function)
        return pipe(audio)

def analyze_audio(file_path):
    # Load audio file
    audio = AudioSegment.from_file(file_path)
    
    # Initialize a list to store results
    results = []
    
    # Split audio into 5-second chunks
    chunk_length = 3000  # 5 seconds in milliseconds
    total_length = len(audio)
    
    for start in range(0, total_length, chunk_length):
        end = min(start + chunk_length, total_length)
        audio_chunk = audio[start:end]
        
        # Run stuttering detection function
        detection_results = stuttering_detection(audio_chunk)
        
        # Extract the relevant label (nonstutter or stutter)
        for result in detection_results:
            if result['label'] == 'nonstutter':
                results.append({'label': 'nonstutter'})
            elif result['label'] in ['repetition', 'prolongation', 'blocks']:
                results.append({'label': 'stutter'})
    
    return results  # Return the results instead of saving to CSV
