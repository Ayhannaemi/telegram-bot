from flask import Flask, request
import requests
import os
import openai

# -----------------------------
# تنظیمات توکن تلگرام و ChatGPT
# -----------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # توکن ربات تلگرام از Environment Variable
with open("/etc/secrets/openai_key.txt") as f:  # کلید ChatGPT از Secret File
    OPENAI_API_KEY = f.read().strip()

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

# -----------------------------
# ارسال پیام به کاربر
# -----------------------------
def send_message(chat_id, text):
    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": text})

# -----------------------------
# پاسخ به پیام‌ها
# -----------------------------
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    # دستورهای ثابت ربات
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
        send_message(chat_id,"فی هشتصد\nبرای دیدن خدمات، دستور /services رو بفرست.")
    elif text == "/contact":
        send_message(chat_id,"📩 برای مشاوره با پشتیبانی: @Arena_Suppoort")
    
    # بخش ChatGPT (مشاوره آنلاین)
    elif text.startswith("/chat "):
        user_question = text.replace("/chat ", "", 1)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_question}],
                temperature=0.7,
                max_tokens=500
            )
            answer = response.choices[0].message.content
            send_message(chat_id, f"💬 پاسخ ChatGPT:\n{answer}")
        except Exception as e:
            send_message(chat_id, f"⚠️ خطا در پاسخگویی ChatGPT: {str(e)}")

    else:
        send_message(chat_id, "❓ دستور ناشناخته! از /start استفاده کن.")

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
