import requests

data = {
    "en_female": "en-US-JennyNeural",
    "en_male": "en-US-AdolfoNeural",
    "uz_female": "uz-UZ-MadinaNeural",
    "uz_male": "uz-UZ-SardorNeural",
}


def tts_change(mod, text):
    json_data = {
        "userId": "inUAm03YN6bzaW49f2ztet2P91V2",
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
                r = response.json()
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

result = tts_change(mod=data["en_female"], text="Assalomu Aleykum. Xurmatli ota onalar sizlar bilan Mr.Mirmakhmudov")
print("\nAPI javobi:", result)
