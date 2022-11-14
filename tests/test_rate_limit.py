LIMIT = 100


def test_single_prediction_one_hundred_limit(client):
    for i in range(LIMIT):
        client.post("/single-hate-prediction", json={"text": "Hello"})

    res = client.post("/single-hate-prediction", json={"text": "Hello"})

    assert res.status_code == 429


def test_many_prediction_one_hundred_limit(client):
    for i in range(LIMIT):
        client.post("/many-hate-prediction",
                    json={"texts": ["Hello", "World"]})

    res = client.post("/many-hate-prediction",
                      json={"texts": ["Hello", "World"]})

    assert res.status_code == 429
