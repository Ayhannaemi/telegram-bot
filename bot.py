from flask import Flask, request
import requests
import os
import openai

# -----------------------------
# تنظیمات
# -----------------------------
TOKEN = "8094291923:AAENXpm4aBXhIjIUx6_4tKuCKsiwmh9ssc8"
URL = f"https://api.telegram.org/bot{TOKEN}/"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # در Render یا هاست، ست کن
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
user_states = {}

# -----------------------------
# تابع ارسال پیام
# -----------------------------
def send_message(chat_id, text, keyboard=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if keyboard:
        payload["reply_markup"] = {
            "keyboard": keyboard,
            "resize_keyboard": True,
            "one_time_keyboard": False
        }
    requests.post(URL + "sendMessage", json=payload)

# -----------------------------
# پاسخ ChatGPT فارسی تخصصی
# -----------------------------
def chatgpt_reply(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "تو یک مشاور متخصص طراحی سایت، اپلیکیشن و برنامه‌نویسی هستی. پاسخ‌هایت را به زبان فارسی و با لحن مودبانه و تخصصی بده."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "⚠️ مشکلی در ارتباط با سرور مشاوره پیش آمد، لطفاً دوباره تلاش کن."

# -----------------------------
# وب‌هوک اصلی
# -----------------------------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "").strip()

    main_keyboard = [
        ["💻 خدمات", "💰 تعرفه‌ها"],
        ["📞 ارتباط با ما", "📂 نمونه کارها"],
        ["🧾 سفارش جدید", "🤖 مشاوره هوشمند Arena AI"]
    ]

    # حالت مشاوره ChatGPT
    if chat_id in user_states and user_states[chat_id] == "chatgpt":
        if text == "/exit":
            del user_states[chat_id]
            send_message(chat_id, "🚪 از حالت مشاوره خارج شدی.", keyboard=main_keyboard)
        else:
            reply = chatgpt_reply(text)
            send_message(chat_id, reply)
        return "ok"

    # دستورات اصلی
    if text == "/start":
        send_message(chat_id, "👋 سلام! خوش اومدی به <b>Arena PC</b>.\nاز منوی زیر انتخاب کن 👇", keyboard=main_keyboard)

    elif text == "💻 خدمات" or text == "/services":
        send_message(chat_id, "📋 خدمات ما:\n"
                              "1️⃣ طراحی سایت\n"
                              "2️⃣ طراحی اپلیکیشن موبایل\n"
                              "3️⃣ رابط کاربری (UI/UX)\n"
                              "4️⃣ پروژه‌های Python و JavaScript\n\n"
                              "برای سفارش، پیام بده: @Arena_Suppoort")

    elif text == "💰 تعرفه‌ها":
        send_message(chat_id, "💵 تعرفه‌ها:\n"
                              "🔹 سایت شرکتی: از ۳ میلیون تومان\n"
                              "🔹 اپلیکیشن اندروید: از ۵ میلیون تومان\n"
                              "🔹 طراحی UI/UX: از ۲ میلیون تومان")

    elif text == "📞 ارتباط با ما":
        send_message(chat_id, "📞 ارتباط با پشتیبانی:\nTelegram: @Arena_Suppoort\nInstagram: @arena_pc")

    elif text == "📂 نمونه کارها":
        send_message(chat_id, "🌐 مشاهده نمونه کارها:\nhttps://arenapc.ir")

    elif text == "🧾 سفارش جدید":
        send_message(chat_id, "✍️ لطفاً نوع سفارش خود را بنویس تا بررسی کنیم:\n(مثلاً طراحی سایت فروشگاهی یا اپلیکیشن اندروید)")

    elif text == "🤖 مشاوره هوشمند Arena AI":
        user_states[chat_id] = "chatgpt"
        send_message(chat_id, "💬 حالت مشاوره فعال شد!\nسؤالاتت درباره طراحی، برنامه‌نویسی یا سفارش رو بپرس.\nبرای خروج بنویس /exit")

    elif text == "/kolye":
        send_message(chat_id, "📿 قیمت گردنبند فی هشتصد هزار تومنه.\nبرای سفارش پیام بده: @Arena_Suppoort")

    else:
        send_message(chat_id, "❓ دستور ناشناخته! از منوی پایین استفاده کن.", keyboard=main_keyboard)

    return "ok"

# -----------------------------
# صفحه تست
# -----------------------------
@app.route("/")
def home():
    return "🤖 Arena PC Bot with AI is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
