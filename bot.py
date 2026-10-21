import telebot, requests, re

BOT_TOKEN = "8764129682:AAHx10MzjcMVPSGv9EiURmG6nmVxIDzLyJQ"
POLLEN_KEY = "sk_byyg5IYazgK0nQdmHuRy9UcADycvyWCs"  # <--- сюда

bot = telebot.TeleBot(BOT_TOKEN)

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
        # если опять лимит - скажем честно
        if "Free limit" in t:
            bot.send_message(m.chat.id, "Подожди 10 сек, лимит апишки 🙏")
            return
            
        t = re.sub(r'https?://\S+', '', t)
        bot.send_message(m.chat.id, t.strip())
    except Exception as e:
        print(e)

bot.infinity_polling()