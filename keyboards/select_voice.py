from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

voice_select = InlineKeyboardBuilder()
voice_select.row(types.InlineKeyboardButton(text="Erkak 🤵‍♂️", callback_data="male_voice"), types.InlineKeyboardButton(text="Ayol 👩", callback_data="female_voice"))


language_select_male = InlineKeyboardBuilder()
language_select_male.row(types.InlineKeyboardButton(text="Uzbek 🇺🇿", callback_data="uz_language_male"), types.InlineKeyboardButton(text="English 🇺🇸", callback_data="en_language_male"))

language_select_female = InlineKeyboardBuilder()
language_select_female.row(types.InlineKeyboardButton(text="Uzbek 🇺🇿", callback_data="uz_language_female"), types.InlineKeyboardButton(text="English 🇺🇸", callback_data="en_language_female"))

check_male = InlineKeyboardBuilder()
check_male.row(types.InlineKeyboardButton(text="Tasdiqlash ✅", callback_data="check_accept_male"))
check_male.row(types.InlineKeyboardButton(text="Bekor qilish ❌", callback_data="check_cancel"))

check_female = InlineKeyboardBuilder()
check_female.row(types.InlineKeyboardButton(text="Tasdiqlash ✅", callback_data="check_accept_female"))
check_female.row(types.InlineKeyboardButton(text="Bekor qilish ❌", callback_data="check_cancel"))


check_male_en = InlineKeyboardBuilder()
check_male_en.row(types.InlineKeyboardButton(text="Accept ✅", callback_data="check_accept_male_en"))
check_male_en.row(types.InlineKeyboardButton(text="Bekor qilish ❌", callback_data="check_cancel"))


check_female_en = InlineKeyboardBuilder()
check_female_en.row(types.InlineKeyboardButton(text="Accept ✅", callback_data="check_accept_female_en"))
check_female_en.row(types.InlineKeyboardButton(text="Bekor qilish ❌", callback_data="check_cancel"))


emotions_male = InlineKeyboardBuilder()
emotions_male.row(types.InlineKeyboardButton(text="Happy 😂", callback_data="happy_emotion_male"), types.InlineKeyboardButton(text="Sad 😢", callback_data="sad_emotion_male"))
emotions_male.row(types.InlineKeyboardButton(text="Angry 😡", callback_data="angry_emotion_male"), types.InlineKeyboardButton(text="Surprised 😮", callback_data="surprised_emotion_male"))

emotions_female = InlineKeyboardBuilder()
emotions_female.row(types.InlineKeyboardButton(text="Happy 😂", callback_data="happy_emotion_female"), types.InlineKeyboardButton(text="Sad 😢", callback_data="sad_emotion_female"))
emotions_female.row(types.InlineKeyboardButton(text="Angry 😡", callback_data="angry_emotion_female"), types.InlineKeyboardButton(text="Surprised 😮", callback_data="surprised_emotion_female"))