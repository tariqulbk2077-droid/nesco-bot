import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
# এখানে আমরা একটি AI লাইব্রেরি ব্যবহার করব যা সার্চ করতে পারে
import google.generativeai as genai 

# Koyeb Health Check
web_app = Flask('')
@web_app.route('/')
def home(): return "AI Bot is alive!"
def run(): web_app.run(host='0.0.0.0', port=8000)

# Gemini AI সেটিংস (এটি সার্চ এবং চ্যাট দুটাই করবে)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

async def handle_ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # বটকে একটু সময় দিতে হবে প্রসেস করার জন্য
    await update.message.reply_chat_action("typing")
    
    try:
        # AI কে বলা হচ্ছে ব্যবহারকারীর প্রশ্নের উত্তর দিতে (সার্চসহ)
        prompt = f"তুমি একজন সাহায্যকারী সহকারী। ব্যবহারকারী প্রশ্ন করেছে: {user_text}। যদি দাম বা তথ্য জানতে চায় তবে সঠিক ডাটা দাও, আর ক্যাজুয়াল কথা হলে বন্ধুসুলভ উত্তর দাও।"
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("দুঃখিত, আমি এখন উত্তর দিতে পারছি না। পরে চেষ্টা করুন।")

if __name__ == '__main__':
    threading.Thread(target=run).start()
    
    # টেলিগ্রাম বট টোকেন
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()
    
    # সব টেক্সট মেসেজ হ্যান্ডেল করবে
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_message))
    
    app.run_polling()
