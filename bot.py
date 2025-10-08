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
    text = data["message"].get("text", "").lower()

    if text == "/start":
        send_message(chat_id, "👋 سلام! خوش اومدی به ربات Arena PC.\n"
                              "برای دیدن خدمات، دستور /services رو بفرست ✨")

    elif text == "/services":
        send_message(chat_id, "📋 خدمات ما:\n"
                              "1️⃣ طراحی و پشتیبانی وب‌سایت\n"
                              "2️⃣ طراحی اپلیکیشن موبایل\n"
                              "3️⃣ رابط کاربری (UI/UX)\n"
                              "4️⃣ پروژه‌های پایتون، جاوااسکریپت و وردپرس\n"
                              "5️⃣ فروش و تعمیر لپ‌تاپ و لوازم جانبی\n\n"
                              "برای جزئیات بیشتر: /price")

    elif text == "/price":
        send_message(chat_id, "💰 تعرفه‌ها:\n"
                              "🔹 طراحی سایت از ۳ میلیون تومان\n"
                              "🔹 طراحی اپلیکیشن از ۵ میلیون تومان\n"
                              "🔹 پشتیبانی سایت ماهیانه از ۵۰۰ هزار تومان\n"
                              "🔹 پروژه دانشجویی از ۳۵۰ هزار تومان به بالا\n\n"
                              "برای سفارش، دستور /order رو بفرست.")

    elif text == "/order":
        send_message(chat_id, "🧾 برای ثبت سفارش لطفاً موارد زیر را ارسال کنید:\n"
                              "1️⃣ نوع پروژه (مثلاً سایت یا اپ)\n"
                              "2️⃣ توضیح کوتاه درباره نیازت\n"
                              "3️⃣ زمان‌بندی مدنظر\n\n"
                              "📨 بعد از ارسال، با شما تماس می‌گیریم.\n"
                              "پشتیبانی: @Arena_Suppoort")

    elif text == "/portfolio":
        send_message(chat_id, "📂 نمونه کارها:\n"
                              "🌐 arenapc.ir\n"
                              "💼 instagram.com/arena_pc\n\n"
                              "برای سفارش اختصاصی: /order")

    elif text == "/about":
        send_message(chat_id, "🏢 درباره ما:\n"
                              "ArenaPC مجموعه‌ای از طراحان و برنامه‌نویسانه که روی پروژه‌های وب، اپلیکیشن و سیستم‌های هوشمند کار می‌کنن.\n"
                              "🎯 هدف ما، ترکیب خلاقیت با تکنولوژی‌ست.")

    elif text == "/contact":
        send_message(chat_id, "📞 راه‌های ارتباط:\n"
                              "Telegram: @Arena_Suppoort\n"
                              "Instagram: @arena_pc\n"
                              "Website: arenapc.ir")

    elif text == "/kolye":
        send_message(chat_id, "💎 قیمت کلیه لپ‌تاپ‌ها از ۸۰۰ هزار تومان به بالا هست.\n"
                              "برای دیدن موجودی روز، به @Arena_Suppoort پیام بده.")

    else:
        send_message(chat_id, "❓ دستور ناشناخته!\n"
                              "از /start استفاده کن تا لیست دستورات رو ببینی.")

    return "ok"

# -----------------------------
# صفحه تست
# -----------------------------
@app.route("/")
def home():
    return "🤖 Telegram Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
