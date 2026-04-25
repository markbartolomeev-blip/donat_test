from flask import Flask, request
import hashlib
import requests

app = Flask(__name__)

BOT_TOKEN = "8607747387:AAHUwYkVplbTdZan1O-jsVkA7y5z-tfSgMA"  # от @BotFather
YOOMONEY_SECRET = "7jHL+Kzgz7KkKtcr9EtCl88q"  # которое в настройках формы

@app.route('/webhook', methods=['POST'])
def yoomoney_webhook():
    data = request.form.to_dict()
    print("Получено:", data)
    
    notification_type = data.get('notification_type')
    if notification_type != 'p2p-incoming':
        return 'OK'
    
    label = data.get('label')      # Telegram ID пользователя
    amount = float(data.get('amount', 0))
    operation_id = data.get('operation_id')
    sha1 = data.get('sha1_hash')
    
    # Проверка подписи
    check_str = f"{notification_type}&{operation_id}&{amount}&{YOOMONEY_SECRET}&{label}"
    if hashlib.sha1(check_str.encode()).hexdigest() != sha1:
        print("Неверная подпись!")
        return 'Invalid signature', 400
    
    # Рассчитываем монеты (10 монет за 1 рубль)
    coins = int(amount * 10)
    
    # Отправляем пользователю через бота
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        'chat_id': label,
        'text': f"✅ Оплачено {amount} ₽\n🎮 Получено {coins} монет!"
    })
    
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
