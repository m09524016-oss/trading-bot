import os
import telebot
from telebot import types
import google.generativeai as genai
from PIL import Image
import io

# جلب توكن التيليغرام ومفتاح الذكاء الاصطناعي من متغيرات البيئة
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# التحقق من وجود المفاتيح
if not GEMINI_API_KEY:
    print("تحذير: مفتاح GEMINI_API_KEY غير معد في إعدادات البيئة!")

# إعداد مكتبة جوجل للذكاء الاصطناعي
genai.configure(api_key=GEMINI_API_KEY)

# تهيئة بوت التيليغرام
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 **مرحباً بك في بوت تحليل الشارتات الفني (Gemini Vision)**\n\n"
        "قم بإرسال أو رفع صورة لقططة شاشة (Screenshot) لأي شارت تداول (Forex, Crypto, Gold)، "
        "وسيقوم الذكاء الاصطناعي فوراً بقراءة الشموع والمؤشرات وإعطائك قراراً فنياً احترافياً!"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_chart_image(message):
    try:
        # إرسال رسالة انتظار للمستخدم
        wait_msg = bot.reply_to(message, "⏳ جاري قراءة الشموع وتحليل البيانات عبر نموذج الرؤية الذكي...")

        # الحصول على أعلى دقة للصورة المرفقة
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # فتح الصورة باستخدام مكتبة PIL
        image = Image.open(io.BytesIO(downloaded_file))

        # استخدام أحدث نموذج مدعوم للرؤية
        model = genai.GenerativeModel('gemini-2.5-flash')

        # موجه الأوامر (Prompt) المخصص للتحليل الفني
        prompt = (
            "أنت محلل فني محترف وأستاذ في تداول العملات والذهب (Forex & Crypto). "
            "قم بتحليل لقطة الشاشة (الشارت) المرفقة بدقة عالية، وتضمن في تحليلك:\n"
            "1. تحديد زوج العملات أو الأصول وظروف السوق الحالية.\n"
            "2. اتجاه الشموع والمؤشرات الظاهرة (مثل الاتجاه العام ودعم ومقاومة).\n"
            "3. قراءة مؤشرات العزم أو الاتجاه الظاهرة في الشارت.\n"
            "4. إعطاء توصية أو قرار تداول مقترح (شراء/بيع) مع الأسباب باختصار واحترافية."
        )

        # توليد التحليل من النموذج
        response = model.generate_content([prompt, image])
        
        analysis_result = response.text

        # تعديل رسالة الانتظار وإرسال النتيجة النهائية
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=wait_msg.message_id,
            text=f"📊 **التحليل الفني للـشارت (Gemini Vision):**\n\n{analysis_result}",
            parse_mode='Markdown'
        )

    except Exception as e:
        error_msg = str(e)
        if "GEMINI_API_KEY" in error_msg or "API_KEY_INVALID" in error_msg:
            bot.reply_to(message, "❌ خطأ: مفتاح الذكاء الاصطناعي (GEMINI_API_KEY) غير معد بشكل صحيح في إعدادات السيرفر.")
        else:
            bot.reply_to(message, f"❌ حدث خطأ أثناء معالجة الصورة:\n`{error_msg}`", parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "أهلاً بك! يرجى إرسال **صورة شارت (Screenshot)** ليقوم الذكاء الاصطناعي بتحليلها فوراً.")

if __name__ == '__main__':
    print("البوت يعمل الآن...")
    bot.infinity_polling()
