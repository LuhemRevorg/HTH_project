from transformers import pipeline
import pandas as pd
from pydub import AudioSegment
import numpy as np

def main_st():
    audio_path = '/Users/rhychaw/hackathon/Rhythm/backend/uploads/recording.wav'
    pipe = pipeline("audio-classification", model="HareemFatima/distilhubert-finetuned-stutterdetection")

    # Simulated output (replace with your actual function)
    def stuttering_detection(audio_chunk):
    # Convert to numpy array and ensure it is float32
        audio_array = np.array(audio_chunk.get_array_of_samples()).astype(np.float32)

        # Save the chunk temporarily if needed for processing
        audio_chunk.export("temp.wav", format="wav")  # Uncomment to export for testing
        return pipe(audio_array)


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
        
        # Create a DataFrame and save to CSV
        df = pd.DataFrame(results)
        df.to_csv('/Users/rhychaw/hackathon/Rhythm/backend/Models/results/stutter.csv', index=False)

    analyze_audio(audio_path)

