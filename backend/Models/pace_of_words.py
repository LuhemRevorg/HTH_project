import os
import pandas as pd
import librosa
import logging

audio_file_path = "/Users/rhychaw/hackathon/Rhythm/backend/uploads/recording.wav"
audio_id = "speech"
destination = "/Users/rhychaw/hackathon/Rhythm/backend/Models/results"
date = "2024-09-28"

def main_pow():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def read_audio_from_local(audio_file_path):
        try:
            with open(audio_file_path, 'rb') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading audio file: {str(e)}")
            return None

    def analyze_speech_speed(segment_audio):
        zcr = librosa.feature.zero_crossing_rate(segment_audio)
        return zcr.mean()

    def define_pace(zcr):
        if zcr < 0.001:
            return 'very slow'
        elif 0.001 <= zcr < 0.005:
            return 'slow'
        elif 0.005 <= zcr < 0.01:
            return 'medium slow'
        elif 0.01 <= zcr < 0.025:
            return 'medium'
        elif 0.025 <= zcr < 0.035:
            return 'medium fast'
        elif zcr < 0.05:
            return 'fast'
        else:
            return 'very fast'

    def speech_pace_for_transcription_segments(df_transcript, audio_id, destination, audio_file_path, date):
        speech_pace_data = {'start_time': [], 'end_time': [], 'speech_pace': [], 'speaker': [], 'audio_id': [], 'zcr': []}

        # Load the audio directly using librosa
        try:
            audio, sample_rate = librosa.load(audio_file_path, sr=None, mono=True)
        except Exception as e:
            logger.error(f"An error occurred while loading the audio data for audio_id {audio_id}: {str(e)}")
            return

        filtered_df = df_transcript[df_transcript['speaker'] != 'IVR']
        for index, row in filtered_df.iterrows():
            start_time = row['start_time']
            end_time = row['end_time']
            speaker = row['speaker']

            logger.info(f"Processing segment {index}: start_time={start_time}, end_time={end_time}, speaker={speaker}")

            try:
                # Convert times to samples
                start_sample = librosa.time_to_samples(start_time, sr=sample_rate)
                end_sample = librosa.time_to_samples(end_time, sr=sample_rate)
                segment_audio = audio[start_sample:end_sample]

                if len(segment_audio) == 0:
                    logger.warning(f"Segment {index} is empty for audio_id {audio_id}. Skipping this segment.")
                    continue

                segment_audio, _ = librosa.effects.trim(segment_audio)

                if len(segment_audio) == 0:
                    logger.warning(f"Segment {index} is empty after trimming for audio_id {audio_id}. Skipping.")
                    continue

                zcr_segment = analyze_speech_speed(segment_audio)
                pace_segment = define_pace(zcr_segment)

                logger.info(f"Computed ZCR for segment {index}: {zcr_segment}")

                speech_pace_data['start_time'].append(start_time)
                speech_pace_data['end_time'].append(end_time)
                speech_pace_data['speech_pace'].append(pace_segment)
                speech_pace_data['speaker'].append(speaker)
                speech_pace_data['audio_id'].append(audio_id)
                speech_pace_data['zcr'].append(zcr_segment)
            except Exception as e:
                logger.error(f"An error occurred while processing segment {index} for audio_id {audio_id}: {str(e)}")
                continue

        df_result = pd.DataFrame(speech_pace_data)
        df_result = df_result[df_result['speaker'] != 'IVR']

        result_file_path = os.path.join(destination, f"{audio_id}_speech_pace.csv")
        df_result.to_csv(result_file_path, index=False)
        logger.info(f"File successfully saved locally for {audio_id} at {result_file_path}")

    y, sr = librosa.load(audio_file_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    segment_duration = 5
    num_segments = int(duration // segment_duration)

    df_transcript = pd.DataFrame({
        'start_time': [i * segment_duration for i in range(num_segments)],
        'end_time': [(i + 1) * segment_duration for i in range(num_segments)],
        'speaker': ['Speaker 1' if i % 2 == 0 else 'Speaker 2' for i in range(num_segments)]
    })

    if num_segments * segment_duration < duration:
        extra_segment = pd.DataFrame({
            'start_time': [num_segments * segment_duration],
            'end_time': [duration],
            'speaker': ['Speaker 1']
        })
        df_transcript = pd.concat([df_transcript, extra_segment], ignore_index=True)

    os.makedirs(destination, exist_ok=True)
    speech_pace_for_transcription_segments(df_transcript, audio_id, destination, audio_file_path, date)

