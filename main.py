import telebot
from telebot import types
import os

# ==================== क्रेडेंशियल्स ====================
BOT_TOKEN = "6227179254:AAHd7mtq55sxSlQAcEKuqwMDog74_3Z4Dzg"
ADMIN_ID = 1006157952  
QR_CODE_URL = "https://i.ibb.co/7JzK1hRv/IMG-20260913-223730-495.jpg" 
DB_FILE = "database.txt"
# ======================================================

bot = telebot.TeleBot(BOT_TOKEN)

# 📄 लोकल फाइल से बैलेंस पढ़ने और लिखने के फंक्शन्स
def read_all_balances():
    balances = {}
    if not os.path.exists(DB_FILE):
        return balances
    try:
        with open(DB_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    uid, bal = line.strip().split(":")
                    balances[int(uid)] = int(bal)
    except Exception as e:
        print(f"File Read Error: {e}")
    return balances

def save_all_balances(balances):
    try:
        with open(DB_FILE, "w") as f:
            for uid, bal in balances.items():
                f.write(f"{uid}:{bal}\n")
    except Exception as e:
        print(f"File Write Error: {e}")

def get_user_balance(user_id):
    balances = read_all_balances()
    return balances.get(user_id, 0)

def update_user_balance(user_id, amount):
    balances = read_all_balances()
    balances[user_id] = balances.get(user_id, 0) + amount
    save_all_balances(balances)
    return balances[user_id]

# 1. मुख्य होम मेनू कीबोर्ड
def main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_balance = types.KeyboardButton("BALANCE ✅")
    btn_add_fund = types.KeyboardButton("ADD FUND ✅")
    btn_obb = types.KeyboardButton("OBB & FILES")
    btn_hack = types.KeyboardButton("BGMI PAID HACK")
    
    markup.row(btn_balance, btn_add_fund)
    markup.row(btn_obb)
    markup.row(btn_hack)
    return markup

# OBB & FILES सब-मेनू
def obb_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("🛒 खरीदें PAID OBB (₹399)"))
    markup.row(types.KeyboardButton("🛒 खरीदें CUSTOMIZED OBB (₹599)"))
    markup.row(types.KeyboardButton("वापस जाएँ 🔙"))
    return markup

# HACK सब-मेनू
def hack_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("🛒 खरीदें Only ESP (₹599)"))
    markup.row(types.KeyboardButton("🛒 खरीदें Brutal HACK (₹1199)"))
    markup.row(types.KeyboardButton("वापस जाएँ 🔙"))
    return markup

# 🛒 ऑटोमैटिक कटौती लॉजिक
def process_balance_deduction(message, item_name, price, stock_data):
    user_id = message.from_user.id
    current_balance = get_user_balance(user_id)
    
    if current_balance >= price:
        new_balance = update_user_balance(user_id, -price)
        success_text = (
            "✅ *खरीदारी सफल रही!*\n\n"
            f"📦 *उत्पाद:* {item_name} (Full Season)\n"
            f"💸 *कटौती:* {price} RS\n"
            f"💰 *नया बैलेंस:* {new_balance} RS\n\n"
            f"{stock_data}"
        )
        bot.send_message(message.chat.id, success_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())
    else:
        bot.send_message(message.chat.id, f"❌ *बैलेंस कम है!*\n\n• आवश्यक: {price} RS\n• आपका बैलेंस: {current_balance} RS\n\nकृपया FUND बढ़ाने के लिए ADD FUND बटन दबाएं।")

# /start कमांड
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    # नए यूजर का डिफॉल्ट एंट्री सेव करना
    balances = read_all_balances()
    if user_id not in balances:
        balances[user_id] = 0
        save_all_balances(balances)
    bot.send_message(message.chat.id, "👋 आपका स्वागत है SpeedFistt स्टोर बॉट में!\n\nनीचे दिए गए बटन्स का उपयोग करके शॉपिंग करें।", reply_markup=main_menu_keyboard())

# इनपुट हैंडलर
@bot.message_handler(func=lambda message: True)
def handle_bot_operations(message):
    user_id = message.from_user.id
    
    # 💰 BALANCE चेक
    if message.text == "BALANCE ✅":
        balance = get_user_balance(user_id)
        bot.send_message(message.chat.id, f"💰 आपका मौजूदा बैलेंस है: *{balance} RS*", parse_mode="Markdown")
        
    # 💸 ADD FUND
    elif message.text == "ADD FUND ✅":
        fund_text = f"📌 *मैनुअल फंड जोड़ने की प्रक्रिया:*\n\n1. ऊपर दिए गए QR को स्कैन करें।\n2. स्क्रीनशॉट एडमिन को भेजें।\n\n🔑 *आपकी ID:* `{user_id}`\n📩 *Send Screenshot @SpeedFistt*"
        try:
            bot.send_photo(message.chat.id, QR_CODE_URL, caption=fund_text, parse_mode="Markdown")
        except:
            bot.send_message(message.chat.id, fund_text, parse_mode="Markdown")
        
    elif message.text == "OBB & FILES":
        bot.send_message(message.chat.id, "📁 उत्पाद चुनें (Full Season):", reply_markup=obb_menu_keyboard())
    elif message.text == "BGMI PAID HACK":
        bot.send_message(message.chat.id, "⚡ हैक चुनें (Full Season):", reply_markup=hack_menu_keyboard())
    elif message.text == "वापस जाएँ 🔙":
        bot.send_message(message.chat.id, "🔙 मुख्य मेनू:", reply_markup=main_menu_keyboard())

    # उत्पाद ऑटो-कटौती बटन्स
    elif message.text == "🛒 खरीदें PAID OBB (₹399)":
        process_balance_deduction(message, "PAID OBB & FILES", 399, "🔥 *आपका PAID OBB लिंक:* https://example.com")
    elif message.text == "🛒 खरीदें CUSTOMIZED OBB (₹599)":
        process_balance_deduction(message, "CUSTOMIZED OBB", 599, "🔥 *आपका CUSTOMIZED OBB लिंक:* https://example.com")
    elif message.text == "🛒 खरीदें Only ESP (₹599)":
        process_balance_deduction(message, "Only ESP Hack", 599, "🔥 *आपकी ESP HACK की (Key):* ESP-KEY-XXXX-XXXX")
    elif message.text == "🛒 खरीदें Brutal HACK (₹1199)":
        process_balance_deduction(message, "Brutal HACK", 1199, "🔥 *आपकी BRUTAL HACK की (Key):* BRUTAL-KEY-XXXX-XXXX")

# 👑 एडमिन कमांड: मैनुअल फंड जोड़ना
@bot.message_handler(commands=['add'])
def admin_add_balance(message):
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()
    if len(args) < 3:
        bot.send_message(message.chat.id, "⚠️ Format: `/add [User_ID] [Amount]`")
        return
    try:
        target_user = int(args[1])
        amount = int(args[2])
        
        # फाइल डेटाबेस में बैलेंस जोड़ना
        new_balance = update_user_balance(target_user, amount)
        
        bot.send_message(message.chat.id, f"✅ यूजर `{target_user}` के खाते में {amount} RS जोड़ दिए गए हैं।")
        bot.send_message(target_user, f"🎉 एडमिन @SpeedFistt ने आपके खाते में *{amount} RS* जोड़ दिए हैं! अपना BALANCE चेक करें।", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ एरर: {str(e)}")

print("🤖 SpeedFistt स्टोर बॉट सफलतापूर्वक चालू है...")
bot.infinity_polling()
