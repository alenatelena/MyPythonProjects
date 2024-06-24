import requests


def api_call(user_text, ctx = None):
    prompt = {
        "modelUri": "gpt://b1gcrohe4sjqleic3h91/yandexgpt",
        "completionOptions": {"stream": False, "temperature": 0.6, "maxTokens": "2000"},
        "messages": [
            
            {"role": "user", "text": user_text},
        ],
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVN3NprGQm8TkJ2gfsXmTAajEBimfYSFa7q7mMO",
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()
    return result
    