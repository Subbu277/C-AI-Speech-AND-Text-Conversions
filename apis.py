import time
from flask import request, jsonify, Blueprint, send_from_directory, send_file
from io import BytesIO
from google_apis import text_to_audio,audio_to_text,analyze_sentiment

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

   audio_content = file.read()
   text = audio_to_text(audio_content)
   score = analyze_sentiment(text)
   return jsonify({'transcription': text,'sentiment':score})




@health_api.route('/health', methods=['GET'])
def health():
    time.sleep(5)
    return jsonify({"message": "Server Health : Running"}), 200

@ui_api.route('/')
def index():
    return send_from_directory('templates', 'ui.html')
