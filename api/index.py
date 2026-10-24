import os
from flask import Flask, request
import telebot
import google.generativeai as genai
from PIL import Image
import io

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    return "Bot is active and running!", 200

@bot.message_handler(content_types=['photo'])
def handle_chart_image(message):
    try:
        wait_msg = bot.reply_to(message, "⏳ جاري قراءة الشموع وتحليل البيانات عبر نموذج الرؤية الذكي...")

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        image = Image.open(io.BytesIO(downloaded_file))

        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = (
            "أنت محلل فني محترف وأستاذ في تداول العملات والذهب (Forex & Crypto). "
            "قم بتحليل الشارت المرفقة بدقة عالية، وتضمن في تحليلك:\n"
            "1. تحديد زوج العملات أو الأصول وظروف السوق.\n"
            "2. اتجاه الشموع والمؤشرات الظاهرة (دعم ومقاومة).\n"
            "3. قراءة مؤشرات العزم الظاهرة.\n"
            "4. إعطاء توصية أو قرار تداول مقترح (شراء/بيع) مع الأسباب باختصار."
        )

        response = model.generate_content([prompt, image])
        analysis_result = response.text

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=wait_msg.message_id,
            text=f"📊 **التحليل الفني للـشارت (Gemini Vision):**\n\n{analysis_result}",
            parse_mode='Markdown'
        )
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ:\n`{str(e)}`", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "أهلاً بك! يرجى إرسال **صورة شارت (Screenshot)** ليقوم الذكاء الاصطناعي بتحليلها فوراً.")
