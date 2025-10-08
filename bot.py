from flask import Flask, request
import requests
import os
import json

# -----------------------------
# توکن ربات تلگرام
# -----------------------------
TOKEN = os.environ.get("BOT_TOKEN")  # یا توکن مستقیم: "8094291923:AAENXpm4aBXhIjIUx6_4tKuCKsiwmh9ssc8"
URL = f"https://api.telegram.org/bot{TOKEN}/"

# -----------------------------
# کلید OpenAI (ChatGPT)
# -----------------------------
with open("/etc/secrets/openai_key.txt") as f:
    OPENAI_API_KEY = f.read().strip()

# -----------------------------
# اپلیکیشن Flask
# -----------------------------
app = Flask(__name__)

# -----------------------------
# ارسال پیام به کاربر
# -----------------------------
def send_message(chat_id, text):
    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": text})

# -----------------------------
# پاسخ ChatGPT
# -----------------------------
def chatgpt_reply(user_message):
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_message}]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=headers, data=json.dumps(data))
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error ChatGPT:", e)
        return "⚠️ خطا در پاسخگویی ChatGPT."

# -----------------------------
# مسیر وب‌هوک
# -----------------------------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["get"]("text", "")

    # دستورات آماده
    if text == "/start":
        send_message(chat_id, "👋 سلام! من ربات خدمات طراحی و برنامه‌نویسی هستم.\n"
                              "برای دیدن خدمات، دستور /services رو بفرست.")
    elif text == "/services":
        send_message(chat_id, "📋 خدمات ما:\n"
                              "1️⃣ طراحی سایت\n"
                              "2️⃣ طراحی اپلیکیشن موبایل\n"
                              "3️⃣ طراحی رابط کاربری (UI/UX)\n"
                              "4️⃣ پروژه‌های پایتون و جاوااسکریپت\n\n"
                              "برای سفارش، پیام بده: @Arena_Suppoort")
    elif text == "/kolye":
        send_message(chat_id, "فی هشتصد\nبرای دیدن خدمات، دستور /services رو بفرست.")
    elif text.startswith("/gpt"):
        # /gpt متن سوال
        user_question = text.replace("/gpt", "").strip()
        if user_question:
            reply = chatgpt_reply(user_question)
            send_message(chat_id, reply)
        else:
            send_message(chat_id, "لطفا بعد از /gpt سوال خودت رو تایپ کن.")
    else:
        # هر متن دیگه هم ChatGPT جواب بده
        reply = chatgpt_reply(text)
        send_message(chat_id, reply)

    return "ok"

# -----------------------------
# صفحه تست
# -----------------------------
@app.route("/")
def home():
    return "🤖 Telegram Bot is running!"

# -----------------------------
# اجرا
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
