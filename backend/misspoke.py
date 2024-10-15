import os
import csv
import torch
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
import librosa
import sentencepiece

def main_ms(script):
    # Load the pre-trained model and processor
    model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-small-librispeech-asr")
    processor = Speech2TextProcessor.from_pretrained("facebook/s2t-small-librispeech-asr")

    def transcribe_audio(audio_path):
        # Load the audio file using librosa
        audio, sample_rate = librosa.load(audio_path, sr=16000)  # The model expects a 16kHz sample rate

        # Preprocess the audio file into the correct format for the model
        inputs = processor(audio, sampling_rate=sample_rate, return_tensors="pt")

        # Generate the transcription using the model
        generated_ids = model.generate(inputs["input_features"], attention_mask=inputs["attention_mask"])

        # Decode the transcription to get the text
        transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)

        # Return the transcription as a string
        return transcription[0]

    # Example usage:
    audio_file_path = "/Users/rhychaw/hackathon/Rhythm/backend/uploads/recording.wav"  # Replace this with the path to your audio file
    transcription = transcribe_audio(audio_file_path)
    print(transcription)

    # Ensure script is a string
    if isinstance(script, dict):  # If script is a dictionary
        script = script.get('text', '')  # Adjust this key based on your structure
    elif not isinstance(script, str):  # If it's not a string or dict
        script = str(script)

    def compare_strings_and_save_to_csv(str1, str2, filename):
        # Create the 'results' folder if it doesn't exist
        os.makedirs('results', exist_ok=True)

        differences = []
        max_length = max(len(str1), len(str2))
        
        for i in range(max_length):
            char1 = str1[i] if i < len(str1) else ''
            char2 = str2[i] if i < len(str2) else ''

            # Replace empty fields with '0'
            if char1 == '':
                char1 = '0'
            if char2 == '':
                char2 = '0'
            
            if char1 != char2:
                differences.append({'index': i, 'str1Char': char1, 'str2Char': char2})
        
        # Define the full path for the CSV file
        filepath = os.path.join('/Users/rhychaw/hackathon/Rhythm/backend/Models/results', filename)

        # Write differences to a CSV file
        with open(filepath, mode='w', newline='') as csvfile:
            fieldnames = ['index', 'str1Char', 'str2Char']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(differences)

    compare_strings_and_save_to_csv(transcription, script, 'misspoke.csv')

if __name__ == "__main__":
    main_ms()
