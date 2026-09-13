import telebot
from telebot import types
from supabase import create_client, Client

# ==================== क्रेडेंशियल्स ====================
BOT_TOKEN = "6227179254:AAHd7mtq55sxSlQAcEKuqwMDog74_3Z4Dzg"
ADMIN_ID = 1006157952  
SUPABASE_URL = "https://gaxyfiwthsdtugopjzkz.supabase.co/rest/v1/" 
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdheHlmaXd0aHNkdHVnb3Bqemt6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzMTA2NzQsImV4cCI6MjEwNDg4NjY3NH0.Jtxo4aZyd2uDP-YxUwSyPuTIQuSPot0TKpw-h-9sJyc"

# टेलीग्राम कंपैटिबल डायरेक्ट इमेज लिंक
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

# Safe Balance Extractor function
def get_user_balance(user_id):
    try:
        response = supabase.table("users").select("balance").eq("user_id", user_id).execute()
        if response.data and len(response.data) > 0:
            # सुरक्षित तरीका: डिक्शनरी या लिस्ट फॉर्मेट दोनों को चेक करना
            data_row = response.data[0]
            if isinstance(data_row, dict):
                return data_row.get('balance', 0)
        return 0
    except Exception as e:
        print(f"Database Fetch Error: {e}")
        return None

# 🔥 ऑटोमैटिक बैलेंस कटौती
def process_balance_deduction(message, item_name, price, stock_data):
    user_id = message.from_user.id
    current_balance = get_user_balance(user_id)
    
    if current_balance is None:
        bot.send_message(message.chat.id, "❌ डेटाबेस से संपर्क नहीं हो पा रहा है। कृपया कुछ समय बाद प्रयास करें।")
        return
        
    if current_balance >= price:
        new_balance = current_balance - price
        try:
            supabase.table("users").update({"balance": new_balance}).eq("user_id", user_id).execute()
            success_text = (
                "✅ *खरीदारी सफल रही!*\n\n"
                f"📦 *उत्पाद:* {item_name} (Full Season)\n"
                f"💸 *कटौती:* {price} RS\n"
                f"💰 *नया बैलेंस:* {new_balance} RS\n\n"
                f"{stock_data}"
            )
            bot.send_message(message.chat.id, success_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ बैलेंस अपडेट करने में त्रुटि: {str(e)}")
    else:
        bot.send_message(message.chat.id, f"❌ *बैलेंस कम है!*\n\nआवश्यक: {price} RS\nआपका बैलेंस: {current_balance} RS\n\nकृपया ADD FUND बटन दबाकर बैलेंस बढ़ाएं।")

# /start कमांड
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    try:
        supabase.table("users").upsert({"user_id": user_id}).execute()
    except Exception as e:
        print(f"रजिस्ट्रेशन एरर: {e}")
        
    welcome_text = "👋 आपका स्वागत है SpeedFistt स्टोर बॉट में!\n\nनीचे दिए गए बटन्स का उपयोग करके शॉपिंग करें।"
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_keyboard())

# मुख्य बटन्स और इनपुट हैंडलर
@bot.message_handler(func=lambda message: True)
def handle_bot_operations(message):
    user_id = message.from_user.id
    
    # 💰 BALANCE चेक
    if message.text == "BALANCE ✅":
        balance = get_user_balance(user_id)
        if balance is None:
            bot.send_message(message.chat.id, "⚠️ बैलेंस चेक करने में दिक्कत आ रही है। कृपया /start दबाकर दोबारा प्रयास करें।")
        else:
            bot.send_message(message.chat.id, f"💰 आपका मौजूदा बैलेंस है: *{balance} RS*", parse_mode="Markdown")
        
    # 💸 ADD FUND 
    elif message.text == "ADD FUND ✅":
        fund_text = (
            "📌 *मैनुअल फंड जोड़ने की प्रक्रिया:*\n\n"
            "1. ऊपर दिए गए QR कोड को स्कैन करके पेमेंट करें।\n"
            "2. पेमेंट करने के बाद स्क्रीनशॉट और अपनी टेलीग्राम ID एडमिन को भेजें।\n\n"
            f"🔑 *आपकी टेलीग्राम ID:* `{user_id}` (इसे कॉपी करके भेजें)\n\n"
            "📩 *Send Screenshot @SpeedFistt*"
        )
        try:
            bot.send_photo(message.chat.id, QR_CODE_URL, caption=fund_text, parse_mode="Markdown")
        except Exception as e:
            # अगर टेलीग्राम इमेज लिंक रिजेक्ट करता है, तो सीधे लिंक को टेक्स्ट में शामिल करके भेजें
            fallback_text = f"🖼️ *पेमेंट QR कोड लिंक:* {QR_CODE_URL}\n\n" + fund_text
            bot.send_message(message.chat.id, fallback_text, parse_mode="Markdown")
        
    # 📁 OBB & FILES मेनू
    elif message.text == "OBB & FILES":
        bot.send_message(message.chat.id, "📁 *OBB & FILES सेक्शन:*\nनीचे मेनू से अपनी पसंद का उत्पाद चुनें (Full Season):", reply_markup=obb_menu_keyboard())
        
    # ⚡ BGMI PAID HACK मेनू
    elif message.text == "BGMI PAID HACK":
        bot.send_message(message.chat.id, "⚡ *BGMI PAID HACK सेक्शन:*\nनीचे मेनू से अपना हैक चुनें (Full Season):", reply_markup=hack_menu_keyboard())
        
    # 🔙 वापस मुख्य मेनू
    elif message.text == "वापस जाएँ 🔙":
        bot.send_message(message.chat.id, "🔙 आप मुख्य मेनू पर लौट आए हैं:", reply_markup=main_menu_keyboard())

    # ==================== उत्पाद ऑटो-कटौती बटन्स ====================
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
        bot.send_message(message.chat.id, "❌ आपके पास इस कमांड का अधिकार नहीं है।")
        return
        
    args = message.text.split()
    if len(args) < 3:
        bot.send_message(message.chat.id, "⚠️ सही फॉर्मेट: `/add [User_ID] [Amount]`")
        return
        
    try:
        target_user = int(args[1])
        amount = int(args[2])
        
        current_balance = get_user_balance(target_user)
        if current_balance is None:
            # अगर यूजर पहली बार आया है और रजिस्टर्ड नहीं है
            supabase.table("users").upsert({"user_id": target_user, "balance": amount}).execute()
            new_balance = amount
        else:
            new_balance = current_balance + amount
            supabase.table("users").update({"balance": new_balance}).eq("user_id", target_user).execute()
        
        bot.send_message(message.chat.id, f"✅ यूजर `{target_user}` के खाते में {amount} RS जोड़ दिए गए हैं।")
        bot.send_message(target_user, f"🎉 एडमिन @SpeedFistt ने आपके खाते में *{amount} RS* जोड़ दिए हैं! अपना BALANCE चेक करें।", parse_mode="Markdown")
        
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ ID और Amount केवल नंबर होने चाहिए।")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ एरर: {str(e)}")

print("🤖 SpeedFistt स्टोर बॉट सफलतापूर्वक चालू है...")
bot.infinity_polling()
