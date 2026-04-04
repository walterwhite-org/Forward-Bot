from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import motor.motor_asyncio
from datetime import datetime, timedelta
from config import Config

# Database Setup
db_client = motor.motor_asyncio.AsyncIOMotorClient(Config.DATABASE_URI)
db = db_client["ForwardBot"]
users_col = db["PremiumStatus"]

ADMIN_ID = 7689365869 

# --- Text Content for Forwarder Bot ---
MAIN_PREMIUM_TEXT = """
🎁 **PREMIUM FEATURES** 🎁

✨ **No Verification Required**
✨ **High-Speed Message Forwarding**
✨ **Zero Delay Between Channels**
✨ **Clone Multiple Forwarding Tasks**
✨ **Full Admin Support**

*Check your active plan:* `/myplan`
"""

PLAN_TEXT = """
🏅 **AVAILABLE PLANS** 🏅

• 07 DAYS - 10 ₹ / 10 ⭐
• 15 DAYS - 20 ₹ / 20 ⭐
• 30 DAYS - 40 ₹ / 40 ⭐
• 45 DAYS - 55 ₹ / 55 ⭐
• 60 DAYS - 75 ₹ / 75 ⭐

‼️ **MUST SEND SCREENSHOT AFTER PAYMENT**
"""

# --- Keyboards ---
def main_premium_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("• BUY PREMIUM •", callback_data="buy_premium")],
        [InlineKeyboardButton("• REFER FRIENDS •", callback_data="refer"), 
         InlineKeyboardButton("• FREE TRIAL •", callback_data="free_trial")],
        [InlineKeyboardButton("⇆ BACK TO HOME ⇆", callback_data="back_home")]
    ])

def payment_method_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ STAR", callback_data="pay_star"),
         InlineKeyboardButton("💳 UPI", callback_data="pay_upi")],
        [InlineKeyboardButton("⇆ BACK TO PREMIUM ⇆", callback_data="premium_main")]
    ])

# --- Admin Commands ---
@Client.on_message(filters.command("addprem") & filters.user(ADMIN_ID))
async def add_premium(client, message: Message):
    if len(message.command) != 3:
        return await message.reply_text("Usage: `/addprem UserID Days`")
    target_id = int(message.command[1])
    days = int(message.command[2])
    expiry = datetime.utcnow() + timedelta(days=days)
    await users_col.update_one({"user_id": target_id}, {"$set": {"is_premium": True, "expiry": expiry}}, upsert=True)
    await client.send_message(target_id, f"🎉 **Premium Activated!**\nValid for {days} days.\nExpiry: {expiry.strftime('%Y-%m-%d')}")
    await message.reply_text("✅ Success")

# --- Gatekeeper (1-Hour Trial) ---
@Client.on_message(filters.incoming & filters.private, group=-1)
async def gatekeeper(client, message: Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID or (message.text and message.text.startswith(("/", "/start"))):
        return
    
    user_data = await users_col.find_one({"user_id": user_id})
    now = datetime.utcnow()

    if not user_data:
        await users_col.insert_one({"user_id": user_id, "is_premium": False, "trial_start": now})
        return

    if user_data.get("is_premium"):
        if user_data.get("expiry") and now > user_data.get("expiry"):
            await users_col.update_one({"user_id": user_id}, {"$set": {"is_premium": False}})
        else:
            return

    if user_data.get("trial_start") and now < user_data.get("trial_start") + timedelta(hours=1):
        return

    await message.reply_text(MAIN_PREMIUM_TEXT, reply_markup=main_premium_kb())
    raise StopPropagation

# --- Callback Handlers (The "Pages") ---
@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    
    if data == "premium_main":
        await query.message.edit_text(MAIN_PREMIUM_TEXT, reply_markup=main_premium_kb())
    
    elif data == "buy_premium":
        await query.message.edit_text(PLAN_TEXT, reply_markup=payment_method_kb())
        
    elif data == "pay_upi":
        await query.message.edit_text(
            "💳 **PAYMENT METHOD: UPI**\n\n**UPI ID:** `hodystoll@upi` \n\n‼️ Send screenshot to @Amirkhan_Adminbot after payment.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⇆ BACK ⇆", callback_data="buy_premium")]])
        )
        
    elif data == "pay_star":
        await query.message.edit_text(
            "⭐ **PAYMENT METHOD: STARS**\n\nContact @Amirkhan_Adminbot to pay via Telegram Stars.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⇆ BACK ⇆", callback_data="buy_premium")]])
        )


