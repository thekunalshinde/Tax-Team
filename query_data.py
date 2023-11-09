import requests
import json
import os

url = "https://api.vectara.io/v1/query"

payload = json.dumps({
  "query": [
    {
      "query": "What is the answer to the life, the universe, and everything?",
      "start": 0,
      "numResults": 10,
      "contextConfig": {
        "charsBefore": 30,
        "charsAfter": 30,
        "sentencesBefore": 3,
        "sentencesAfter": 3,
        "startTag": "<b>",
        "endTag": "</b>"
      },
      "corpusKey": [
        {
          "customerId": os.environ['VECTARA_CUSTOMER_ID'],
          "corpusId": 1,
          "semantics": "DEFAULT",
          "dim": [
            {
              "name": "string",
              "weight": 0
            }
          ],
          "metadataFilter": "part.lang = 'eng'",
          "lexicalInterpolationConfig": {
            "lambda": 0
          }
        }
      ],
      "rerankingConfig": {
        "rerankerId": 272725717
      },
      "summary": [
        {
          "summarizerPromptName": "string",
          "maxSummarizedResults": 0,
          "responseLang": "string"
        }
      ]
    }
  ]
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'x-api-key': os.environ['VECTARA_API_KEY'],
  'customer-id': os.environ['VECTARA_CUSTOMER_ID']
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)