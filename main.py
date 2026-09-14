import telebot
from telebot import types

# ==================== क्रेडेंशियल्स ====================
BOT_TOKEN = "1105158554:AAHaby5PH4X7EfdRBAFHVXhyONX3ErDQwa4"
ADMIN_ID = 1006157952  
QR_CODE_URL = "https://i.ibb.co/7JzK1hRv/IMG-20260913-223730-495.jpg" 

# ⚠️ यहाँ अपने बनाए गए प्राइवेट चैनल की ID डालें (माइनस चिन्ह के साथ)
# (पक्का कर लें कि बॉट इस चैनल में Admin है और उसे 'Post Messages' की अनुमति है)
CHANNEL_ID = -1003892586354  
# ======================================================

bot = telebot.TeleBot(BOT_TOKEN)

# डमी बैलेंस ट्रैकर (क्रैश से सुरक्षा के लिए, असली बैलेंस चैनल बटन से अपडेट होगा)
user_live_balances = {}

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

# 🛒 ऑटोमैटिक कटौती लॉजिक
def process_balance_deduction(message, item_name, price, stock_data):
    user_id = message.from_user.id
    current_balance = user_live_balances.get(user_id, 0)
    
    if current_balance >= price:
        user_live_balances[user_id] = current_balance - price
        new_balance = user_live_balances[user_id]
        
        # टेलीग्राम चैनल में खरीदारी का रिकॉर्ड भेजना
        try:
            bot.send_message(CHANNEL_ID, f"🛍️ *शॉपिंग रिकॉर्ड*\n\n👤 यूजर ID: `{user_id}`\n📦 उत्पाद: {item_name}\n💸 कटौती: {price} RS\n💰 नया बैलेंस: {new_balance} RS", parse_mode="Markdown")
        except:
            pass
            
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
    if user_id not in user_live_balances:
        user_live_balances[user_id] = 0
    bot.send_message(message.chat.id, "👋 आपका स्वागत है SpeedFistt स्टोर बॉट में!\n\nनीचे दिए गए बटन्स का उपयोग करके शॉपिंग करें।", reply_markup=main_menu_keyboard())

# इनपुट हैंडलर
@bot.message_handler(func=lambda message: True)
def handle_bot_operations(message):
    user_id = message.from_user.id
    
    # 💰 BALANCE चेक
    if message.text == "BALANCE ✅":
        balance = user_live_balances.get(user_id, 0)
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

# 👑 एडमिन कमांड: चैनल में अप्रूवल बटन भेजना
@bot.message_handler(commands=['add'])
def admin_add_balance(message):
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()
    if len(args) < 3:
        bot.send_message(message.chat.id, "⚠️ Format: `/add [User_ID] [Amount]`")
        return
    try:
        target_user = args[1]
        amount = args[2]
        
        # चैनल में इनलाइन बटन के साथ मैसेज भेजना
        markup = types.InlineKeyboardMarkup()
        # callback_data में यूजर आईडी और अमाउंट स्टोर करना
        approve_btn = types.InlineKeyboardButton("बैलेंस जोड़ें ✅", callback_data=f"conf_{target_user}_{amount}")
        markup.add(approve_btn)
        
        channel_msg = f"💰 *फंड अप्रूवल रिक्वेस्ट*\n\n👤 यूजर ID: `{target_user}`\n💵 अमाउंट: *{amount} RS*"
        bot.send_message(CHANNEL_ID, channel_msg, parse_mode="Markdown", reply_markup=markup)
        
        bot.send_message(message.chat.id, f"📨 यूजर `{target_user}` के लिए {amount} RS जोड़ने का बटन आपके प्राइवेट चैनल में भेज दिया गया है। कृपया वहाँ जाकर कन्फर्म करें।")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ एरर: {str(e)}")

# 🔔 चैनल बटन क्लिक हैंडलर (क्लिक करते ही तुरंत रियल-टाइम बैलेंस अपडेट)
@bot.callback_query_handler(func=lambda call: call.data.startswith("conf_"))
def approve_balance_callback(call):
    try:
        # डेटा निकालना callback_data से
        _, target_user_str, amount_str = call.data.split("_")
        target_user = int(target_user_str)
        amount = int(amount_str)
        
        # लाइव बैलेंस अपडेट करना
        current = user_live_balances.get(target_user, 0)
        user_live_balances[target_user] = current + amount
        
        # चैनल का मैसेज अपडेट करके बटन हटा देना ताकि दोबारा क्लिक न हो सके
        updated_text = call.message.text + f"\n\n🟢 *APPROVED:* {amount} RS सफलता पूर्वक जोड़ दिए गए हैं।"
        bot.edit_message_text(chat_id=CHANNEL_ID, message_id=call.message.message_id, text=updated_text, reply_markup=None)
        
        # यूजर को टेलीग्राम पर सूचित करना
        bot.send_message(target_user, f"🎉 एडमिन @SpeedFistt ने आपके खाते में *{amount} RS* जोड़ दिए हैं! अपना BALANCE चेक करें करें।", parse_mode="Markdown")
        bot.answer_callback_query(call.id, "✅ बैलेंस सफलता पूर्वक जोड़ दिया गया!", show_alert=True)
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ एरर: {str(e)}", show_alert=True)

print("🤖 SpeedFistt स्टोर बॉट सफलतापूर्वक चालू है...")
bot.infinity_polling()
