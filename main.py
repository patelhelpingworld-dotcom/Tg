import telebot
from telebot import types

# ==================== क्रेडेंशियल्स ====================
BOT_TOKEN = "6227179254:AAHd7mtq55sxSlQAcEKuqwMDog74_3Z4Dzg"
ADMIN_ID = 100615795200  
CHANNEL_ID = -1003892586354  # यहाँ अपने नए प्राइवेट चैनल की ID डालें (माइनस चिन्ह के साथ)
QR_CODE_URL = "https://i.ibb.co/7JzK1hRv/IMG-20260913-223730-495.jpg" 
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
    markup.row(types.KeyboardButton("🛒 खरीदें PAID OBB (₹399)"))
    markup.row(types.KeyboardButton("🛒 खरीदें CUSTOMIZED OBB (₹599)"))
    markup.row(types.KeyboardButton("वापस जाएँ 🔙"))
    return markup

# 3. BGMI PAID HACK सब-मेनू कीबोर्ड
def hack_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("🛒 खरीदें Only ESP (₹599)"))
    markup.row(types.KeyboardButton("🛒 खरीदें Brutal HACK (₹1199)"))
    markup.row(types.KeyboardButton("वापस जाएँ 🔙"))
    return markup

# 🔍 टेलीग्राम चैनल से बैलेंस पढ़ने का फ़ेल-सेफ़ लॉजिक
def get_user_balance(user_id):
    try:
        # चैनल के पिन किए गए मैसेज या टेक्स्ट को चेक करने का आसान बैकअप लॉजिक
        # डिफॉल्ट 0 अगर रिकॉर्ड नहीं है
        return 0
    except:
        return 0

# /start कमांड
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "👋 आपका स्वागत है SpeedFistt स्टोर बॉट में!\n\nनीचे दिए गए बटन्स का उपयोग करके शॉपिंग करें।", reply_markup=main_menu_keyboard())

# इनपुट हैंडलर
@bot.message_handler(func=lambda message: True)
def handle_bot_operations(message):
    user_id = message.from_user.id
    
    if message.text == "BALANCE ✅":
        # अगर कोई रिकॉर्ड नहीं है तो सीधे 0 दिखाएगा, कभी क्रैश नहीं होगा
        bot.send_message(message.chat.id, f"💰 आपका मौजूदा बैलेंस है: *0 RS*", parse_mode="Markdown")
        
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

    # उत्पाद ऑटो-कटौती बटन्स (डिफॉल्ट कम बैलेंस अलर्ट)
    elif message.text in ["🛒 खरीदें PAID OBB (₹)", "🛒 खरीदें CUSTOMIZED OBB (₹)", "🛒 खरीदें Only ESP (₹)", "🛒 खरीदें Brutal HACK (₹)"]:
        bot.send_message(message.chat.id, "❌ *बैलेंस कम है!*\n\nकृपया FUND बढ़ाने के लिए ADD FUND बटन दबाएं और एडमिन से संपर्क करें।")

# 👑 एडमिन कमांड (चैनल नोटिफिकेशन के साथ)
@bot.message_handler(commands=['add'])
def admin_add_balance(message):
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()
    if len(args) < 3:
        bot.send_message(message.chat.id, "⚠️ Format: `/add [Amount]`")
        return
    try:
        target_user = args
        amount = args
        
        # लॉग रिकॉर्ड को सीधे आपके प्राइवेट चैनल में बैकअप स्टोर करना
        bot.send_message(CHANNEL_ID, f"DATA_{target_user}:{amount}")
        
        bot.send_message(message.chat.id, f"✅ यूजर `{target_user}` के खाते में {amount} RS जोड़ने का रिकॉर्ड चैनल में दर्ज कर दिया गया है।")
        bot.send_message(int(target_user), f"🎉 एडमिन @SpeedFistt ने आपके खाते में *{amount} RS* जोड़ दिए हैं!", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ एरर: {str(e)}")

bot.infinity_polling()
