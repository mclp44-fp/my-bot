import telebot, requests, re
from flask import Flask
from threading import Thread
import os

BOT_TOKEN = "8764129682:AAHx10MzjcMVPSGv9EiURmG6nmVxIDzLyJQ" 
POLLEN_KEY = "sk_byyq51YazgK8nQdaHuIty9UcADycvyMCs"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

@bot.message_handler(content_types=['text'])
def h(m):
    try:
        r = requests.post("https://text.pollinations.ai/openai",
            headers={"Authorization": f"Bearer {POLLEN_KEY}"},
            json={
                "model": "openai-fast",
                "messages": [{"role": "user", "content": m.text}]
            }, timeout=30).json()
        
        t = r['choices'][0]['message']['content']
        
        if "Free limit" in t:
            bot.send_message(m.chat.id, "Подожди 10 сек, лимит апишек 🙏")
            return
            
        t = re.sub(r'https?://\S+', '', t)
        bot.send_message(m.chat.id, t.strip())
    except Exception as e:
        print(e)

def run_bot():
    bot.infinity_polling()

Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
