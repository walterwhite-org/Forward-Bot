from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, LabeledPrice, PreCheckoutQuery
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

‼️ **ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀꜰᴛᴇʀ ᴜᴘɪ ᴘᴀʏᴍᴇɴᴛ**
"""

# --- 1. sᴛᴀʀ ᴘᴀʏᴍᴇɴᴛ ʜᴀɴᴅʟᴇʀs (ᴀᴜᴛᴏᴍᴀᴛᴇᴅ) ---

@Client.on_pre_checkout_query()
async def pre_checkout_handler(client: Client, query: PreCheckoutQuery):
    await query.answer(ok=True)

@Client.on_message(filters.successful_payment)
async def payment_success(client: Client, message: Message):
    payload = message.successful_payment.invoice_payload
    days = int(payload.split("_")[1])
    expiry = datetime.utcnow() + timedelta(days=days)
    
    await users_col.update_one(
        {"user_id": message.from_user.id}, 
        {"$set": {"is_premium": True, "expiry": expiry}}, 
        upsert=True
    )
    
    await message.reply_text(
        f"🎉 **ᴘᴀʏᴍᴇɴᴛ sᴜᴄᴄᴇssꜰᴜʟ!**\n\nʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ᴜᴘɢʀᴀᴅᴇᴅ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ꜰᴏʀ **{days} ᴅᴀʏs**.\n📅 **ᴇxᴘɪʀᴇs:** {expiry.strftime('%Y-%m-%d')}"
    )

# --- 2. ᴄᴏᴍᴍᴀɴᴅ: /ᴍʏᴘʟᴀɴ (ʙʟᴜᴇ ᴄʟɪᴄᴋᴀʙʟᴇ) ---

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
        rem = expiry - now
        if rem.total_seconds() > 0:
            await message.reply_text(
                f"🌟 **ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ** 🌟\n\n👤 **sᴛᴀᴛᴜs:** ᴀᴄᴛɪᴠᴇ ✅\n⏳ **ᴛɪᴍᴇ ʟᴇꜰᴛ:** {rem.days} ᴅᴀʏs\n📅 **ᴇxᴘɪʀᴇs:** {expiry.strftime('%Y-%m-%d')}",
                reply_markup=kb
            )
        else:
            await message.reply_text("❌ **ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ʜᴀs ᴇxᴘɪʀᴇᴅ!**", reply_markup=kb)
    elif user_data.get("trial_start"):
        t_end = user_data["trial_start"] + timedelta(hours=1)
        if now < t_end:
            await message.reply_text(f"🎁 **ꜰʀᴇᴇ ᴛʀɪᴀʟ sᴛᴀᴛᴜs**\n⏳ **ᴛɪᴍᴇ ʟᴇꜰᴛ:** {int((t_end-now).seconds / 60)} ᴍɪɴs", reply_markup=kb)
        else:
            await message.reply_text("❌ **ʏᴏᴜʀ ꜰʀᴇᴇ ᴛʀɪᴀʟ ʜᴀs ᴇxᴘɪʀᴇᴅ!**", reply_markup=kb)
    else:
        await message.reply_text("❌ **ɴᴏ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ.**", reply_markup=kb)

# --- 3. ɢᴀᴛᴇᴋᴇᴇᴘᴇʀ (ʙʟᴏᴄᴋs ɴᴏɴ-ᴘʀᴇᴍɪᴜᴍ) ---

@Client.on_message(filters.incoming & filters.private, group=-1)
async def gatekeeper(client, message: Message):
    user_id = message.from_user.id
    if user_id == ᴀᴅᴍɪɴ_ɪᴅ or (message.text and message.text.startswith(("/", "/start", "/myplan"))):
        return
    
    user_data = await users_col.find_one({"user_id": user_id})
    now = datetime.utcnow()

    if not user_data or (not user_data.get("is_premium") and (not user_data.get("trial_start") or now > user_data.get("trial_start") + timedelta(hours=1))):
        await message.reply_text(ᴍᴀɪɴ_ᴘʀᴇᴍɪᴜᴍ_ᴛᴇxᴛ, reply_markup=main_premium_kb())
        raise StopPropagation

# --- 4. ᴄᴀʟʟʙᴀᴄᴋ ʜᴀɴᴅʟᴇʀ (ʙᴜᴛᴛᴏɴs) ---

def main_premium_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("• ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ •", callback_data="buy_premium")],
        [InlineKeyboardButton("• ᴄᴏɴᴛᴀᴄᴛ •", url="https://t.me/HodyCloud"), 
         InlineKeyboardButton("• ꜰʀᴇᴇ ᴛʀɪᴀʟ •", callback_data="activate_trial")],
        [InlineKeyboardButton("⇆ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ ⇆", callback_data="back_home")]
    ])

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    
    if data == "premium_main":
        await query.message.edit_text(ᴍᴀɪɴ_ᴘʀᴇᴍɪᴜᴍ_ᴛᴇxᴛ, reply_markup=main_premium_kb())

    elif data == "activate_trial":
        user_data = await users_col.find_one({"user_id": user_id})
        if user_data and user_data.get("trial_used"):
            await query.answer("❌ ʏᴏᴜ ʜᴀᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴜsᴇᴅ ʏᴏᴜʀ ᴏɴᴇ-ᴛɪᴍᴇ ᴛʀɪᴀʟ!", show_alert=True)
        else:
            await users_col.update_one({"user_id": user_id}, {"$set": {"trial_start": datetime.utcnow(), "trial_used": True}}, upsert=True)
            await query.answer("✅ 1-ʜᴏᴜʀ ꜰʀᴇᴇ ᴛʀɪᴀʟ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!", show_alert=True)
            await query.message.delete()

    elif data == "buy_premium":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("⭐ sᴛᴀʀ", callback_data="pay_star"), InlineKeyboardButton("💳 ᴜᴘɪ", callback_data="pay_upi")],
            [InlineKeyboardButton("⇆ ʙᴀᴄᴋ ⇆", callback_data="premium_main")]
        ])
        await query.message.edit_text(ᴘʟᴀɴ_ᴛᴇxᴛ, reply_markup=kb)

    elif data == "pay_upi":
        qr = "https://jolly-sky-b8b7.rihanrazak765.workers.dev"
        await query.message.edit_text(
            f"💳 **ᴜᴘɪ ᴘᴀʏᴍᴇɴᴛ**\n\n**ɪᴅ:** `hodystoll@upi` \n📸 **[ᴄʟɪᴄᴋ ᴛᴏ sᴄᴀɴ ǫʀ]({qr})**\n\nsᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴛᴏ @Amirkhan_Adminbot",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⇆ ʙᴀᴄᴋ ⇆", callback_data="buy_premium")]])
        )

    elif data == "pay_star":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("07 ᴅᴀʏs - 10 ⭐", callback_data="buy_star_7_10")],
            [InlineKeyboardButton("30 ᴅᴀʏs - 40 ⭐", callback_data="buy_star_30_40")],
            [InlineKeyboardButton("⇆ ʙᴀᴄᴋ ⇆", callback_data="buy_premium")]
        ])
        await query.message.edit_text("⭐ **sᴇʟᴇᴄᴛ sᴛᴀʀ ᴘʟᴀɴ**", reply_markup=kb)

    elif data.startswith("buy_star_"):
        d, s = data.split("_")[2], int(data.split("_")[3])
        await client.send_invoice(
            chat_id=user_id,
            title=f"ᴘʀᴇᴍɪᴜᴍ {d} ᴅᴀʏs",
            description="ꜰᴜʟʟ ʙᴏᴛ ᴀᴄᴄᴇss",
            payload=f"star_{d}_{s}",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice("Premium", s)],
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"ᴘᴀʏ {s} ⭐", pay=True)]])
        )

