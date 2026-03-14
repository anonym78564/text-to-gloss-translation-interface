import os
import json
import requests

def llm_api_call(start:int, end:int):
    TOKEN = os.getenv("ROUTER_AI")
    url = "https://routerai.ru/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + TOKEN
    }
    with open("prompt.txt", "rt", encoding="utf-8") as file:
        SYSTEM_PROMPT = file.read()

    with open("sentences.txt", "rt", encoding="utf-8") as file:
        sentences = file.read().split("\n")[start:end]

    data = {
        "model": "x-ai/grok-4",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT+" ".join(sentences)}
        ]
    }
    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        answer = response.json()["choices"][0]["message"]["content"]
        json_answer = json.loads(answer)
        with open("corpus.json", "at", encoding="utf-8") as file:
            json.dump(json_answer, file, ensure_ascii=False, indent=2)
    else:
        print(f"Ошибка подключения к ROUTER API. Статус: {response.status_code}")