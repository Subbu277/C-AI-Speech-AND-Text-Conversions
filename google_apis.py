import os
from google.cloud import texttospeech
from google.cloud import storage
import json
import vertexai
import base64
from vertexai.generative_models import GenerativeModel, Part
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

prompt = """
Please provide an exact trascript for the audio, followed by sentiment analysis.

Your response should follow the format (json):

Text: USERS SPEECH TRANSCRIPTION

Sentiment Analysis: positive|neutral|negative

Sentiment Score : -1 to 1
"""

google_api_key = os.environ.get('google_api_key')
bucket_name = os.environ.get('BUCKET_NAME')
project_id = os.environ.get('project_id')

vertexai.init(project=project_id, location="us-central1")
model = GenerativeModel("gemini-1.5-flash-001")
client_options = {"api_key": google_api_key}

text_to_audio_client = texttospeech.TextToSpeechClient(client_options=client_options)

def text_to_audio(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code='en-US',name='en-US-Wavenet-C',ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = text_to_audio_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return response

def audio_to_text(audio_file_uri):
   audio_file = Part.from_uri(audio_file_uri, mime_type="audio/wav")
   contents = [audio_file, prompt]
   response = model.generate_content(contents)
   clean_response = response.text.replace('```json', '').replace('```', '').strip()
   json_obj = json.loads(clean_response)
   audio = text_to_audio(json_obj["Text"])
   json_obj["audio"] = base64.b64encode(audio.audio_content).decode("utf-8")
   return json_obj


def bucket_connection(bucket_name):
    storage_client = storage.Client()
    return storage_client.bucket(bucket_name)

bucket_connection = bucket_connection(bucket_name)

def upload_file(file, bucket_object_name):
    blob = bucket_connection.blob(bucket_object_name)
    blob.upload_from_file(file)
    logger.info(f"------------------- File uploaded to path: {blob.path}")
    path = "gs://" + blob.path.replace('/b','')
    logger.info(f"------------------- File uploaded to url: {path}")
    return path
