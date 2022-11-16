from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_expects_json import expects_json

import os
import json
from utility import import_tensorflow
from dotenv import load_dotenv
load_dotenv()

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT',
                'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per hour"],
    storage_uri="memory://",
)

tf = import_tensorflow()

rnn_model = tf.keras.models.load_model('saved_model/rnn/v1', compile=False)


def is_hate_speech_many(predictions):
    verdicts = []

    for i in predictions:
        if(i >= 0):
            verdicts.append(1)
        else:
            verdicts.append(0)

    return verdicts


def is_hate_speech(prediction):
    return prediction[0] >= 0


def is_text_less_than_hundred_words(text):
    return len(text.split()) <= 100


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=HTTP_METHODS)
def catch_all(path):
    return jsonify({"message": "NOT FOUND"}), 404


single_prediction_schema = {
    "type": "object",
    "properties":  {
        "text": {"type": "string"}
    },
    "required": ["text"],
    "additionalProperties": False
}


@app.route("/single-hate-prediction", methods=['POST'])
@expects_json(single_prediction_schema)
@limiter.limit("100 per minute")
def single_hate_prediction():
    data = request.get_json()
    text = data['text']

    if not is_text_less_than_hundred_words(text):
        return jsonify({"message": "The text property contains more than 100 words."}), 400

    if(not text):
        return jsonify(is_hate_speech=f"{False}")

    verdict = is_hate_speech_many(rnn_model.predict([text])[0])

    return jsonify(is_hate_speech=verdict[0])


many_prediction_schema = {
    "type": "object",
    "properties":  {
        "texts": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": ["texts"],
    "additionalProperties": False
}


@app.route('/many-hate-prediction', methods=['POST'])
@expects_json(many_prediction_schema)
@limiter.limit("100 per minute")
def many_hate_prediction():
    data = request.get_json()

    for i, value in enumerate(data):
        if not is_text_less_than_hundred_words(data["texts"][i]):
            return jsonify({"message": f"The text in index {i} property contains more than 100 words."}), 400

    verdicts = is_hate_speech_many(rnn_model.predict(data['texts']))

    response = []
    for i, value in enumerate(verdicts):
        response.append(
            {f"{i}": {"is_hate_speech": value, f"original": f"{data['texts'][i]}"}})

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
