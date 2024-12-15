from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from models.user import User
from services.user import add_user
from keyboards.select_voice import voice_select

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    user = await User.get_or_none(user_id=message.from_user.id)
    if not user:
        await add_user(user_id=message.from_user.id, full_name=message.from_user.full_name,
                       username=message.from_user.username)
        await message.answer(
            f"<b>Assalomu Aleykum {message.from_user.mention_html()}.\nUshbu Text to Speech botimizga qo'shilganingiz bilan tabriklaymiz 🥳.\nOvozni tanlang: </b>",
            reply_markup=voice_select.as_markup())

    else:
        await message.answer(f"<b>Assalomu Aleykum {message.from_user.mention_html()}.\nQaytganingiz bilan qutlaymiz 🤗.\nOvozni tanlang: </b>",reply_markup=voice_select.as_markup())
