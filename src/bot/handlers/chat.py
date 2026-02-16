from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from src.ai_engine.assistant import SQLAssistant

router = Router()

# Инициализируем ассистента (лучше это делать выше, но для примера сойдет)
assistant = SQLAssistant()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Я готов работать с базой данных.")


@router.message(F.text)
async def handle_user_query(message: Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    user_text = message.text
    answer = await assistant.ask(user_text)

    await message.answer(answer)
