import os
from dotenv import load_dotenv

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from Bot.hendlers import router

load_dotenv()

TOKEN = os.getenv('TOKEN')

async def main():
    bot = Bot(token=TOKEN)

    dp = Dispatcher()
    dp.include_router(router)

    #Console log
    logging.basicConfig(level= logging.INFO)

    async def set_commands():
        commands = [BotCommand(command='start', description='Начало работы'),
                    BotCommand(command='help', description='Помощь')]
        await bot.set_my_commands(commands, BotCommandScopeDefault())

    await dp.start_polling(bot)
    await set_commands()

if __name__ == "__main__":
    asyncio.run(main())



