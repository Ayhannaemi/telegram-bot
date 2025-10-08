from flask import Flask, request
import requests
import os

TOKEN = "8094291923:AAENXpm4aBXhIjIUx6_4tKuCKsiwmh9ssc8"
URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)

# -----------------------------
# تابع ارسال پیام به کاربر
# -----------------------------
def send_message(chat_id, text):
    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": text})

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
                              "برای سفارش، پیام بده: @Arena_Suppoort")
    elif text == "/kolye":
        send_message(chat_id, "فی هشتصد\nبرای دیدن خدمات، دستور /services رو بفرست.")
    else:
        send_message(chat_id, "❓ دستور ناشناخته! از /start استفاده کن.")

    return "ok"

# -----------------------------
# صفحه تست
# -----------------------------
@app.route("/")
def home():
    return "🤖 Telegram Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
