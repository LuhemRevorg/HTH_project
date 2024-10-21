<b>RHYTHM</b> <br>
This application takes in a user's voice input, processes it through six machine learning models, and provides insightful feedback on various aspects of the speech. From stuttering detection to pitch analysis, the application is designed to enhance the quality of speech and return an improved version using text-to-speech (TTS) APIs.
<br>
<b>Features</b> <br>
  Stuttering Detection: Powered by Meta’s Wav2Vec2 model and Apple's SEP-28K dataset to identify stuttering patterns in the user's speech. <br>
  Misspoken Word Detection: Uses Google’s SpeechRecognition alongside a custom algorithm to detect any incorrectly spoken words. <br>
  Pitch Analysis and Improvement: Utilizes OpenAI API, alongside librosa and Scipy libraries, to analyze the pitch of the user's speech and suggest improvements. <br>
  Custom Speech Output: Generates an improved version of the speech using 11elevenlab’s API and OpenAI’s API with custom SSML (Speech Synthesis Markup Language) for refined speech delivery. <br>
<b>Models and Tools</b> <br>
  Stuttering Detection:<br> 
    Model: Meta’s Wav2Vec2.<br>
    Dataset: Apple’s SEP-28K.<br>
  Misspoken Word Detection:<br>
    Google’s SpeechRecognition.<br>
    Custom detection algorithm.<br>
  Pitch Analysis & Improvement:<br>
    OpenAI API for generating improvements.<br>
Libraries: librosa and Scipy for detailed pitch analysis. <br>
Speech Output: <br>
  11elevenlab’s API for natural-sounding speech synthesis. <br>
  OpenAI’s API using custom SSML to refine and improve the speech output. <br>
