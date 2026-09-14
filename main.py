import telebot
from telebot import types

# ==================== क्रेडेंशियल्स ====================
BOT_TOKEN = "6227179254:AAHd7mtq55sxSlQAcEKuqwMDog74_3Z4Dzg"
ADMIN_ID = 1006157952  
QR_CODE_URL = "https://i.ibb.co/7JzK1hRv/IMG-20260913-223730-495.jpg" 

# ⚠️ यहाँ अपने बनाए गए प्राइवेट चैनल की ID डालें (माइनस चिन्ह के साथ)
# ध्यान दें: अगर आपकी आईडी -100 से शुरू होती है, तो उसे पूरा माइनस के साथ लिखें
CHANNEL_ID = -1003892586354  
# ======================================================

bot = telebot.TeleBot(BOT_TOKEN)

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

# 🔍 चैनल के इतिहास को स्कैन करके लाइव बैलेंस निकालने का 100% सही तरीका
def get_user_balance(user_id):
    total_balance = 0
    try:
        # चैनल के आखिरी 1000 संदेशों का इतिहास निकालना
        messages = bot.get_chat_history(CHANNEL_ID, limit=1000)
        
        # संदेशों को पुराने से नए (नीचे से ऊपर) के क्रम में गिनना
        for msg in reversed(messages):
            if msg.text:
                text_str = str(msg.text).strip()
                # फ़ॉर्मेट चेक करना: ADD:USER_ID:AMOUNT
                if text_str.startswith("ADD:"):
                    parts = text_str.split(":")
                    if len(parts) == 3 and int(parts[1]) == user_id:
                        total_balance += int(parts[2])
                # फ़ॉर्मेट चेक करना: BUY:USER_ID:AMOUNT
                elif text_str.startswith("BUY:"):
                    parts = text_str.split(":")
                    if len(parts) == 3 and int(parts[1]) == user_id:
                        total_balance -= int(parts[2])
                        
        return total_balance
    except Exception as e:
        print(f"चैनल से बैलेंस पढ़ने में तकनीकी त्रुटि: {e}")
        return 0

# 🛒 ऑटोमैटिक कटौती लॉजिक (चैनल एंट्री के साथ)
def process_balance_deduction(message, item_name, price, stock_data):
    user_id = message.from_user.id
    current_balance = get_user_balance(user_id)
    
    if current_balance >= price:
        try:
            # कटौती का रिकॉर्ड प्राइवेट चैनल में 'BUY:यूजर:प्राइस' के रूप में भेजना
            bot.send_message(CHANNEL_ID, f"BUY:{user_id}:{price}")
            
            new_balance = current_balance - price
            success_text = (
                "✅ *खरीदारी सफल रही!*\n\n"
                f"📦 *उत्पाद:* {item_name} (Full Season)\n"
                f"💸 *कटौती:* {price} RS\n"
                f"💰 *नया बैलेंस:* {new_balance} RS\n\n"
                f"{stock_data}"
            )
            bot.send_message(message.chat.id, success_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ कटौती रिकॉर्ड चैनल में दर्ज नहीं हो पाया: {str(e)}")
    else:
        bot.send_message(message.chat.id, f"❌ *बैलेंस कम है!*\n\n• आवश्यक: {price} RS\n• आपका बैलेंस: {current_balance} RS\n\nकृपया FUND बढ़ाने के लिए ADD FUND बटन दबाएं।")

# /start कमांड
@bot.message_handler(commands=['start'])
def start_command(message):
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
        
        # फंड जोड़ने का रिकॉर्ड 'ADD:यूजर:अमाउंट' के रूप में सीधे चैनल में भेजना
        bot.send_message(CHANNEL_ID, f"ADD:{target_user}:{amount}")
        
        bot.send_message(message.chat.id, f"✅ यूजर `{target_user}` के खाते में {amount} RS जोड़ दिए गए हैं।")
        bot.send_message(target_user, f"🎉 एडमिन @SpeedFistt ने आपके खाते में *{amount} RS* जोड़ दिए हैं! अपना BALANCE चेक करें।", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ चैनल में बैलेंस जोड़ने में एरर: {str(e)}")

print("🤖 SpeedFistt स्टोर बॉट सफलतापूर्वक चालू है...")
bot.infinity_polling()
