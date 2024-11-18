import os
from google.cloud import texttospeech
from google.cloud import speech_v1 as speech
from google.cloud import language_v1
from google.cloud import storage

google_api_key = os.environ.get('google_api_key')

client_options = {"api_key": google_api_key}

text_to_audio_client = texttospeech.TextToSpeechClient(client_options=client_options)
audio_to_text_client = speech.SpeechClient(client_options=client_options)
sentiment_client = language_v1.LanguageServiceClient(client_options=client_options)

def text_to_audio(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code='en-US',name='en-US-Wavenet-C',ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = text_to_audio_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return response

def audio_to_text(content):
   audio = speech.RecognitionAudio(content=content)
   config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.MP3, sample_rate_hertz=16000,language_code='en-US')
   response = audio_to_text_client.recognize(config=config, audio=audio)
   result_text = ""
   for result in response.results:
       result_text = result_text + result.alternatives[0].transcript
   return result_text


def analyze_sentiment(text):
    document = language_v1.Document(content=text, type=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = sentiment_client.analyze_sentiment(document=document)
    score = round(sentiment.document_sentiment.score, 2)
    label = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
    return score, label

def bucket_connection(bucket_name):
    storage_client = storage.Client()
    return storage_client.bucket(bucket_name)

bucket_name = "cnad_image_and_text_uploads"
bucket_connection = bucket_connection(bucket_name)

def upload_file(file, bucket_object_name):
    blob = bucket_connection.blob(bucket_object_name)
    blob.upload_from_file(file)
    return blob.public_url
