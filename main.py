from flask import Flask
from apis import texttospeech_api,speechtotext_api,ui_api,health_api

app = Flask(__name__)

app.register_blueprint(texttospeech_api)
app.register_blueprint(speechtotext_api)
app.register_blueprint(health_api)
app.register_blueprint(ui_api)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
