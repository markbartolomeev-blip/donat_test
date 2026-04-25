from flask import Flask, request
import requests
import hashlib

app = Flask(__name__)

BOT_TOKEN = "8607747387:AAHUwYkVplbTdZan1O-jsVkA7y5z-tfSgMA"     # от @BotFather
SECRET = "7jHL+Kzgz7KkKtcr9EtCl88q"     # из настроек формы

@app.route('/', methods=['POST'])
def webhook():
    data = request.form.to_dict()
    
    if data.get('notification_type') != 'p2p-incoming':
        return 'OK'
    
    # Проверка подписи
    check_str = f"{data['notification_type']}&{data['operation_id']}&{data['amount']}&{SECRET}&{data['label']}"
    if hashlib.sha1(check_str.encode()).hexdigest() != data.get('sha1_hash'):
        return 'Bad sign'
    
    user_id = int(data['label'])
    coins = int(float(data['amount']) * 10)
    
    # Отправка в Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={'chat_id': user_id, 'text': f'✅ Получено {coins} монет!'})
    
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
