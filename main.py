import os
import time
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_nesco_data(meter_no):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://customer.nesco.gov.bd/")
        time.sleep(2)
        
        # মিটার নম্বর ইনপুট
        driver.find_element(By.ID, "reference_no").send_keys(meter_no)
        
        # রিচার্জ হিস্ট্রি ক্লিক
        driver.find_element(By.XPATH, "//button[contains(text(), 'রিচার্জ হিস্ট্রি')]").click()
        time.sleep(3)
        
        # ডাটা সংগ্রহ
        name = driver.find_element(By.ID, "customer_name").get_attribute("value")
        consumer = driver.find_element(By.ID, "customer_no").get_attribute("value")
        balance = driver.find_element(By.ID, "current_balance").get_attribute("value")
        
        # রিচার্জ টেবিলের প্রথম রো এর ডাটা
        last_recharge = driver.find_element(By.XPATH, "//table[@id='recharge_history_table']/tbody/tr[1]").text
        
        return f"👤 নাম: {name}\n🆔 কনজ্যুমার নং: {consumer}\n💰 ব্যালেন্স: {balance} টাকা\n🕒 লাস্ট হিস্ট্রি: {last_recharge}"
    except:
        return "❌ তথ্য পাওয়া যায়নি। নম্বরটি সঠিক কিনা চেক করুন।"
    finally:
        driver.quit()

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    await update.message.reply_text("অপেক্ষা করুন, ডাটা আনা হচ্ছে...")
    result = get_nesco_data(msg)
    await update.message.reply_text(result)

if __name__ == '__main__':
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT, reply))
    app.run_polling()
  
