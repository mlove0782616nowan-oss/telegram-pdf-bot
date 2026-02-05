import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
PDF_FOLDER = "pdfs"

bot = telebot.TeleBot(TOKEN)

user_files = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "📂 أهلاً بك\nاكتب /files لعرض ملفات PDF"
    )

@bot.message_handler(commands=['files'])
def list_files(message):
    if not os.path.exists(PDF_FOLDER):
        bot.send_message(message.chat.id, "❌ لا توجد ملفات")
        return

    files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]

    if not files:
        bot.send_message(message.chat.id, "📭 لا توجد ملفات PDF")
        return

    user_files[message.chat.id] = files

    markup = InlineKeyboardMarkup()
    for i, file in enumerate(files):
        markup.add(
            InlineKeyboardButton(
                text=file,
                callback_data=str(i)
            )
        )

    bot.send_message(
        message.chat.id,
        "📑 اختر ملفًا:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def send_pdf(call):
    chat_id = call.message.chat.id
    index = int(call.data)

    filename = user_files[chat_id][index]
    file_path = os.path.join(PDF_FOLDER, filename)

    with open(file_path, "rb") as pdf:
        bot.send_document(chat_id, pdf)

    bot.answer_callback_query(call.id, "📤 تم الإرسال")

print("🤖 البوت يعمل الآن 24/7")
bot.infinity_polling()
