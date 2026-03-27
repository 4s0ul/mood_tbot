import asyncio

from aiogram.types import BotCommand

from app.bot import bot, dp
from app.handlers import register_handlers


async def set_commands() -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Start the bot"),
            BotCommand(command="help", description="Show help"),
            BotCommand(command="about", description="About the bot"),
        ]
    )


async def main() -> None:
    register_handlers(dp)
    await set_commands()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
