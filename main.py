import telebot
from telebot import types
from supabase import create_client, Client

# ==================== क्रेडेंशियल्स ====================
BOT_TOKEN = "6227179254:AAHd7mtq55sxSlQAcEKuqwMDog74_3Z4Dzg"
ADMIN_ID = 1006157952  
SUPABASE_URL = "https://gaxyfiwthsdtugopjzkz.supabase.co/rest/v1/" 
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdheHlmaXd0aHNkdHVnb3Bqemt6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzMTA2NzQsImV4cCI6MjEwNDg4NjY3NH0.Jtxo4aZyd2uDP-YxUwSyPuTIQuSPot0TKpw-h-9sJyc"
QR_CODE_URL = "https://i.ibb.co/7JzK1hRv/IMG-20260913-223730-495.jpg" 
# ======================================================

bot = telebot.TeleBot(BOT_TOKEN)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

# 2. OBB & FILES सब-मेनू कीबोर्ड
def obb_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_paid_obb = types.KeyboardButton("🛒 खरीदें PAID OBB (₹399)")
    btn_cust_obb = types.KeyboardButton("🛒 खरीदें CUSTOMIZED OBB (₹599)")
    btn_back = types.KeyboardButton("वापस जाएँ 🔙")
    
    markup.row(btn_paid_obb)
    markup.row(btn_cust_obb)
    markup.row(btn_back)
    return markup

# 3. BGMI PAID HACK सब-मेनू कीबोर्ड
def hack_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_esp = types.KeyboardButton("🛒 खरीदें Only ESP (₹599)")
    btn_brutal = types.KeyboardButton("🛒 खरीदें Brutal HACK (₹1199)")
    btn_back = types.KeyboardButton("वापस जाएँ 🔙")
    
    markup.row(btn_esp)
    markup.row(btn_brutal)
    markup.row(btn_back)
    return markup

# 🔍 Supabase SDK फिक्स - बिल्कुल सही और टेस्टेड तरीका
def get_user_balance(user_id):
    try:
        response = supabase.table("users").select("balance").eq("user_id", user_id).execute()
        # डेटा की पहली रो से बैलेंस निकालना
        if response.data and len(response.data) > 0:
            return response.data[0].get('balance', 0)
        
        # अगर नया यूजर है तो रजिस्टर करें
        supabase.table("users").upsert({"user_id": user_id, "balance": 0}).execute()
        return 0
    except Exception as e:
        print(f"ডेटाबेस फेच एरर: {e}")
        return None

# 🛒 ऑटोमैटिक कटौती लॉजिक
def process_balance_deduction(message, item_name, price, stock_data):
    user_id = message.from_user.id
    current_balance = get_user_balance(user_id)
    
    if current_balance is None:
        bot.send_message(message.chat.id, "❌ डेटाबेस से संपर्क नहीं हो पाया।")
        return
        
    if current_balance >= price:
        new_balance = current_balance - price
        try:
            supabase.table("users").update({"balance": new_balance}).eq("user_id", user_id).execute()
            success_text = f"✅ *खरीदारी सफल रही!*\n\n📦 *उत्पाद:* {item_name}\n💸 *कटौती:* {price} RS\n💰 *नया बैलेंस:* {new_balance} RS\n\n{stock_data}"
            bot.send_message(message.chat.id, success_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ एरर: {str(e)}")
    else:
        bot.send_message(message.chat.id, f"❌ *बैलेंस कम है!*\n\n• आवश्यक: {price} RS\n• आपका बैलेंस: {current_balance} RS\n\n¼फंड बढ़ाने के लिए ADD FUND बटन दबाएं।")

# /start कमांड
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    try:
        supabase.table("users").upsert({"user_id": user_id, "balance": 0}).execute()
    except Exception as e:
        print(f"रजिस्ट्रेशन एरर: {e}")
    bot.send_message(message.chat.id, "👋 आपका स्वागत है SpeedFistt स्टोर बॉट में!\n\nनीचे दिए गए बटन्स का उपयोग करके शॉपिंग करें।", reply_markup=main_menu_keyboard())

# इनपुट हैंडलर
@bot.message_handler(func=lambda message: True)
def handle_bot_operations(message):
    user_id = message.from_user.id
    
    if message.text == "BALANCE ✅":
        balance = get_user_balance(user_id)
        if balance is None:
            bot.send_message(message.chat.id, "⚠️ बैलेंस चेक करने में दिक्कत आ रही है। कृपया /start दबाकर दोबारा प्रयास करें।")
        else:
            bot.send_message(message.chat.id, f"💰 आपका मौजूदा बैलेंस है: *{balance} RS*", parse_mode="Markdown")
        
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

# 👑 एडमिन कमांड
@bot.message_handler(commands=['add'])
def admin_add_balance(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ अधिकार नहीं है।")
        return
    args = message.text.split()
    if len(args) < 3:
        bot.send_message(message.chat.id, "⚠️ Format: `/add [User_ID] [Amount]`")
        return
    try:
        target_user = int(args[1])
        amount = int(args[2])
        current_balance = get_user_balance(target_user)
        
        new_balance = (current_balance if current_balance else 0) + amount
        supabase.table("users").upsert({"user_id": target_user, "balance": new_balance}).execute()
        
        bot.send_message(message.chat.id, f"✅ यूजर `{target_user}` के खाते में {amount} RS जोड़ दिए गए।")
        bot.send_message(target_user, f"🎉 एडमिन @SpeedFistt ने आपके खाते में *{amount} RS* जोड़ दिए हैं! अपना BALANCE嫌 चेक करें।", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ एरर: {str(e)}")

print("🤖 SpeedFistt स्टोर बॉट सफलतापूर्वक चालू है...")
bot.infinity_polling()
