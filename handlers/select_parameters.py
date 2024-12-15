from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from keyboards.select_voice import language_select_male, language_select_female, check_male, check_female, \
    check_male_en, check_female_en, emotions_male, emotions_female
from aiogram.fsm.context import FSMContext
from states.upload_text import GetText1, GetText2, GetText3, GetText4
from config import API_TOKEN
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()
import os
router = Router()
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "male_voice")
async def cmd_choose_male(callback: CallbackQuery):
    await callback.message.edit_text(text="<b>Tilni tanlang: </b>", reply_markup=language_select_male.as_markup())


@router.callback_query(F.data == "uz_language_male")
async def cmd_uz_male(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="<b>📝 Matnni kiriting:</b>")
    await state.set_state(GetText1.text)


@router.message(GetText1.text)
async def cmd_uz_male_text(message: Message, state: FSMContext):
    await state.update_data(speechtext=message.text)
    await message.answer(
        text=f"<b>Ovoz: Erkak 🤵‍♂️\nTil: Uzbek 🇺🇿\nMatn: {message.text} 📝</b>",
        reply_markup=check_male.as_markup())
    await state.set_state(GetText1.finish)


@router.callback_query(F.data == "check_accept_male")
async def cmd_check_accept(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_text(text="<b>Tasdiqlandi ✅\n Holati: Tayyorlanmoqda.... </b>")
    data1 = await state.get_data()
    await state.clear()
    speechtext = data1.get("speechtext", "Unknown")
    import requests
    import time

    def tts_change(mod, text):
        json_data = {
            "userId": os.getenv("API_USER_ID"),
            "platform": "landing_demo",
            "ssml": f"<speak><p>{text}</p></speak>",
            "voice": f"{mod}",
            "narrationStyle": "regular"
        }
        print("Yuborilayotgan ma'lumot:", json_data)

        try:
            response = requests.post("https://play.ht/api/transcribe", json=json_data)
            print("\nJavobni tekshirish:")
            print("Status kodi:", response.status_code)
            print("Content-Type:", response.headers.get('Content-Type'))

            if response.status_code == 200:
                try:
                    r = response.json()["file"]
                    print("API'dan olingan javob:", r)
                    return r
                except requests.exceptions.JSONDecodeError:
                    print("Javob JSON formatida emas!")
                    print("Javob:", response.text)
                    return None
            else:
                print(f"Xatolik yuz berdi! Status kodi: {response.status_code}")
                print("Javob:", response.text)
                return None
        except requests.exceptions.RequestException as e:
            print("So'rov yuborishda xato yuz berdi:", e)
            return None

    def tts_change_with_retry(mod, text, retries=3, delay=2):
        attempt = 0
        while attempt < retries:
            result = tts_change(mod, text)

            if result is not None:
                return result

            print(f"Javob topilmadi, qayta urinish {attempt + 1}...")
            attempt += 1
            time.sleep(delay)
        print("So'rovni qayta yuborish mumkin emas!")
        return None

    result = tts_change_with_retry(mod="uz-UZ-SardorNeural", text=speechtext)
    print("\nAPI javobi:", result)
    bot_info = await bot.get_me()
    del_mes = await callback.message.edit_text(text=f"<b>Tasdiqlandi ✅\nHolati: Fayl yuklanmoqda....</b>")
    await bot.send_audio(callback.from_user.id, result,
                         caption=f"<b>Ovoz: Erkak 🤵‍♂️\nTil: Uzbek 🇺🇿\nMatn: {speechtext}\n\n@{bot_info.username}</b>")
    await bot.delete_message(callback.from_user.id, del_mes.message_id)
    await callback.answer("Tayyor ✅")


@router.callback_query(F.data == "female_voice")
async def cmd_choose_female(callback: CallbackQuery):
    await callback.message.edit_text(text="<b>Tilni tanlang: </b>", reply_markup=language_select_female.as_markup())


@router.callback_query(F.data == "uz_language_female")
async def cmd_uz_male(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="<b>📝 Matnni kiriting:</b>")
    await state.set_state(GetText2.text)


@router.message(GetText2.text)
async def cmd_uz_male_text(message: Message, state: FSMContext):
    await state.update_data(speechtext=message.text)
    await message.answer(text=f"<b>Ovoz: Female 👩\nTil: Uzbek 🇺🇿\nMatn: {message.text} 📝</b>",
                         reply_markup=check_female.as_markup())
    await state.set_state(GetText2.finish)


@router.callback_query(F.data == "check_accept_female")
async def cmd_check_accept_female(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_text(text="<b>Tasdiqlandi ✅\n Holati: Tayyorlanmoqda.... </b>")
    data2 = await state.get_data()
    await state.clear()
    speechtext2 = data2.get("speechtext", "Unknown")
    import requests
    import time

    def tts_change(mod, text):
        json_data = {
            "userId": os.getenv("API_USER_ID"),
            "platform": "landing_demo",
            "ssml": f"<speak><p>{text}</p></speak>",
            "voice": f"{mod}",
            "narrationStyle": "regular"
        }
        print("Yuborilayotgan ma'lumot:", json_data)

        try:
            response = requests.post("https://play.ht/api/transcribe", json=json_data)
            print("\nJavobni tekshirish:")
            print("Status kodi:", response.status_code)
            print("Content-Type:", response.headers.get('Content-Type'))

            if response.status_code == 200:
                try:
                    r = response.json()["file"]
                    print("API'dan olingan javob:", r)
                    return r
                except requests.exceptions.JSONDecodeError:
                    print("Javob JSON formatida emas!")
                    print("Javob:", response.text)
                    return None
            else:
                print(f"Xatolik yuz berdi! Status kodi: {response.status_code}")
                print("Javob:", response.text)
                return None
        except requests.exceptions.RequestException as e:
            print("So'rov yuborishda xato yuz berdi:", e)
            return None

    def tts_change_with_retry(mod, text, retries=3, delay=2):
        attempt = 0
        while attempt < retries:
            result = tts_change(mod, text)

            if result is not None:
                return result

            print(f"Javob topilmadi, qayta urinish {attempt + 1}...")
            attempt += 1
            time.sleep(delay)
        print("So'rovni qayta yuborish mumkin emas!")
        return None

    result = tts_change_with_retry(mod="uz-UZ-MadinaNeural", text=speechtext2)
    print("\nAPI javobi:", result)
    bot_info = await bot.get_me()
    del_mes = await callback.message.edit_text(text=f"<b>Tasdiqlandi ✅\nHolati: Fayl yuklanmoqda....</b>")
    await bot.send_audio(callback.from_user.id, result,
                         caption=f"<b>Ovoz: Ayol 👩\nTil: Uzbek 🇺🇿</b>\nMatn: {speechtext2}\n\n@{bot_info.username} ")
    await bot.delete_message(callback.from_user.id, del_mes.message_id)
    await callback.answer("Tayyor ✅")


@router.callback_query(F.data == "en_language_male")
async def cmd_en_male(callback: CallbackQuery):
    await callback.message.edit_text(text="<b>🥹 Emotion tanlang:</b>", reply_markup=emotions_male.as_markup())


@router.callback_query(F.data == "happy_emotion_male")
async def cmd_happy_emotion(callback: CallbackQuery, state: FSMContext):
    await state.update_data(speechemotion="male_happy")
    await callback.message.edit_text(f"<b>📝 Matnni kiriting: </b>")
    await state.set_state(GetText3.text)


@router.callback_query(F.data == "angry_emotion_male")
async def cmd_angry_emotion(callback: CallbackQuery, state: FSMContext):
    await state.update_data(speechemotion="male_angry")
    await callback.message.edit_text(f"<b>📝 Matnni kiriting: </b>")
    await state.set_state(GetText3.text)


@router.callback_query(F.data == "sad_emotion_male")
async def cmd_sad_emotion(callback: CallbackQuery, state: FSMContext):
    await state.update_data(speechemotion="male_sad")
    await callback.message.edit_text(f"<b>📝 Matnni kiriting: </b>")
    await state.set_state(GetText3.text)


@router.callback_query(F.data == "surprised_emotion_male")
async def cmd_happy_emotion(callback: CallbackQuery, state: FSMContext):
    await state.update_data(speechemotion="male_surprised")
    await callback.message.edit_text(f"<b>📝 Matnni kiriting: </b>")
    await state.set_state(GetText3.text)


@router.message(GetText3.text)
async def cmd_uz_male_text(message: Message, state: FSMContext):
    await state.update_data(speechtext=message.text)
    await state.set_state(GetText3.finish)
    data3 = await state.get_data()
    emotion1 = data3.get("speechemotion", "Unknown")
    await message.answer(
        text=f"<b>Ovoz: Erkak 🤵‍♂️\nTil: English 🇺🇸\nEmotion: {emotion1}\nMatn: {message.text} 📝</b>",
        reply_markup=check_male_en.as_markup())


@router.callback_query(F.data == "check_accept_male_en")
async def cmd_check_male_en(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_text(text="<b>Tasdiqlandi ✅\nHolati: Tayyorlanmoqda.... </b>")
    data3 = await state.get_data()
    await state.clear()
    speechtext3 = data3.get("speechtext", "Unknown")
    speechemotion1 = data3.get("speechemotion", "Unknown")
    print(data3)

    import requests

    url = "https://api.play.ht/api/v2/tts/stream"

    payload = {
        "voice": "s3://voice-cloning-zero-shot/b41d1a8c-2c99-4403-8262-5808bc67c3e0/bentonsaad/manifest.json",
        "output_format": "mp3",
        "voice_engine": "PlayDialog",
        "quality": "high",
        "emotion": f"{speechemotion1}",
        "text": f"{speechtext3}"
    }

    headers = {
        "accept": "audio/mpeg",
        "content-type": "application/json",
        "AUTHORIZATION": os.getenv("API_KEY"),
        "X-USER-ID": os.getenv("API_USER_ID")
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        with open(f'tts_audio.mp3', 'wb') as file:
            file.write(response.content)
        del_mes = await callback.message.edit_text(text="<b>Tasdiqlandi ✅\nHolati: Fayl yuklanmoqda.... </b>")
        bot_info = await bot.get_me()
        with open("tts_audio.mp3", "rb") as music_from_buffer:
            await callback.message.answer_audio(
                BufferedInputFile(
                    music_from_buffer.read(),
                    filename="tts_audio.mp3"
                ),
                caption=f"<b>Ovoz: Male 🤵‍♂️\nTil: English 🇺🇸\nEmotion: {speechemotion1}\nMatn: {speechtext3}\n\n🤖 @{bot_info.username} </b>")
            await bot.delete_message(callback.from_user.id, del_mes.message_id)
            await callback.answer("Tayyor ✅")


    else:
        print("Xatolik yuz berdi:", response.status_code, response.text)
        await callback.message.edit_text(text=f"Xatolik yuz berdi: {response.status_code} - {response.text}")


# ----------------------------------


@router.callback_query(F.data == "en_language_female")
async def cmd_en_female(callback: CallbackQuery):
    await callback.message.edit_text(text="<b>🥹 Emotion tanlang:</b>", reply_markup=emotions_female.as_markup())


@router.callback_query(F.data == "happy_emotion_female")
async def cmd_happy_emotion(callback: CallbackQuery, state: FSMContext):
    await state.update_data(speechemotion="female_happy")
    await callback.message.edit_text(f"<b>📝 Matnni kiriting: </b>")
    await state.set_state(GetText4.text)


@router.callback_query(F.data == "angry_emotion_female")
async def cmd_angry_emotion(callback: CallbackQuery, state: FSMContext):
    await state.update_data(speechemotion="female_angry")
    await callback.message.edit_text(f"<b>📝 Matnni kiriting: </b>")
    await state.set_state(GetText4.text)


@router.callback_query(F.data == "sad_emotion_female")
async def cmd_sad_emotion(callback: CallbackQuery, state: FSMContext):
    await state.update_data(speechemotion="female_sad")
    await callback.message.edit_text(f"<b>📝 Matnni kiriting: </b>")
    await state.set_state(GetText4.text)


@router.callback_query(F.data == "surprised_emotion_female")
async def cmd_happy_emotion(callback: CallbackQuery, state: FSMContext):
    await state.update_data(speechemotion="female_surprised")
    await callback.message.edit_text(f"<b>📝 Matnni kiriting: </b>")
    await state.set_state(GetText4.text)


@router.message(GetText4.text)
async def cmd_uz_female_text(message: Message, state: FSMContext):
    await state.update_data(speechtext=message.text)
    await state.set_state(GetText4.finish)
    data4 = await state.get_data()
    emotion2 = data4.get("speechemotion", "Unknown")
    await message.answer(
        text=f"<b>Ovoz: Ayol 👩️\nTil: English 🇺🇸\nEmotion: {emotion2}\nMatn: {message.text} 📝</b>",
        reply_markup=check_female_en.as_markup())


@router.callback_query(F.data == "check_accept_female_en")
async def cmd_check_female_en(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_text(text="<b>Tasdiqlandi ✅\nHolati: Tayyorlanmoqda.... </b>")
    data4 = await state.get_data()
    await state.clear()
    speechtext4 = data4.get("speechtext", "Unknown")
    speechemotion2 = data4.get("speechemotion", "Unknown")

    import requests

    url = "https://api.play.ht/api/v2/tts/stream"

    payload = {
        "voice": "s3://voice-cloning-zero-shot/34eaa933-62cb-4e32-adb8-c1723ef85097/original/manifest.json",
        "output_format": "mp3",
        "voice_engine": "PlayDialog",
        "quality": "high",
        "emotion": f"{speechemotion2}",
        "text": f"{speechtext4}"
    }

    headers = {
        "accept": "audio/mpeg",
        "content-type": "application/json",
        "AUTHORIZATION": os.getenv("API_KEY"),
        "X-USER-ID": os.getenv("API_USER_ID")
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        with open(f'tts_audio.mp3', 'wb') as file:
            file.write(response.content)
        del_mes = await callback.message.edit_text(text="<b>Tasdiqlandi ✅\nHolati: Fayl yuklanmoqda.... </b>")
        bot_info = await bot.get_me()
        with open("tts_audio.mp3", "rb") as music_from_buffer:
            await callback.message.answer_audio(
                BufferedInputFile(
                    music_from_buffer.read(),
                    filename="tts_audio.mp3",
                ),
                caption=f"<b>Ovoz: Female 👩\nTil: English 🇺🇸\nEmotion: {speechemotion2}\nMatn: {speechtext4}\n\n🤖 @{bot_info.username} </b>")
            await bot.delete_message(callback.from_user.id, del_mes.message_id)
            await callback.answer("Tayyor ✅")


    else:
        print("Xatolik yuz berdi:", response.status_code, response.text)
        await callback.message.edit_text(text=f"Xatolik yuz berdi: {response.status_code} - {response.text}")


@router.callback_query(F.data == "check_cancel")
async def cmd_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text="<b>Bekor qilindi ✅</b>")
