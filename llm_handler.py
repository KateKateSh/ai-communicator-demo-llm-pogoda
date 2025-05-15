import requests
import streamlit as st

HF_TOKEN = st.secrets["HF_TOKEN"]

def query_huggingface(event, model="HuggingFaceH4/zephyr-7b-beta"):
    prompt = f"""
Ты — AI-коммуникатор спроса. Не объясняй, кто ты. Сразу анализируй событие и выдай только деловые рекомендации.

📋 Используй только действия из этого списка:
- Увеличить складские запасы
- Расширить зону доставки
- Увеличить число курьеров
- Настроить push-уведомление
- Изменить витрину в приложении
- Уведомить партнёров
- Добавить товар в “быструю доставку”
- Обновить рекомендации в главной ленте

❌ Не придумывай действия, которых нет в реальных цифровых или логистических процессах e-commerce и доставки.

Формат ответа:
📌 Прогноз: ...
✅ Действия:
- ...
- ...
👥 Роли:
- ...
🧠 Почему:
...

Пример:

Событие: "14 февраля, День всех влюблённых, снег в Москве"

📌 Прогноз: ожидается рост спроса на цветы, подарки, доставку еды. Из-за снегопада возможны задержки курьеров.
✅ Действия:
- Увеличить складские запасы подарков
- Увеличить число курьеров в центре Москвы
- Настроить push-уведомление с предложением подарков
- Изменить витрину в приложении под вечерние предложения

👥 Роли:
- Логистика
- Склад
- Маркетинг

🧠 Почему:
Снег + праздник создают пиковый спрос и логистические риски. Нужно подготовиться заранее.

[СТОП ПРИМЕР]

Событие: {event}
Ответ:
"""

    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.6,
            "top_p": 0.85
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return clean_response(result[0]["generated_text"])
        return "[⚠️ Ответ не содержит текста]"
    except Exception as e:
        return f"[❌ Ошибка LLM: {str(e)}]"

def clean_response(raw_text):
    if "[СТОП ПРИМЕР]" in raw_text:
        raw_text = raw_text.split("[СТОП ПРИМЕР]")[-1]
    start = raw_text.find("📌 Прогноз:")
    return raw_text[start:].strip() if start != -1 else raw_text.strip()
