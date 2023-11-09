import json
import os
import requests

def vectara_api_call(query:str, corpus_id=1) -> dict:
    url = "https://api.vectara.io/v1/query"

    payload = json.dumps({
      "query": [
        {
          "query": query,
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
              "corpusId": corpus_id,
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
    json_response = response.json()
    return response

def vectara_api_call_get_responses(query:str, corpus_id=1) -> dict:
    url = "https://api.vectara.io/v1/query"

    payload = json.dumps({
      "query": [
        {
          "query": query,
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
              "corpusId": corpus_id,
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
    # json_response = response.json()
    json_response = response.json()
    responses = json_response['responseSet'][0]['response']
    return responses

if __name__ == '__main__':
    # response = vectara_api_call(query="what does the universe contain")
    # response = vectara_api_call(query="What is the overall sentiment in the data?")
    responses = vectara_api_call_get_responses(query="What is the overall sentiment in the data?")
    print(responses)
    # print(response.text)