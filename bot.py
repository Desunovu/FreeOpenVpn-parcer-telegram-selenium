import logging
from seleniumscript import SeleniumScript

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
script = SeleniumScript()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['vpn'])
async def send_vpn_code(message: types.Message):
    link, captcha = script.start_script()
    message.text = f"Germany\nLink: {link}"
    await message.answer(message.text)
    await message.answer(f"{captcha}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)