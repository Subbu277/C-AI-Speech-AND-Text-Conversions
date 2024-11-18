import time
from flask import request, jsonify, Blueprint, send_from_directory, send_file
from io import BytesIO
import os
from google_apis import text_to_audio,audio_to_text,analyze_sentiment
from datetime import datetime

texttospeech_api = Blueprint('texttospeech', __name__)
speechtotext_api = Blueprint('speechtotext_api', __name__)
health_api = Blueprint('health', __name__)
ui_api = Blueprint('ui', __name__)

@speechtotext_api.route('/speechtotext', methods=['POST'])
def audiototext_route():
   if 'file' not in request.files:
       return jsonify({'error': 'No file provided'}), 400

   file = request.files['file']

   if file.filename == '':
       return jsonify({'error': 'No selected file'}), 400

   if not (file.filename.lower().endswith('.mp3') or file.filename.lower().endswith('.wav')):
       return jsonify({'error': 'Invalid file type. Only MP3 and WAV files are allowed'}), 400

   if not file or not file.readable():
       return jsonify({'error': 'Invalid file'}), 400

   timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
   local_path = f"temp_{timestamp}_{file.filename}"
   file.save(local_path)
   file.seek(0)
   try:
       upload_file(file, f"{timestamp}/{local_path}")
   except Exception as e:
       os.remove(local_path)
       return jsonify({"error": f"Failed to upload image"}), 500

   audio_content = file.read()
   #text = audio_to_text(audio_content)
   #score = analyze_sentiment(text)
   return jsonify({'transcription': "hello",'sentiment':"123"})




@health_api.route('/health', methods=['GET'])
def health():
    time.sleep(5)
    return jsonify({"message": "Server Health : Running"}), 200

@ui_api.route('/')
def index():
    return send_from_directory('templates', 'ui.html')
