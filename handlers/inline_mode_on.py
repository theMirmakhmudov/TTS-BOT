import requests
import hashlib
from aiogram import Router, types
import time
from dotenv import load_dotenv
import os

load_dotenv()

router = Router()

def tts_change(mod, text, retries=3, delay=3):
    json_data = {
        "userId": os.getenv("API_USER_ID"),
        "platform": "landing_demo",
        "ssml": f"<speak><p>{text}</p></speak>",
        "voice": f"{mod}",
        "narrationStyle": "regular"
    }

    for attempt in range(retries):
        try:
            response = requests.post("https://play.ht/api/transcribe", json=json_data)

            if response.status_code == 200:
                try:
                    r = response.json()
                    if 'file' in r:
                        return r['file']
                    else:
                        return None
                except requests.exceptions.JSONDecodeError:
                    return None
            else:
                return None
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return None

@router.inline_query()
async def inline_query_message(query: types.InlineQuery):
    user_text = query.query
    audio_url = tts_change(mod="uz-UZ-MadinaNeural", text=user_text if user_text else "Hello, Whats App")

    if audio_url:
        result_id = hashlib.md5(user_text.encode()).hexdigest()
        articles = [
            types.InlineQueryResultAudio(
                id=result_id,
                audio_url=audio_url,
                title=f"{user_text}",
                start_parameter=result_id
            )
        ]

        await query.answer(results=articles, cache_time=1, is_personal=True)
    else:
        await query.answer(results=[], switch_pm_text="Xatolik yuz berdi", switch_pm_user_id=query.from_user.id)
