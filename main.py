import os
import time
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Koyeb Health Check এর জন্য Flask সার্ভার
web_app = Flask('')

@web_app.route('/')
def home():
    return "Bot is active!"

def run():
    web_app.run(host='0.0.0.0', port=8000)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# NESCO স্ক্র্যাপিং ফাংশন
def get_nesco_data(meter_no):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://customer.nesco.gov.bd/")
        time.sleep(3)
        
        # মিটার নম্বর ইনপুট বক্স খুঁজে বের করা
        input_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='গ্রাহক নম্বর']")
        input_box.send_keys(meter_no)
        
        # রিচার্জ হিস্ট্রি বাটন ক্লিক
        btn = driver.find_element(By.XPATH, "//button[contains(text(), 'রিচার্জ হিস্ট্রি')]")
        btn.click()
        time.sleep(5) # ডাটা লোড হতে সময় দিন
        
        # ডাটা সংগ্রহ
        res_name = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div/input").get_attribute("value")
        res_balance = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[6]/div/input").get_attribute("value")
        
        return f"👤 নাম: {res_name}\n💰 ব্যালেন্স: {res_balance} টাকা"
    except Exception as e:
        return "❌ তথ্য খুঁজে পাওয়া যায়নি। সাইটে সমস্যা বা নম্বরটি ভুল হতে পারে।"
    finally:
        driver.quit()

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    meter = update.message.text
    if meter.isdigit():
        await update.message.reply_text(f"অপেক্ষা করুন, {meter} এর তথ্য খোঁজা হচ্ছে...")
        result = get_nesco_data(meter)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("দয়া করে সঠিক মিটার নম্বরটি লিখুন।")

if __name__ == '__main__':
    keep_alive() # ৮০০০ পোর্ট সচল করবে
    
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app.run_polling()
    
