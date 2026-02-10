import os
import telebot
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 1. إعداد الخادم الوهمي لإرضاء Koyeb
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Healthy")

def run_health_server():
    # Koyeb يستخدم المنفذ 8080 افتراضياً
    server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    server.serve_forever()

# تشغيل الخادم في خلفية البوت
threading.Thread(target=run_health_server, daemon=True).start()

# 2. إعدادات البوت
TOKEN = "7957280620:AAF1qTJriuHm8y3x0oQ5SVlnI39iGzcNlbQ"
bot = telebot.TeleBot(TOKEN)
PDF_FOLDER = "."
user_files = {}

@bot.message_handler(commands=['start', 'files'])
def start(message):
    files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
    if not files:
        bot.send_message(message.chat.id, "❌ لا توجد ملفات PDF.")
        return
    user_files[message.chat.id] = files
    markup = InlineKeyboardMarkup()
    for i, file in enumerate(files):
        markup.add(InlineKeyboardButton(text=file, callback_data=str(i)))
    bot.send_message(message.chat.id, "📂 اختر ملفك:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def send_pdf(call):
    chat_id = call.message.chat.id
    index = int(call.data)
    files = user_files.get(chat_id)
    if files and index < len(files):
        with open(os.path.join(PDF_FOLDER, files[index]), "rb") as pdf:
            bot.send_document(chat_id, pdf)

print("🤖 البوت يعمل الآن على Koyeb...")
bot.infinity_polling()
