import streamlit as st
from llm_handler import query_huggingface

# Настройка страницы
st.set_page_config(page_title="AI-коммуникатор спроса", page_icon="🤖🌧️")
st.title("🤖🌧️ AI-коммуникатор спроса (тест погоды)")
st.caption("LLM-помощник для событийного прогнозирования спроса в логистике и маркетинге")

# Инпут от пользователя
user_input = st.text_input(
    "Введите событие для анализа",
    placeholder="Например: Концерт Imagine Dragons в Лужниках + жара"
)

# Кнопка генерации
if st.button("Сгенерировать рекомендации") and user_input:
    with st.spinner("⏳ Анализируем событие..."):
        output = query_huggingface(user_input)
    
    # Вывод в формате markdown
    st.markdown("### 📌 Ответ от AI:")
    st.markdown(output)

# Подвал
st.markdown("---")
st.caption("v1.1 · Демонстрация AI-решения на основе Hugging Face · by Kate")
