from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import motor.motor_asyncio
from datetime import datetime, timedelta
from config import Config

# ᴅᴀᴛᴀʙᴀsᴇ sᴇᴛᴜᴘ
db_client = motor.motor_asyncio.AsyncIOMotorClient(Config.DATABASE_URI)
db = db_client["ForwardBot"]
users_col = db["PremiumStatus"]

ᴀᴅᴍɪɴ_ɪᴅ = 7689365869 

# --- ᴛᴇxᴛ ᴄᴏɴᴛᴇɴᴛ ---
ᴍᴀɪɴ_ᴘʀᴇᴍɪᴜᴍ_ᴛᴇxᴛ = """
🎁 **ᴘʀᴇᴍɪᴜᴍ ꜰᴇᴀᴛᴜʀᴇs** 🎁

✨ **ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪꜰʏ**
✨ **ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋs**
✨ **ᴅɪʀᴇᴄᴛ ꜰɪʟᴇ ꜰᴏʀᴡᴀʀᴅɪɴɢ**
✨ **ʜɪɢʜ-sᴘᴇᴇᴅ ᴘʀᴏᴄᴇssɪɴɢ**
✨ **ᴢᴇʀᴏ ᴅᴇʟᴀʏ ʙᴇᴛᴡᴇᴇɴ ᴄʜᴀɴɴᴇʟs**
✨ **ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ**

💡 **ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ:** `/myplan`
"""

ᴘʟᴀɴ_ᴛᴇxᴛ = """
🏅 **ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs** 🏅

• 07 ᴅᴀʏs - 10 ₹ / 10 ⭐
• 15 ᴅᴀʏs - 20 ₹ / 20 ⭐
• 30 ᴅᴀʏs - 40 ₹ / 40 ⭐
• 45 ᴅᴀʏs - 55 ₹ / 55 ⭐
• 60 ᴅᴀʏs - 75 ₹ / 75 ⭐

‼️ **ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀꜰᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ**
"""

# --- ᴋᴇʏʙᴏᴀʀᴅs ---
def main_premium_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("• ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ •", callback_data="buy_premium")],
        [InlineKeyboardButton("• ᴄᴏɴᴛᴀᴄᴛ •", url="https://t.me/HodyCloud"), 
         InlineKeyboardButton("• ꜰʀᴇᴇ ᴛʀɪᴀʟ •", callback_data="activate_trial")],
        [InlineKeyboardButton("⇆ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ ⇆", callback_data="back_home")]
    ])

def payment_method_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ sᴛᴀʀ", callback_data="pay_star"),
         InlineKeyboardButton("💳 ᴜᴘɪ", callback_data="pay_upi")],
        [InlineKeyboardButton("⇆ ʙᴀᴄᴋ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ⇆", callback_data="premium_main")]
    ])

# --- ᴄᴏᴍᴍᴀɴᴅ: /ᴍʏᴘʟᴀɴ ---
@Client.on_message(filters.command("myplan") & filters.private)
async def my_plan(client, message: Message):
    user_id = message.from_user.id
    user_data = await users_col.find_one({"user_id": user_id})
    now = datetime.utcnow()

    if not user_data:
        return await message.reply_text("❌ **ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ.**\nᴜsᴇ /start ᴛᴏ sᴇᴇ ᴘʀᴇᴍɪᴜᴍ ᴏᴘᴛɪᴏɴs.")

    if user_data.get("is_premium"):
        expiry = user_data.get("expiry")
        if expiry:
            remaining = expiry - now
            days = remaining.days
            hours, remainder = divmod(remaining.seconds, 3600)
            await message.reply_text(
                f"🌟 **ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ** 🌟\n\n"
                f"👤 **sᴛᴀᴛᴜs:** ᴀᴄᴛɪᴠᴇ ✅\n"
                f"⏳ **ᴛɪᴍᴇ ʟᴇꜰᴛ:** {days} ᴅᴀʏs, {hours} ʜᴏᴜʀs\n"
                f"📅 **ᴇxᴘɪʀᴇs ᴏɴ:** {expiry.strftime('%Y-%m-%d')}"
            )
        else:
            await message.reply_text("👤 **sᴛᴀᴛᴜs:** ʟɪꜰᴇᴛɪᴍᴇ ᴘʀᴇᴍɪᴜᴍ ✅")
    else:
        trial_start = user_data.get("trial_start")
        if trial_start and now < trial_start + timedelta(hours=1):
            diff = (trial_start + timedelta(hours=1)) - now
            mins = int(diff.seconds / 60)
            await message.reply_text(f"🎁 **ꜰʀᴇᴇ ᴛʀɪᴀʟ sᴛᴀᴛᴜs**\n\n⏳ **ᴛɪᴍᴇ ʟᴇꜰᴛ:** {mins} ᴍɪɴᴜᴛᴇs")
        else:
            await message.reply_text("❌ **ʏᴏᴜʀ ᴘʟᴀɴ ʜᴀs ᴇxᴘɪʀᴇᴅ!**\nᴘʟᴇᴀsᴇ ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.")

