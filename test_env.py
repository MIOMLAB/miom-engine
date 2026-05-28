import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("DEEPSEEK_API_KEY")
if key:
    print(f"Ключ найден: {key[:10]}...{key[-4:]}")
else:
    print("Ключ НЕ найден. Проверь содержимое .env")