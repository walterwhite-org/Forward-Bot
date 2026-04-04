from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, LabeledPrice
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

💡 **ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ:** /myplan
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
    
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("➕ ᴇxᴛᴇɴᴅ ᴘʟᴀɴ", callback_data="buy_premium")]])

    if not user_data:
        return await message.reply_text("❌ **ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ.**", reply_markup=kb)

    if user_data.get("is_premium"):
        expiry = user_data.get("expiry")
        if expiry:
            remaining = expiry - now
            if remaining.total_seconds() <= 0:
                return await message.reply_text("❌ **ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ʜᴀs ᴇxᴘɪʀᴇᴅ!**", reply_markup=kb)
            
            await message.reply_text(
                f"🌟 **ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ** 🌟\n\n"
                f"👤 **sᴛᴀᴛᴜs:** ᴀᴄᴛɪᴠᴇ ✅\n"
                f"⏳ **ᴛɪᴍᴇ ʟᴇꜰᴛ:** {remaining.days} ᴅᴀʏs\n"
                f"📅 **ᴇxᴘɪʀᴇs ᴏɴ:** {expiry.strftime('%Y-%m-%d')}",
                reply_markup=kb
            )
    else:
        trial_start = user_data.get("trial_start")
        if trial_start:
            trial_end = trial_start + timedelta(hours=1)
            if now < trial_end:
                diff = trial_end - now
                await message.reply_text(f"🎁 **ꜰʀᴇᴇ ᴛʀɪᴀʟ sᴛᴀᴛᴜs**\n\n⏳ **ᴛɪᴍᴇ ʟᴇꜰᴛ:** {int(diff.seconds / 60)} ᴍɪɴᴜᴛᴇs", reply_markup=kb)
            else:
                await message.reply_text("❌ **ʏᴏᴜʀ ꜰʀᴇᴇ ᴛʀɪᴀʟ ʜᴀs ᴇxᴘɪʀᴇᴅ!**", reply_markup=kb)
        else:
            await message.reply_text("❌ **ɴᴏ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ ꜰᴏᴜɴᴅ.**", reply_markup=kb)

# --- ᴄᴀʟʟʙᴀᴄᴋ ʜᴀɴᴅʟᴇʀ ---
@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    
    if data == "premium_main":
        await query.message.edit_text(ᴍᴀɪɴ_ᴘʀᴇᴍɪᴜᴍ_ᴛᴇxᴛ, reply_markup=main_premium_kb())
    
    elif data == "activate_trial":
        user_data = await users_col.find_one({"user_id": user_id})
        # STRICT CHECK: If they have trial_start in DB, they can NEVER use it again
        if user_data and "trial_start" in user_data:
            await query.answer("❌ ʏᴏᴜ ʜᴀᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴜsᴇᴅ ʏᴏᴜʀ ᴏɴᴇ-ᴛɪᴍᴇ ꜰʀᴇᴇ ᴛʀɪᴀʟ!", show_alert=True)
        else:
            await users_col.update_one({"user_id": user_id}, {"$set": {"trial_start": datetime.utcnow(), "is_premium": False}}, upsert=True)
            await query.answer("✅ 1-ʜᴏᴜʀ ꜰʀᴇᴇ ᴛʀɪᴀʟ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!", show_alert=True)
            await query.message.delete()

    elif data == "buy_premium":
        await query.message.edit_text(ᴘʟᴀɴ_ᴛᴇxᴛ, reply_markup=payment_method_kb())
        
    elif data == "pay_upi":
        qr_link = "https://jolly-sky-b8b7.rihanrazak765.workers.dev"
        await query.message.edit_text(
            f"💳 **ᴘᴀʏᴍᴇɴᴛ ᴍᴇᴛʜᴏᴅ: ᴜᴘɪ**\n\n**ᴜᴘɪ ɪᴅ:** `hodystoll@upi` \n\n📸 **[ᴄʟɪᴄᴋ ᴛᴏ sᴄᴀɴ ǫʀ]({qr_link})**\n\n‼️ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴛᴏ @Amirkhan_Adminbot",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⇆ ʙᴀᴄᴋ ⇆", callback_data="buy_premium")]]),
            disable_web_page_preview=False
        )
        
    elif data == "pay_star":
        # Direct Telegram Stars Invoice Buttons
        star_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("10 ⭐", callback_data="star_10"), InlineKeyboardButton("20 ⭐", callback_data="star_20")],
            [InlineKeyboardButton("40 ⭐", callback_data="star_40"), InlineKeyboardButton("55 ⭐", callback_data="star_55")],
            [InlineKeyboardButton("75 ⭐", callback_data="star_75")],
            [InlineKeyboardButton("⇆ ʙᴀᴄᴋ ⇆", callback_data="buy_premium")]
        ])
        await query.message.edit_text("⭐ **ᴘᴀʏ ᴡɪᴛʜ sᴛᴀʀs**\n\nsᴇʟᴇᴄᴛ ʏᴏᴜʀ ᴀᴍᴏᴜɴᴛ:", reply_markup=star_kb)

    elif data.startswith("star_"):
        amount = int(data.split("_")[1])
        await client.send_invoice(
            chat_id=user_id,
            title="Premium Subscription",
            description=f"Upgrade to Premium for {amount} Stars",
            payload=f"premium_{amount}",
            provider_token="", # Empty for Telegram Stars
            currency="XTR",
            prices=[LabeledPrice("Premium", amount)]
        )





