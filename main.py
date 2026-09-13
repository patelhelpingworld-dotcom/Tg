import telebot
from telebot import types
from supabase import create_client, Client

# ====================   ====================
BOT_TOKEN = "6227179254:AAHd7mtq55sxSlQAcEKuqwMDog74_3Z4Dzg"
ADMIN_ID = 1006157952  #    ID  ( quotes )
SUPABASE_URL = "https://gaxyfiwthsdtugopjzkz.supabase.co/rest/v1/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdheHlmaXd0aHNkdHVnb3Bqemt6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzMTA2NzQsImV4cCI6MjEwNDg4NjY3NH0.Jtxo4aZyd2uDP-YxUwSyPuTIQuSPot0TKpw-h-9sJyc"

#   QR Code     (URL) 
# ( Imgur         QR       )
QR_CODE_URL = "https://i.ibb.co/7JzK1hRv/IMG-20260913-223730-495.jpg" 
# ========================================================

bot = telebot.TeleBot(BOT_TOKEN)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#    (    )
def main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_balance = types.KeyboardButton("BALANCE ")
    btn_add_fund = types.KeyboardButton("ADD FUND ")
    btn_obb = types.KeyboardButton("OBB & FILES")
    btn_hack = types.KeyboardButton("BGMI PAID HACK")
    
    markup.row(btn_balance, btn_add_fund)
    markup.row(btn_obb)
    markup.row(btn_hack)
    return markup

# /start 
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    try:
        supabase.table("users").upsert({"user_id": user_id}).execute()
    except Exception as e:
        print(f" : {e}")
        
    welcome_text = "    SpeedFistt   !\n\n        "
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_keyboard())

#     
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    user_id = message.from_user.id
    
    #  BALANCE  
    if message.text == "BALANCE ":
        response = supabase.table("users").select("balance").eq("user_id", user_id).execute()
        balance = response.data[0]['balance'] if response.data else 0
        bot.send_message(message.chat.id, f"    : *{balance} RS*", parse_mode="Markdown")
        
    #  ADD FUND (QR Code + Screenshot Message)
    elif message.text == "ADD FUND ":
        fund_text = (
            " *    :*\n\n"
            "1.    QR      \n"
            "2.         ID   \n\n"
            f" *  ID:* `{user_id}` (   )\n\n"
            " *Send Screenshot @SpeedFistt*"
        )
        #       
        try:
            bot.send_photo(message.chat.id, QR_CODE_URL, caption=fund_text, parse_mode="Markdown")
        except:
            #  QR         ,     
            bot.send_message(message.chat.id, fund_text, parse_mode="Markdown")
        
    #  OBB & FILES - (   2 )
    elif message.text == "OBB & FILES":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_paid_obb = types.InlineKeyboardButton("PAID OBB & FILES (399)", callback_data="buy_paid_obb")
        btn_cust_obb = types.InlineKeyboardButton("CUSTOMIZED OBB (599)", callback_data="buy_cust_obb")
        markup.add(btn_paid_obb, btn_cust_obb)
        
        bot.send_message(message.chat.id, " *OBB & FILES :*\n       (Full Season):", reply_markup=markup, parse_mode="Markdown")
        
    #  BGMI PAID HACK - (   2 )
    elif message.text == "BGMI PAID HACK":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_esp = types.InlineKeyboardButton("Only ESP (599)", callback_data="buy_esp")
        btn_brutal = types.InlineKeyboardButton("Brutal HACK (1199)", callback_data="buy_brutal")
        markup.add(btn_esp, btn_brutal)
        
        bot.send_message(message.chat.id, " *BGMI PAID HACK :*\n     (Full Season):", reply_markup=markup, parse_mode="Markdown")

#    (      )
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def process_purchase(call):
    user_id = call.from_user.id
    item_name = ""
    price = 0
    stock_data = ""
    
    #       
    if call.data == "buy_paid_obb":
        item_name = "PAID OBB & FILES"
        price = 399
        stock_data = "  PAID OBB : https://example.com"
    elif call.data == "buy_cust_obb":
        item_name = "CUSTOMIZED OBB"
        price = 599
        stock_data = "  CUSTOMIZED OBB : https://example.com"
    elif call.data == "buy_esp":
        item_name = "Only ESP Hack"
        price = 599
        stock_data = "  ESP HACK  (Key): ESP-KEY-XXXX-XXXX"
    elif call.data == "buy_brutal":
        item_name = "Brutal HACK"
        price = 1199
        stock_data = "  BRUTAL HACK  (Key): BRUTAL-KEY-XXXX-XXXX"

    # Supabase       
    response = supabase.table("users").select("balance").eq("user_id", user_id).execute()
    if not response.data:
        bot.answer_callback_query(call.id, "    /start ", show_alert=True)
        return
        
    current_balance = response.data[0]['balance']
    
    #     (Deduction)
    if current_balance >= price:
        new_balance = current_balance - price
        supabase.table("users").update({"balance": new_balance}).eq("user_id", user_id).execute()
        
        #       
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        success_text = (
            " *  !*\n\n"
            f" : {item_name} (Full Season)\n"
            f" : {price} RS\n"
            f"  : {new_balance} RS\n\n"
            f"{stock_data}"
        )
        bot.send_message(call.message.chat.id, success_text, parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, f"   ! : {price} RS,  : {current_balance} RS", show_alert=True)

#   :    (/add [User_ID] [Amount])
@bot.message_handler(commands=['add'])
def admin_add_balance(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "        ")
        return
        
    args = message.text.split()
    if len(args) < 3 or not args[1].isdigit() or not args[2].isdigit():
        bot.send_message(message.chat.id, "  : `/add [User_ID] [Amount]`")
        return
        
    target_user = int(args[1])
    amount = int(args[2])
    
    response = supabase.table("users").select("balance").eq("user_id", target_user).execute()
    if not response.data:
        bot.send_message(message.chat.id, "       (    )")
        return
        
    new_balance = response.data[0]['balance'] + amount
    supabase.table("users").update({"balance": new_balance}).eq("user_id", target_user).execute()
    
    bot.send_message(message.chat.id, f"  `{target_user}`    {amount} RS    ")
    bot.send_message(target_user, f"  @SpeedFistt     *{amount} RS*   !    ", parse_mode="Markdown")

#  
print(" SpeedFistt    ...")
bot.infinity_polling()
