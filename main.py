import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Koyeb Health Check-এর জন্য ছোট সার্ভার
web_app = Flask('')
@web_app.route('/')
def home(): return "AI Bot is Running!"
def run(): web_app.run(host='0.0.0.0', port=8000)

# Gemini AI সেটআপ
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash') # লেটেস্ট এবং ফাস্ট মডেল

async def handle_ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text: return

    await update.message.reply_chat_action("typing")
    
    try:
        # AI কে নির্দেশ দেওয়া হচ্ছে কীভাবে কথা বলবে
        prompt = f"তুমি একজন বন্ধুত্বপূর্ণ বাঙালি সহকারী। ব্যবহারকারী বলেছে: '{user_text}'। তার সাথে বন্ধুসুলভভাবে কথা বলো এবং প্রয়োজনীয় তথ্য বা দাম জানাও।"
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("দুঃখিত বন্ধু, আমি এই মুহূর্তে উত্তরটি খুঁজে পাচ্ছি না। একটু পরে আবার বলবে কি?")

if __name__ == '__main__':
    # পোর্ট ৮০০০ সচল রাখা
    threading.Thread(target=run).start()
    
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_message))
    app.run_polling()