# --- ɢᴀᴛᴇᴋᴇᴇᴘᴇʀ ʟᴏɢɪᴄ ---
@Client.on_message(filters.incoming & filters.private, group=-1)
async def gatekeeper(client, message: Message):
    user_id = message.from_user.id
    if user_id == ᴀᴅᴍɪɴ_ɪᴅ or (message.text and message.text.startswith(("/", "/start", "/myplan"))):
        return
    
    user_data = await users_col.find_one({"user_id": user_id})
    now = datetime.utcnow()

    if not user_data:
        await message.reply_text(ᴍᴀɪɴ_ᴘʀᴇᴍɪᴜᴍ_ᴛᴇxᴛ, reply_markup=main_premium_kb())
        raise StopPropagation

    if user_data.get("is_premium"):
        expiry = user_data.get("expiry")
        if expiry and now > expiry:
            await users_col.update_one({"user_id": user_id}, {"$set": {"is_premium": False}})
        else:
            return

    trial_start = user_data.get("trial_start")
    if trial_start and now < trial_start + timedelta(hours=1):
        return 

    await message.reply_text(ᴍᴀɪɴ_ᴘʀᴇᴍɪᴜᴍ_ᴛᴇxᴛ, reply_markup=main_premium_kb())
    raise StopPropagation

# --- ᴄᴀʟʟʙᴀᴄᴋ ʜᴀɴᴅʟᴇʀ ---
@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    
    if data == "premium_main":
        await query.message.edit_text(ᴍᴀɪɴ_ᴘʀᴇᴍɪᴜᴍ_ᴛᴇxᴛ, reply_markup=main_premium_kb())
    
    elif data == "activate_trial":
        user_data = await users_col.find_one({"user_id": user_id})
        if user_data and user_data.get("trial_start"):
            await query.answer("❌ ʏᴏᴜ ʜᴀᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴜsᴇᴅ ʏᴏᴜʀ ꜰʀᴇᴇ ᴛʀɪᴀʟ!", show_alert=True)
        else:
            await users_col.update_one({"user_id": user_id}, {"$set": {"trial_start": datetime.utcnow()}}, upsert=True)
            await query.answer("✅ 1-ʜᴏᴜʀ ꜰʀᴇᴇ ᴛʀɪᴀʟ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!", show_alert=True)
            await query.message.delete()

    elif data == "buy_premium":
        await query.message.edit_text(ᴘʟᴀɴ_ᴛᴇxᴛ, reply_markup=payment_method_kb())
        
    elif data == "pay_upi":
        qr_link = "https://jolly-sky-b8b7.rihanrazak765.workers.dev"
        await query.message.edit_text(
            f"💳 **ᴘᴀʏᴍᴇɴᴛ ᴍᴇᴛʜᴏᴅ: ᴜᴘɪ**\n\n**ᴜᴘɪ ɪᴅ:** `hodystoll@upi` \n\n📸 **[ᴄʟɪᴄᴋ ᴛᴏ sᴄᴀɴ ǫʀ]({qr_link})**\n\n‼️ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴛᴏ @Amirkhan_Adminbot ᴀꜰᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⇆ ʙᴀᴄᴋ ⇆", callback_data="buy_premium")]]),
            disable_web_page_preview=False
        )
        
    elif data == "pay_star":
        # ɴᴏᴛᴇ: ꜰᴏʀ ᴀᴜᴛᴏᴍᴀᴛɪᴄ sᴛᴀʀ ᴘᴀʏᴍᴇɴᴛs, ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ sᴇɴᴅ ᴀɴ ɪɴᴠᴏɪᴄᴇ. 
        # ꜰᴏʀ ɴᴏᴡ, ᴛʜɪs ʟɪɴᴋs ᴛᴏ ᴀᴅᴍɪɴ ᴀs ʀᴇǫᴜᴇsᴛᴇᴅ ꜰᴏʀ sᴛᴀʀ ᴄᴏɴꜰɪʀᴍᴀᴛɪᴏɴ.
        star_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("10 ⭐", url="https://t.me/Amirkhan_Adminbot"), InlineKeyboardButton("20 ⭐", url="https://t.me/Amirkhan_Adminbot")],
            [InlineKeyboardButton("40 ⭐", url="https://t.me/Amirkhan_Adminbot"), InlineKeyboardButton("55 ⭐", url="https://t.me/Amirkhan_Adminbot")],
            [InlineKeyboardButton("75 ⭐", url="https://t.me/Amirkhan_Adminbot")],
            [InlineKeyboardButton("⇆ ʙᴀᴄᴋ ⇆", callback_data="buy_premium")]
        ])
        await query.message.edit_text("⭐ **ᴘᴀʏ ᴡɪᴛʜ sᴛᴀʀs**\n\nsᴇʟᴇᴄᴛ ᴘʟᴀɴ ʙᴇʟᴏᴡ:", reply_markup=star_kb)




