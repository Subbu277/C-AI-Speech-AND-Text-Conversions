import time
from flask import request, jsonify, Blueprint, send_from_directory, send_file
from io import BytesIO
import os
from google_apis import text_to_audio,audio_to_text,analyze_sentiment,upload_file,audio_to_text1
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
   local_path = f"{timestamp}_{file.filename}"
   file.save(local_path)
   file.seek(0)
   path=upload_file(file, f"{timestamp}/{local_path}")
   response_json = audio_to_text1(path)
   os.remove(local_path)
   return response_json




@health_api.route('/health', methods=['GET'])
def health():
    time.sleep(5)
    return jsonify({"message": "Server Health : Running"}), 200

@ui_api.route('/')
def index():
    return send_from_directory('templates', 'ui.html')
