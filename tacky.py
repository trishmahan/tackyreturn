from flask import Flask, render_template, request
from google.cloud import texttospeech
import os
from os import path
import time
from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
load_dotenv()
google_env = os.getenv("GOOGLE")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_env

app = Flask(__name__)
@app.route('/')
def tacky_form():
    return render_template('form.html')

@app.route('/home',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        input_start = ""
        file_end = ""
        template = ""
        if result['trait'] == 'brave':
            input_start = "Welcome to Gryffindor, "
            file_end = "-gryf.mp3"
            template = "gryf.html"
        elif result['trait'] == 'wise':
            input_start = "Welcome to Ravenclaw, "
            file_end = "-rav.mp3"
            template = "rav.html"
        elif result['trait'] == 'loyal':
            input_start = "Welcome to Hufflepuff, "
            file_end = "-huff.mp3"
            template = "huff.html"
        elif result['trait'] == 'cunning':
            input_start = "Welcome to Slytherin, "
            file_end = "-slyth.mp3"
            template = "slyth.html"
        else:
            input_start = "Welcome to Hogwarts"
            file_end = "-hoggy.mp3"
            template = "home.html"
        file_name = result['Name'].lower() + file_end
        audio_path = "static/mp3/" + file_name
        input_text = input_start + result['Name']
        if path.exists(audio_path):
            return render_template(template,result = result,audio = audio_path)
        else: 
            audio_path = speak_with_google(input_text, file_name)
            time.sleep(1)
            return render_template(template,result = result,audio = audio_path)

# Instantiates a TTS client
speech_client = texttospeech.TextToSpeechClient()

def speak_with_google(input_text, file_name):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=input_text)
    # Build the voice request, select the language code ("en-US") and the ssml
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB", name="en-GB-Wavenet-D"#, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = speech_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    # The response's audio_content is binary.
    path = "static/mp3/" + file_name
    with open(path, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
    return path

### WORKING

if __name__ == '__main__':
    app.run(debug = True)