import os
from google.cloud import texttospeech
from google.cloud import speech_v1 as speech

google_api_key = os.environ.get('google_api_key')

client_options = {"api_key": google_api_key}

text_to_audio_client = texttospeech.TextToSpeechClient(client_options=client_options)
audio_to_text_client = speech.SpeechClient(client_options=client_options)

def text_to_audio(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code='en-US',name='en-US-Wavenet-C',ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = text_to_audio_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return response

def audio_to_text(content):
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.MP3, language_code='en-US')
    response = audio_to_text_client.recognize(config=config, audio=audio)
    result_text = ""
    for result in response.results:
        result_text = result_text + result.alternatives[0].transcript
    return result_text
