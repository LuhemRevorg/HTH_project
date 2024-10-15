from flask import Flask, request, jsonify, send_from_directory
import os
from flask_cors import CORS, cross_origin
import pandas as pd
from Models.timestamps import main_ts
from Models.pace_of_words import main_pow
from Models.stutter import main_st
from misspoke import main_ms

app = Flask(__name__)
# Allow requests from your React app's origin
CORS(app)

# Create an uploads directory if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Sample comments data
comments = [
    {"timestamp": "00:01", "text": "Good job! You spoke clearly."},
    {"timestamp": "00:10", "text": "You were a bit fast on this part."},
    {"timestamp": "00:20", "text": "Excellent pace!"}
]

# Global variable to store the script and audio filename
script = ""
audio_filename = ""

# Define result file paths
result_directory = '/Users/rhychaw/hackathon/Rhythm/backend/Models/results/'
result_files = {
    'pitch': os.path.join(result_directory, 'common_entries.csv'),
    'misspoke': os.path.join(result_directory, 'misspoke.csv'),
    'pace': os.path.join(result_directory, 'speech_speech_pace.csv'),
    'stutter': os.path.join(result_directory, 'speech_speech_pace.csv'),
}

@app.route('/')
def hello():
    return 'Hello, This is Rhythm!'

@app.route('/predict', methods=['POST'])
@cross_origin(origins='*')
def predict():
    global script, audio_filename  # Declare the global variable
    if 'audio' not in request.files or 'script' not in request.form:
        return jsonify({'error': 'No audio file or script provided'}), 400

    audio_file = request.files['audio']
    script = request.form['script']  # Store the script in the global variable
    audio_filename = audio_file.filename  # Store the audio filename

    # Save the audio file
    audio_path = os.path.join('uploads', audio_filename)
    audio_file.save(audio_path)

    # Process the results by calling your models
    main_ts()
    #main_ms(script)
    main_pow()
    main_st()

    # Return response with file paths to the results
    result = {
        'message': f'WAV file "{audio_filename}" received successfully!',
        'script': f'Script received: {script}',
        'result_pitch': result_files['pitch'],
        'result_misspoke': result_files['misspoke'],
        'result_pace': result_files['pace'],
        'result_stutter': result_files['stutter'],
    }

    return jsonify(result)

@app.route('/get-comments', methods=['GET'])
def get_comments():
    print("Received a request for comments.")
    audio_url = f'http://localhost:8080/uploads/{audio_filename}' if audio_filename else None

    pace_csv = ""
    feedback = ""
    misspoken_feedback = ""
    pitch_deviations = []

    # Path to the pace CSV
    csv_file_path = result_files['pace']
    if not os.path.exists(csv_file_path):
        print(f"CSV file does not exist at: {csv_file_path}")
        return jsonify({"error": "CSV file not found"}), 404

    try:
        print(f"Trying to read the CSV file at: {csv_file_path}")
        # Read the pace CSV
        df_pace = pd.read_csv(csv_file_path)
        pace_csv = df_pace.to_csv(index=False)
        print("Pace CSV content read successfully.")

        # Stutter logic
        stutter_csv_path = result_files['stutter']  # Assuming you have a separate CSV for stuttering
        if not os.path.exists(stutter_csv_path):
            print(f"Stutter CSV file does not exist at: {stutter_csv_path}")
            return jsonify({"error": "Stutter CSV file not found"}), 404

        # Read the stutter CSV
        df_stutter = pd.read_csv(stutter_csv_path, header=None, names=['label'])
        print("Stutter DataFrame content:\n", df_stutter.head())  # Print the first few rows of the DataFrame

        # Count occurrences of 'stutter' and 'nonstutter'
        stutter_count = df_stutter['label'].value_counts().get('stutter', 0)
        nonstutter_count = df_stutter['label'].value_counts().get('nonstutter', 0)

        # Prepare feedback based on counts
        if stutter_count > nonstutter_count:
            feedback = "You stuttered a lot throughout the speech. Work on that."
        else:
            feedback = "You stuttered very little, that's a strong suit!"

        # Misspoken words logic
        misspoken_csv_path = result_files['misspoke']  # Assuming you have a separate CSV for misspoken words
        if not os.path.exists(misspoken_csv_path):
            print(f"Misspoken CSV file does not exist at: {misspoken_csv_path}")
            return jsonify({"error": "Misspoken CSV file not found"}), 404

        # Read the misspoken CSV
        df_misspoken = pd.read_csv(misspoken_csv_path)
        print("Misspoken DataFrame content:\n", df_misspoken.head())  # Print the first few rows of the DataFrame

        # Check if misspoken words are present
        if df_misspoken.empty:
            misspoken_feedback = "Great! You did not misspell a single word."
        else:
            # Count the occurrences of each misspoken word
            misspoken_counts = df_misspoken['str1Char'].value_counts()
            misspoken_feedback = misspoken_counts.to_dict()  # Convert to dictionary for easy access

        # Analyzing the common_entries CSV for pitch deviations
        common_entries_csv_path = result_files['pitch']  # Path to your common_entries CSV
        if not os.path.exists(common_entries_csv_path):
            print(f"Common entries CSV file does not exist at: {common_entries_csv_path}")
            return jsonify({"error": "Common entries CSV file not found"}), 404

        # Read the common entries CSV
        df_common = pd.read_csv(common_entries_csv_path)
        print("Common entries DataFrame content:\n", df_common.head())  # Print the first few rows

        # Calculate mean and standard deviation of pitch values
        mean_pitch = df_common['DataDict Value'].mean()
        std_dev_pitch = df_common['DataDict Value'].std()

        # Determine upper and lower thresholds
        threshold_upper = mean_pitch + std_dev_pitch
        threshold_lower = mean_pitch - std_dev_pitch

        deviating_words = df_common[
            (df_common['DataDict Value'] > threshold_upper) | 
            (df_common['DataDict Value'] < threshold_lower)
        ]

        # Prepare a list of deviating words with their timestamps and thresholds
        for index, row in deviating_words.iterrows():
            deviation_info = {
                "Word": row['Word'],
                "DataDict Value": row['DataDict Value'],
                "Start": row['Start'],
                "Deviation": "Upper Threshold" if row['DataDict Value'] > threshold_upper else "Lower Threshold"
            }
            pitch_deviations.append(deviation_info)
            
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        return jsonify({"error": str(e)}), 500

    print("Sending comments and CSV content.")
    return jsonify({
        "comments": comments,
        "script": script,
        "audio": audio_url,
        "pace_csv": pace_csv,
        "stutter": feedback,  # Send feedback about stuttering
        "misspoken_feedback": misspoken_feedback,  # Send feedback about misspoken words
        "pitch_deviations": pitch_deviations  # Send pitch deviation results
    })


@app.route('/uploads/<path:filename>', methods=['GET'])
def send_audio(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
