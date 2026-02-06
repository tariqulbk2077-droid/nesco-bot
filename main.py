import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Koyeb-এর জন্য ওয়েব সার্ভার
web_app = Flask('')
@web_app.route('/')
def home(): return "Bot Active"
def run(): web_app.run(host='0.0.0.0', port=8000)

# Gemini AI সেটআপ
gemini_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-1.5-flash')

async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    if not user_msg: return
    
    await update.message.reply_chat_action("typing")
    
    try:
        # AI কে তথ্য ও চ্যাটিংয়ের জন্য প্রম্পট দেওয়া
        prompt = f"ব্যবহারকারী বলেছে: {user_msg}। তুমি একজন স্মার্ট অ্যাসিস্ট্যান্ট হিসেবে তাকে বাংলায় উত্তর দাও।"
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        # এপিআই কী মিসিং থাকলে বা এরর হলে এই মেসেজ দেখাবে
        await update.message.reply_text("এপিআই কী (API Key) সঠিক নেই অথবা সার্ভারে সমস্যা হচ্ছে।")

if __name__ == '__main__':
    threading.Thread(target=run).start()
    
    bot_token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(bot_token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))
    app.run_polling()
