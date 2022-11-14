import pytest
import json
from jsonschema import validate


single_prediction_schema = {
    "type": "object",
    "properties":  {
        "is_hate_speech": {"type": "integer", "enum": [0, 1]}
    },
    "required": ["is_hate_speech"],
    "additionalProperties": False
}


def test_single_prediction(client):
    res = client.post("/single-hate-prediction", json={"text": "Hello"})
    data = res.get_json()

    validate(data, single_prediction_schema)
    assert res.status_code == 200


many_prediction_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties":  {
            "@^\\d$": {
                "type": "object",
                "properties": {
                    "is_hate_speech": {"type": "integer", "enum": [0, 1]},
                    "original": {"type": "string"}
                }
            }
        }
    },
    "additionalProperties": False
}


def test_many_prediction(client):
    request = {"texts": ["Hello", "World"]}
    res = client.post("/many-hate-prediction",
                      json=request)
    data = res.get_json()

    validate(data, many_prediction_schema)
    assert res.status_code == 200
