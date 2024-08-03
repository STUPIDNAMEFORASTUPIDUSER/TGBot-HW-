import asyncio
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from handlers import register_handlers
from db import create_table

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

# Регистрация обработчиков
register_handlers(dp)

# Запуск процесса поллинга новых апдейтов
async def main():
    # Запуск создания таблицы БД
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
