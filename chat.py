import asyncio
import logging
from groq import AsyncGroq
import os
from dotenv import load_dotenv
load_dotenv()
# Настройка логирования
logging.basicConfig(level=logging.INFO)

class AIChatBot:
    def __init__(self):
        self.client = AsyncGroq(api_key = os.environ.get("GROQ_API_KEY"))
        self.history = []

    async def get_response(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        try:
            chat_completion = await self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=self.history
            )
            response = chat_completion.choices[0].message.content
            self.history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            logging.error(f"Ошибка API: {e}")
            return "Ошибка при подключении."

async def main():
    bot = AIChatBot()
    print("Бот запущен. Напиши 'стоп' для выхода.")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "стоп": break
        
        response = await bot.get_response(user_input)
        print(f"AI: {response}")

if __name__ == "__main__":
    asyncio.run(main())
