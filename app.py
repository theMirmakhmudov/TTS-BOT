import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, executor, types
import aiohttp
from sql import Database
from config import API_TOKEN, ADMIN

db = Database(path_to_db="database.db")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def tts_change(mod, text):
    json_data = {
        "userId": "public-access",
        "platform": "landing_demo",
        "ssml": f"<speak><p>{text}</p></speak>",
        "voice": f"{mod}",
        "narrationStyle": "regular"
    }
    # response = requests.post("https://play.ht/api/transcribe", json=json_data).json()['file']
    async with aiohttp.ClientSession() as session:
        async with session.post("https://play.ht/api/transcribe", json=json_data) as response:
            async with session.post("https://play.ht/api/transcribe", json=json_data) as response:
                if response.status == 200:
                    r = await response.json()
                    print(r)
                    return r
                else:
                    print(f"Xato yuz berdi! Status kodi: {response.status}")
                    return None


async def download_file(url, destination):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(destination, 'wb') as f:
                    f.write(await response.read())
                return 'save'
            else:
                print(f"Failed to download: {response.status}")


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    try:
        db.add_user(user_id=message.from_user.id, name=message.from_user.full_name, voice='women')
    except:
        pass

    await message.answer(f"<b>Assalomu alaykum, {message.from_user.get_mention()}\nBotga biror bir xabar yuboring ovoz qilib beradi ✅</b>")


@dp.message_handler(commands=['change_language'])
async def send_welcome(message: types.Message):
    try:
        db.add_user(user_id=message.from_user.id, name=message.from_user.full_name, voice='women')
    except:
        pass

    await message.answer(f"""<b>📣 Ovozni o'zgartirish</b>""", reply_markup=types.InlineKeyboardMarkup(row_width=2).add(
        types.InlineKeyboardButton("Erkak kishi", callback_data=f"male"),
        types.InlineKeyboardButton("Ayol kishi", callback_data=f"women")))


@dp.callback_query_handler(state="*")
async def send_welcome(call: types.CallbackQuery):
    if call.data == 'male':
        db.update_user_voice(voice='male', user_id=call.from_user.id)
        await call.answer(text="🧔🏻‍♂️ Erkak kishi tili sozlandi!", show_alert=True)
        await call.message.delete()
    elif call.data == 'women':
        db.update_user_voice(voice='women', user_id=call.from_user.id)

        await call.answer(text="👩‍🦰 Ayol kishi tili sozlandi!", show_alert=True)
        await call.message.delete()
    else:
        pass


@dp.message_handler(commands=['stat'], chat_id=ADMIN)
async def statiska(message: types.Message):
    stat = db.stat()
    await message.answer(stat[0])
    print(stat)


@dp.message_handler(commands=['send'], chat_id=ADMIN)
async def send_users(message: types.Message):
    user = db.select_all_users()
    for i in user:
        user_id = i[1]
        try:
            await bot.send_message(chat_id=user_id, text="""<b>Bot yangilandi!

/start - buyrug'i orqali botni yangilang...

Yangilanish ro'yxati:</b>
<i>- botdagi imloviy xatoliklar tuzatilishi
- tezlik oshirilishi</i>""")
        except:
            pass
    await message.answer("Xabar yuborildi...")


@dp.message_handler(state='*')
async def send_welcome(message: types.Message):
    user = db.is_user(user_id=message.from_user.id)
    bot_user = await bot.get_me()
    se = ""
    for x in user:
        se += x[3]
    sen = await message.reply('⏳')
    if se == 'male':
        res = await tts_change(mod="uz-UZ-SardorNeural", text=message.text)
    elif se == 'women':
        res = await tts_change(mod="uz-UZ-MadinaNeural", text=message.text)
    try:
        mn = await download_file(res['file'], '{}.ogg'.format(message.message_id))
        if mn == 'save':
            with open('{}.ogg'.format(message.message_id), "rb") as voice:
                await sen.delete()
                await bot.send_voice(chat_id=message.from_user.id, voice=voice,
                                     caption=f"<b>{message.text}\n🎙 @{bot_user.username}</b>")
            os.remove('{}.ogg'.format(message.message_id))
    except:
        await sen.delete()


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "♻️ Botni qayta ishga tushurish"),
            types.BotCommand("change_language", "🔉 ovozni o'zgartirish"),
        ]
    )


if __name__ == '__main__':
    try:
        db.create_table_users()
    except:
        pass
    executor.start_polling(dp, skip_updates=True, on_startup=set_default_commands)
