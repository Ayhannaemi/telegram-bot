from flask import Flask, request
import requests
import os

TOKEN = "8094291923:AAENXpm4aBXhIjIUx6_4tKuCKsiwmh9ssc8"
URL = f"https://api.telegram.org/bot{TOKEN}/"
ADMIN_ID = 1026455806  # آیدی عددی خودت

app = Flask(__name__)

# برای نگه‌داری وضعیت هر کاربر
user_states = {}

def send_message(chat_id, text, buttons=None, keyboard=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}

    if buttons:
        payload["reply_markup"] = {"inline_keyboard": buttons}
    elif keyboard:
        payload["reply_markup"] = {
            "keyboard": keyboard,
            "resize_keyboard": True,
            "one_time_keyboard": False
        }

    requests.post(URL + "sendMessage", json=payload)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return "ok"

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "").strip()
        username = data["message"]["from"].get("username", "ناشناخته")

        main_keyboard = [
            ["💻 خدمات", "💰 تعرفه‌ها"],
            ["📞 ارتباط با ما", "📂 نمونه کارها"],
            ["🧾 سفارش جدید"]
        ]

        # اگر در حال پر کردن فرم هست
        if chat_id in user_states:
            state = user_states[chat_id]

            if state["step"] == "name":
                state["name"] = text
                state["step"] = "phone"
                send_message(chat_id, "📞 لطفاً شماره تماس خود را وارد کنید:")

            elif state["step"] == "phone":
                state["phone"] = text
                state["step"] = "project"
                send_message(chat_id, "🧠 نوع پروژه‌تان را بنویسید (مثلاً طراحی سایت یا اپلیکیشن):")

            elif state["step"] == "project":
                state["project"] = text
                send_message(chat_id, "✅ ممنون! اطلاعات شما ثبت شد.\n"
                                      "همکاران ما به زودی با شما تماس می‌گیرند 🙏",
                             keyboard=main_keyboard)

                # ارسال اطلاعات به ادمین
                message = (
                    "📩 سفارش جدید دریافت شد:\n\n"
                    f"👤 نام: {state['name']}\n"
                    f"📞 شماره: {state['phone']}\n"
                    f"💼 پروژه: {state['project']}\n"
                    f"🔗 کاربر: @{username}"
                )
                send_message(ADMIN_ID, message)

                del user_states[chat_id]

            return "ok"

        # دستورات عمومی
        if text == "/start":
            send_message(chat_id,
                         "👋 سلام! خوش اومدی به <b>Arena PC</b>.\n"
                         "از منوی پایین یکی از گزینه‌ها رو انتخاب کن 👇",
                         keyboard=main_keyboard)

        elif text == "🧾 سفارش جدید":
            user_states[chat_id] = {"step": "name"}
            send_message(chat_id, "🧾 لطفاً نام و نام خانوادگی خود را وارد کنید:")

        elif text == "💻 خدمات":
            buttons = [
                [{"text": "🌐 طراحی سایت", "callback_data": "web"}],
                [{"text": "📱 اپلیکیشن موبایل", "callback_data": "app"}],
                [{"text": "🎨 رابط کاربری (UI/UX)", "callback_data": "uiux"}],
            ]
            send_message(chat_id, "📋 لیست خدمات ما:", buttons=buttons)

        elif text == "💰 تعرفه‌ها":
            send_message(chat_id, "💵 تعرفه خدمات:\n"
                                  "🔹 طراحی سایت از ۳ میلیون تومان\n"
                                  "🔹 اپلیکیشن موبایل از ۵ میلیون تومان\n"
                                  "🔹 رابط کاربری از ۱.۵ میلیون تومان")

        elif text == "📞 ارتباط با ما":
            send_message(chat_id, "📞 راه‌های ارتباط:\n"
                                  "Telegram: @Arena_Suppoort\n"
                                  "Instagram: @arena_pc\n"
                                  "Website: arenapc.shop")

        elif text == "📂 نمونه کارها":
            send_message(chat_id, "📂 نمونه کارها:\n"
                                  "🌐 arenapc.shop\n"
                                  "💼 instagram.com/arena_pc")

        else:
            send_message(chat_id, "❓ دستور ناشناخته! از منوی پایین استفاده کن.", keyboard=main_keyboard)

    elif "callback_query" in data:
        query = data["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        data_id = query["data"]

        if data_id == "web":
            send_message(chat_id, "🌐 طراحی سایت شامل:\n"
                                  "✅ سایت فروشگاهی\n✅ سایت شخصی\n✅ سایت شرکتی\n\n"
                                  "برای سفارش پیام بده به @Arena_Suppoort")
        elif data_id == "app":
            send_message(chat_id, "📱 طراحی اپلیکیشن موبایل اندروید و iOS\n"
                                  "با پنل مدیریت و طراحی اختصاصی UI.\n"
                                  "برای سفارش پیام بده به @Arena_Suppoort")
        elif data_id == "uiux":
            send_message(chat_id, "🎨 طراحی رابط کاربری (UI/UX) مدرن و کاربرپسند\n"
                                  "مخصوص اپلیکیشن‌ها و وب‌سایت‌ها.\n"
                                  "برای مشاوره رایگان پیام بده: @Arena_Suppoort")

        requests.post(URL + "answerCallbackQuery", json={"callback_query_id": query["id"]})

    return "ok"

@app.route("/")
def home():
    return "🤖 Arena PC Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

