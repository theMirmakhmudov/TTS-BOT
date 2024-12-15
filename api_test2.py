import requests

url = "https://api.play.ht/api/v2/tts/stream"

payload = {
    "voice": "s3://voice-cloning-zero-shot/b41d1a8c-2c99-4403-8262-5808bc67c3e0/bentonsaad/manifest.json",
    "output_format": "mp3",
    "voice_engine": "PlayDialog",
    "quality": "high",
    "emotion": "male_happy",
    "text": "Hello, Whats App"
}

headers = {
    "accept": "audio/mpeg",
    "content-type": "application/json",
    "AUTHORIZATION": "775444a119154243a510458eeb282df0",
    "X-USER-ID": "5KJikVASKPZgeYY28DpnSXbQafI3"
}

# So'rov yuborish
response = requests.post(url, json=payload, headers=headers)

# Javobni tekshirish
if response.status_code == 200:
    # MP3 faylini saqlash
    with open('output_audio.mp3', 'wb') as f:
        f.write(response.content)
    print("MP3 fayl muvaffaqiyatli saqlandi: 'output_audio.mp3'")
else:
    print("Xatolik yuz berdi:", response.status_code, response.text)
