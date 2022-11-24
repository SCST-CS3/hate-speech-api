# Filipino Hate Speech API

### Endpoints

**POST | Single Hate Prediction - /single-hate-prediction**
Name | Description | Type
---|---|---
text | The text that would be classified as Hate Speech | String
---|---|---
Rate Limit - 100 Request per minute | Does not accept additional properties
Sample Request

```json
{
  "text": "Lorem Ipsum"
}
```

Sample Response

```json
{
  "is-hate": 0
}
```

**POST | Many Hate Prediction - /many-hate-prediction**
Name | Description | Type
---|---|---
texts | An array of text to be classified as Hate Speech | Array
---|---|---
Rate Limit - 100 Request per minute | Does not accept additional properties

Sample Request

```json
{
  "texts": ["Lorem", "Ipsum", "Lorem", "Ipsum"]
}
```

Sample Response

```json
{
  [
  {
    "0": {
      "is_hate": "0",
      "original": "Lorem"
    }
  },
  {
    "1": {
      "is_hate": "0",
      "original": "Ipsum"
    }
  },
  {
    "2": {
      "is_hate": "0",
      "original": "Lorem"
    }
  },
  {
    "3": {
      "is_hate": "0",
      "original": "Ipsum"
    }
  }
]
}
```
