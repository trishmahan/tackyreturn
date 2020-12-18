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
        audio_path = "static/mp3/"
        if result['trait'] == "brave":
            input_text = "Welcome to Gryffindor, " + result['Name']
            file_name = result['Name'].lower() + "-gryf.mp3"
            audio_path = audio_path + file_name
            if path.exists(audio_path):
                return render_template("gryf.html",result = result,audio = audio_path)
            else: 
                audio_path = speak_with_google(input_text, file_name)
                time.sleep(1)
                return render_template("gryf.html",result = result,audio = audio_path)
        elif result['trait'] == "loyal":
            input_text = "Welcome to Hufflepuff, " + result['Name']
            file_name = result['Name'].lower() + "-huff.mp3"
            audio_path = audio_path + file_name
            if path.exists(audio_path):
                return render_template("huff.html",result = result,audio = audio_path)
            else: 
                audio_path = speak_with_google(input_text, file_name)
                time.sleep(1)
                return render_template("huff.html",result = result,audio = audio_path)
        elif result['trait'] == "wise":
            input_text = "Welcome to Ravenclaw, " + result['Name']
            file_name = result['Name'].lower() + "-rav.mp3"
            audio_path = audio_path + file_name
            if path.exists(audio_path):
                return render_template("rav.html",result = result,audio = audio_path)
            else: 
                audio_path = speak_with_google(input_text, file_name)
                time.sleep(1)
                return render_template("rav.html",result = result,audio = audio_path)
        elif result['trait'] == "cunning":
            input_text = "Welcome to Slytherin, " + result['Name']
            file_name = result['Name'].lower() + "-slyth.mp3"
            audio_path = audio_path + file_name
            if path.exists(audio_path):
                return render_template("slyth.html",result = result,audio = audio_path)
            else: 
                audio_path = speak_with_google(input_text, file_name)
                time.sleep(1)
                return render_template("slyth.html",result = result,audio = audio_path)
        else:
            return render_template("home.html",result = result)

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