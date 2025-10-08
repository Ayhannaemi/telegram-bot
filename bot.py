from flask import Flask, request
import requests
import os

TOKEN = "8094291923:AAENXpm4aBXhIjIUx6_4tKuCKsiwmh9ssc8"
URL = f"https://api.telegram.org/bot{TOKEN}/"
ADMIN_ID = 1026455806  # آیدی عددی خودت

# لینک زرین‌پال و Merchant
ZARINPAL_MERCHANT = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
ZARINPAL_BASE = "https://www.zarinpal.com/pg/StartPay/"
ZARINPAL_VERIFY = "https://www.zarinpal.com/pg/PaymentVerification.json"

app = Flask(__name__)
user_states = {}

# مبلغ ثابت خدمات
SERVICE_PRICES = {
    "web": 3000000,
    "app": 5000000,
    "uiux": 1500000
}

# نگهداری وضعیت پرداخت‌ها
pending_payments = {}  # chat_id: service_id

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

def create_payment_link(chat_id, service_id):
    amount = SERVICE_PRICES[service_id]
    pending_payments[chat_id] = service_id
    return f"{ZARINPAL_BASE}{ZARINPAL_MERCHANT}?amount={amount}&callback_url=https://YOUR_DOMAIN.com/verify/{chat_id}"

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

        if chat_id in user_states:
            state = user_states[chat_id]
            if state["step"] == "name":
                state["name"] = text
                state["step"] = "phone"
                send_message(chat_id, "📞 لطفاً شماره تماس خود را وارد کنید:")
            elif state["step"] == "phone":
                state["phone"] = text
                state["step"] = "project"
                send_message(chat_id, "🧠 نوع پروژه‌تان را بنویسید:")
            elif state["step"] == "project":
                state["project"] = text
                send_message(chat_id, "✅ اطلاعات ثبت شد. حالا خدمت موردنظر را انتخاب و پرداخت کنید 🙏",
                             keyboard=main_keyboard)

                message = (
                    f"📩 سفارش جدید دریافت شد:\n"
                    f"👤 نام: {state['name']}\n"
                    f"📞 شماره: {state['phone']}\n"
                    f"💼 پروژه: {state['project']}\n"
                    f"🔗 کاربر: @{username}"
                )
                send_message(ADMIN_ID, message)
                del user_states[chat_id]
            return "ok"

        if text == "/start":
            send_message(chat_id, "👋 سلام! خوش اومدی به <b>Arena PC</b>.\nاز منوی پایین یکی از گزینه‌ها رو انتخاب کن 👇",
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
            send_message(chat_id, "📞 راه‌های ارتباط:\nTelegram: @Arena_Suppoort\nInstagram: @arena_pc\nWebsite: arenapc.shop")
        elif text == "📂 نمونه کارها":
            send_message(chat_id, "📂 نمونه کارها:\n🌐 arenapc.shop\n💼 instagram.com/arena_pc")
        else:
            send_message(chat_id, "❓ دستور ناشناخته! از منوی پایین استفاده کن.", keyboard=main_keyboard)

    elif "callback_query" in data:
        query = data["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        data_id = query["data"]

        if data_id in SERVICE_PRICES:
            link = create_payment_link(chat_id, data_id)
            send_message(chat_id, f"💳 برای پرداخت خدمت <b>{data_id}</b>، روی لینک زیر کلیک کنید:\n{link}")
        requests.post(URL + "answerCallbackQuery", json={"callback_query_id": query["id"]})

    return "ok"

# تایید پرداخت
@app.route("/verify/<int:chat_id>", methods=["GET"])
def verify(chat_id):
    if chat_id not in pending_payments:
        return "❌ پرداخت نامعتبر یا تکراری"

    service_id = pending_payments[chat_id]
    amount = SERVICE_PRICES[service_id]

    # اینجا باید درخواست واقعی به زرین‌پال بزنیم (نمونه فرضی)
    # response = requests.post(ZARINPAL_VERIFY, json={"merchant_id": ZARINPAL_MERCHANT, "amount": amount})
    # success = response.json().get("status") == 100
    success = True  # فرض می‌کنیم پرداخت موفق است

    if success:
        send_message(chat_id, f"✅ پرداخت خدمت <b>{service_id}</b> با موفقیت انجام شد. با تشکر!")
        send_message(ADMIN_ID, f"💰 کاربر @{chat_id} پرداخت خدمت <b>{service_id}</b> را انجام داد.")
        del pending_payments[chat_id]
        return "پرداخت موفق ✅"
    else:
        return "❌ پرداخت موفق نبود"

@app.route("/")
def home():
    return "🤖 Arena PC Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
