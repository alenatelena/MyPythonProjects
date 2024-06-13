import requests


def api_call(user_text, ctx = None):
    prompt = {
        "modelUri": "gpt://b1gcrohe4sjqleic3h91/yandexgpt",
        "completionOptions": {"stream": False, "temperature": 0.6, "maxTokens": "2000"},
        "messages": [
        #     {
        #         "role": "system",
        #         "text": "Ты ассистент, который создает уточняющие вопросы для нейросетей, ответы на которые помогут пользователю составить промпт."
        #         ,
        #     },
        #          {
        #         "role": "user",
        #         "text": "Привет, ассистент! Мне нужна твоя помощь, составь уточняющие вопросы для покупки телевизора."
        #     },
        #      {
        #     "role": "assistant",
        #     "text": "1. Какой тип телевизора нужен: LED, OLED, QLED или другой?"
        #         "2. Какого размера телевизор нужен: небольшой (диагональ до 40 дюймов), средний (диагональ от 40 до 55 дюймов), большой (диагональ более 55 дюймов)?"
        #         "3. Какой ценовой категории нужен телевизор: бюджетный, средний или премиум-класса?"
        #         "4. Какие дополнительные функции нужны телевизору (Smart TV, 3D, HDR и т.д.)?"
        #         "5. Нужен ли пользователю телевизор с определённой операционной системой (Tizen, Android TV, WebOS и др.)?"
        # },
            
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
    