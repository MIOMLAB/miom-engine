import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

HISTORY_FILE = "chat_history.json"
PROMPT_FILE = "promt_miom_v5.1.txt"  # Файл с нашим промптом

def load_system_prompt():
    """Читает системный промпт из файла или использует базовый"""
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return """Ты — Мирон, магистр математических наук и элитный спортивный аналитик с 10-летним стажем. 
Ты работаешь по протоколу МИОМ v5.1 «Эра тренерского гения». 
Ты — друг и напарник Дениса. Всегда отвечаешь на русском языке."""

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return [{"role": "system", "content": load_system_prompt()}]

def save_history(messages):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

messages = load_history()

# Если файл с промптом изменился — обновляем системное сообщение
current_prompt = load_system_prompt()
if messages and messages[0]["role"] == "system":
    messages[0]["content"] = current_prompt
else:
    messages.insert(0, {"role": "system", "content": current_prompt})

print(f"🚀 MIOM Engine — Безлимитный штаб активирован.")
print(f"📚 Загружено сообщений: {(len(messages) - 1) // 2}")
print(f"📄 Системный промпт: {PROMPT_FILE} ({len(current_prompt)} символов)")
print("Вводите сообщения (для выхода введите 'exit')\n")

while True:
    user_input = input("Вы: ")
    if user_input.lower() == "exit":
        print("Штаб закрыт. До связи, стратег!")
        break
    
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    print(f"\nМирон: {reply}\n")
    messages.append({"role": "assistant", "content": reply})
    save_history(messages)