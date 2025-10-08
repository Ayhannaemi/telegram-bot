from flask import Flask, request
import requests
import os
import openai
import time

# -----------------------------
# کلیدهای API و توکن
# -----------------------------
TOKEN = os.environ.get("BOT_TOKEN")  # توکن ربات از Environment Variables
URL = f"https://api.telegram.org/bot{TOKEN}/"

# خواندن کلید OpenAI از فایل سکرت
with open("/etc/secrets/openai_key.txt") as f:
    OPENAI_API_KEY = f.read().strip()

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

# -----------------------------
# تابع ارسال پیام به کاربر
# -----------------------------
def send_message(chat_id, text):
    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": text})

# -----------------------------
# تابع نمایش تایپینگ
# -----------------------------
def send_typing(chat_id):
    requests.post(URL + "sendChatAction", data={"chat_id": chat_id, "action": "typing"})

# -----------------------------
# تابع چت با ChatGPT
# -----------------------------
def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "⚠️ خطا در پاسخگویی ChatGPT."

# -----------------------------
# پاسخ به پیام‌های کاربران
# -----------------------------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    if text == "/start":
        send_message(chat_id, "👋 سلام! من ربات خدمات طراحی و برنامه‌نویسی هستم.\n"
                              "برای دیدن خدمات، دستور /services رو بفرست.")
    elif text == "/services":
        send_message(chat_id, "📋 خدمات ما:\n"
                              "1️⃣ طراحی سایت\n"
                              "2️⃣ طراحی اپلیکیشن موبایل\n"
                              "3️⃣ طراحی رابط کاربری (UI/UX)\n"
                              "4️⃣ پروژه‌های پایتون و جاوااسکریپت\n\n"
                              "برای سفارش، پیام بده: @Arena_Support")
    elif text == "/kolye":
        send_message(chat_id, "💎 فی هشتصد\nبرای دیدن خدمات، دستور /services رو بفرست.")
    else:
        # نمایش حالت تایپینگ قبل از پاسخ ChatGPT
        send_typing(chat_id)
        time.sleep(1)  # زمان شبیه‌سازی تایپینگ
        answer = chat_with_gpt(text)
        send_message(chat_id, answer)

    return "ok"

# -----------------------------
# صفحه تست
# -----------------------------
@app.route("/")
def home():
    return "🤖 Telegram Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
