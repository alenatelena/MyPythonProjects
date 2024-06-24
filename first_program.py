import requests

from api import api_call

model_response = ''

def send_prompt_to_nn(textInput):
    global model_response

    pattern_user = f"Выступи в роли генератора подсказок для нейросеии, помогающий оптимизировать промпты пользователя, дополнять его деталями, задавая вопросы, на которые пользователь сможет ответить. Напиши какие вопросы можно задать к промпту: '{textInput}', чтобы дополнить его деталями и сделать более понятными. Верни только список вопросов. \n"
    result = api_call(pattern_user)
    print(result)
    result = result['result']['alternatives'][0]['message']['text'].split('\n')[1:]
    model_response = textInput
    return result


def compile_prompt(questions):
    textInput = '\n'.join([f"{q}: {a}" for q, a in questions.items()])
    pattern_user = f"Пользователь дал ответы на уточняющие вопросы, учитывая его ответы собери их в один правильный промпт: изначальный промпт - f{model_response} \n Вот такие были даны ответы {textInput}. Сделай из этого правильно сформулированный промпт учитывая ответы пользователя.Пиши от первого лица. Ниже добавь объяснение того, как ответы на вопросы повлияли на промпт."
    result = api_call(pattern_user)
    print(result)
    return result['result']['alternatives'][0]['message']['text']