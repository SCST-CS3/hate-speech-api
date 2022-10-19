from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utility import import_tensorflow

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute"],
    storage_uri="memory://",
)

tf = import_tensorflow()

rnn_model = tf.keras.models.load_model('saved_model/rnn/v1', compile=False)


def is_hate_speech(predictions):
    verdicts = []

    for i in predictions:
        if(i >= 0):
            verdicts.append(1)
        else:
            verdicts.append(0)

    return verdicts


def is_hate_speech_single(prediction):
    return prediction[0] >= 0


@app.route("/single-hate-prediction", methods=['POST'])
@limiter.limit("5 per minute")
def single_hate_prediction():
    data = request.get_json()
    text = data['text']

    if(not text):
        return jsonify(is_hate_speech=f"{False}")

    verdict = is_hate_speech_single(rnn_model.predict([text])[0])

    response = {
        "is_hate_speech": f"{verdict}"
    }

    return jsonify(response)


@app.route('/many-hate-prediction')
@limiter.limit("5 per minute")
def many_hate_prediction():
    data = request.get_json()
    text = data['text']

    verdict = is_hate_speech_single(rnn_model.predict([text])[0])

    response = {
        "is_hate_speech": f"{verdict}"
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run()
