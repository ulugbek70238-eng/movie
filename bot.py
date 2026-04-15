import requests

TOKEN = ""

ADMIN_ID = ''

def send_notification(message: str):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    playload = {
        'chat_id': ADMIN_ID,
        'text': message,
        'parse_mode': 'HTML',
    }
    try:
        response = requests.post(url, json=playload)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка при отправке в телеграм, {e}")