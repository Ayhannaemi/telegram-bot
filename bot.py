from flask import Flask, request
import telegram
import os

# -----------------------------
# تنظیمات ربات
# -----------------------------
TOKEN = "8094291923:AAENXpm4aBXhIjIUx6_4tKuCKsiwmh9ssc8"
ADMIN_ID = 1026455806

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

# -----------------------------
# مسیر اصلی وبهوک
# -----------------------------
@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    if text == "/start":
        bot.send_message(chat_id=chat_id,
                         text="👋 سلام! من ربات خدمات طراحی و برنامه‌نویسی هستم.\n\n"
                              "می‌تونم توی طراحی سایت، برنامه‌نویسی و پروژه‌های نرم‌افزاری کمکت کنم 💻\n"
                              "برای دیدن خدمات، دستور /services رو بفرست.")
    elif text == "/services":
        bot.send_message(chat_id=chat_id,
                         text="📋 لیست خدمات ما:\n"
                              "1️⃣ طراحی سایت\n"
                              "2️⃣ طراحی اپلیکیشن موبایل\n"
                              "3️⃣ طراحی رابط کاربری (UI/UX)\n"
                              "4️⃣ برنامه‌نویسی پایتون و جاوااسکریپت\n\n"
                              "برای سفارش، پیام بده: @Ayhannaemi")
    else:
        bot.send_message(chat_id=chat_id,
                         text="❓ دستور ناشناخته!\nاز /start برای شروع استفاده کن.")

    return 'ok'

# -----------------------------
# صفحه اصلی (برای تست سرور)
# -----------------------------
@app.route('/')
def index():
    return "🤖 Telegram Bot is running!"

# -----------------------------
# اجرای ربات روی Render
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
