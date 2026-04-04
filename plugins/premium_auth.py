from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, LabeledPrice, PreCheckoutQuery
import motor.motor_asyncio
from datetime import datetime, timedelta
from config import Config

# ==========================================
# ᴅᴀᴛᴀʙᴀsᴇ sᴇᴛᴜᴘ
# ==========================================
db_client = motor.motor_asyncio.AsyncIOMotorClient(Config.DATABASE_URI)
db = db_client["ForwardBot"]
users_col = db["PremiumStatus"]

ᴀᴅᴍɪɴ_ɪᴅ = 7689365869 

# ==========================================
# ᴛᴇxᴛ ᴄᴏɴᴛᴇɴᴛ
# ==========================================
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

def main_premium_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("• ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ •", callback_data="buy_premium")],
        [InlineKeyboardButton("• ᴄᴏɴᴛᴀᴄᴛ •", url="https://t.me/HodyCloud"), 
         InlineKeyboardButton("• ꜰʀᴇᴇ ᴛʀɪᴀʟ •", callback_data="activate_trial")],
        [InlineKeyboardButton("⇆ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ ⇆", callback_data="back_home")]
    ])

def payment_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ sᴛᴀʀ", callback_data="pay_star"), InlineKeyboardButton("💳 ᴜᴘɪ", callback_data="pay_upi")],
        [InlineKeyboardButton("⇆ ʙᴀᴄᴋ ⇆", callback_data="premium_main")]
    ])

# ==========================================
# 1. ᴀᴅᴍɪɴ ᴄᴏɴᴛʀᴏʟ ᴄᴏᴍᴍᴀɴᴅs
# ==========================================
@Client.on_message(filters.command("addprem") & filters.user(ᴀᴅᴍɪɴ_ɪᴅ))
async def add_premium(client, message: Message):
    if len(message.command) != 3:
        return await message.reply_text("⚠️ **ᴜsᴀɢᴇ:** `/addprem UserID Days`")
    
    try:
        target_id = int(message.command[1])
        days = int(message.command[2])
        expiry_date = datetime.utcnow() + timedelta(days=days)
        
        await users_col.update_one(
            {"user_id": target_id}, 
            {"$set": {"is_premium": True, "expiry": expiry_date, "prem_expired_notified": False}}, 
            upsert=True
        )
        await message.reply_text(f"✅ **sᴜᴄᴄᴇss!** ᴜsᴇʀ `{target_id}` ɢʀᴀɴᴛᴇᴅ ᴘʀᴇᴍɪᴜᴍ ꜰᴏʀ {days} ᴅᴀʏs.")

        # SEND NOTIFICATION TO USER
        try:
            await client.send_message(
                chat_id=target_id,
                text=f"🎉 **ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!**\n\nʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀs ʙᴇᴇɴ ᴜᴘɢʀᴀᴅᴇᴅ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ꜰᴏʀ **{days} ᴅᴀʏs**.\n\n📅 **ᴇxᴘɪʀᴇs ᴏɴ:** {expiry_date.strftime('%Y-%m-%d')}\n🚀 ʏᴏᴜ ᴄᴀɴ ɴᴏᴡ ꜰᴏʀᴡᴀʀᴅ ᴍᴇssᴀɢᴇs ᴡɪᴛʜᴏᴜᴛ ʟɪᴍɪᴛs!"
            )
        except Exception:
            pass

    except ValueError:
        await message.reply_text("❌ ɪɴᴠᴀʟɪᴅ ɪᴅ ᴏʀ ᴅᴀʏs. ᴜsᴇ ɴᴜᴍʙᴇʀs ᴏɴʟʏ.")

@Client.on_message(filters.command("rmprem") & filters.user(ᴀᴅᴍɪɴ_ɪᴅ))
async def remove_premium(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("⚠️ **ᴜsᴀɢᴇ:** `/rmprem UserID`")
    target_id = int(message.command[1])
    await users_col.update_one({"user_id": target_id}, {"$set": {"is_premium": False, "expiry": None}}, upsert=True)
    await message.reply_text(f"❌ ᴜsᴇʀ `{target_id}` ᴘʀᴇᴍɪᴜᴍ ʀᴇᴠᴏᴋᴇᴅ.")

# ==========================================
# 2. sᴛᴀʀ ᴘᴀʏᴍᴇɴᴛ ʜᴀɴᴅʟᴇʀs (ᴀᴜᴛᴏᴍᴀᴛᴇᴅ)
# ==========================================
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
        {"$set": {"is_premium": True, "expiry": expiry, "prem_expired_notified": False}}, 
        upsert=True
    )
    await message.reply_text(
        f"🎉 **ᴘᴀʏᴍᴇɴᴛ sᴜᴄᴄᴇssꜰᴜʟ!**\n\nʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ᴜᴘɢʀᴀᴅᴇᴅ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ꜰᴏʀ **{days} ᴅᴀʏs**.\n📅 **ᴇxᴘɪʀᴇs ᴏɴ:** {expiry.strftime('%Y-%m-%d')}\n🚀 ᴇɴᴊᴏʏ ᴜɴʟɪᴍɪᴛᴇᴅ ꜰᴏʀᴡᴀʀᴅɪɴɢ!"
    )

# ==========================================
# 3. /ᴍʏᴘʟᴀɴ ᴄᴏᴍᴍᴀɴᴅ
# ==========================================
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
                f"🌟 **ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ** 🌟\n\n👤 **sᴛᴀᴛᴜs:** ᴀᴄᴛɪᴠᴇ ✅\n⏳ **ᴛɪᴍᴇ ʟᴇꜰᴛ:** {rem.days} ᴅᴀʏs\n📅 **ᴇxᴘɪʀᴇs ᴏɴ:** {expiry.strftime('%Y-%m-%d')}",
                reply_markup=kb
            )
        else:
            await users_col.update_one({"user_id": user_id}, {"$set": {"is_premium": False}})
            await message.reply_text("❌ **ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ʜᴀs ᴇxᴘɪʀᴇᴅ!**", reply_markup=kb)
            
    elif user_data.get("trial_start"):
        t_end = user_data["trial_start"] + timedelta(hours=1)
        if now < t_end:
            await message.reply_text(f"🎁 **ꜰʀᴇᴇ ᴛʀɪᴀʟ sᴛᴀᴛᴜs**\n\n⏳ **ᴛɪᴍᴇ ʟᴇꜰᴛ:** {int((t_end-now).seconds / 60)} ᴍɪɴs", reply_markup=kb)
        else:
            await message.reply_text("❌ **ʏᴏᴜʀ ꜰʀᴇᴇ ᴛʀɪᴀʟ ʜᴀs ᴇxᴘɪʀᴇᴅ!**", reply_markup=kb)
    else:
        await message.reply_text("❌ **ɴᴏ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ ꜰᴏᴜɴᴅ.**", reply_markup=kb)

# ==========================================
# 4. ɢᴀᴛᴇᴋᴇᴇᴘᴇʀ (ᴄʜᴇᴄᴋs ᴇxᴘɪʀʏ & ʙʟᴏᴄᴋs)
# ==========================================
@Client.on_message(filters.incoming & filters.private, group=-1)
async def gatekeeper(client, message: Message):
    user_id = message.from_user.id
    text = message.text or ""
    
    if text.startswith(("/", "/start", "/help", "/myplan", "/addprem", "/rmprem")):
        return
    if user_id == ᴀᴅᴍɪɴ_ɪᴅ:
        return
    
    user_data = await users_col.find_one({"user_id": user_id})
    now = datetime.utcnow()

    if user_data:
        # CHECK PREMIUM EXPIRY NOTIFICATION
        if user_data.get("is_premium") and user_data.get("expiry"):
            if now > user_data["expiry"]:
                await users_col.update_one({"user_id": user_id}, {"$set": {"is_premium": False}})
                await message.reply_text("❌ **ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ʜᴀs ᴇxᴘɪʀᴇᴅ!**\n\nᴘʟᴇᴀsᴇ ʀᴇɴᴇᴡ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ᴜsɪɴɢ ᴘʀᴇᴍɪᴜᴍ ꜰᴇᴀᴛᴜʀᴇs.", reply_markup=main_premium_kb())
                raise StopPropagation
            return # User is active premium, allow message

        # CHECK TRIAL EXPIRY NOTIFICATION
        if not user_data.get("is_premium") and user_data.get("trial_start"):
            if now > user_data["trial_start"] + timedelta(hours=1):
                if not user_data.get("trial_expired_notified"):
                    await users_col.update_one({"user_id": user_id}, {"$set": {"trial_expired_notified": True}})
                    await message.reply_text("⏳ **ʏᴏᴜʀ ꜰʀᴇᴇ ᴛʀɪᴀʟ ʜᴀs ᴇɴᴅᴇᴅ!**\n\nʜᴏᴘᴇ ʏᴏᴜ ᴇɴᴊᴏʏᴇᴅ ɪᴛ. ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ꜰᴏʀᴡᴀʀᴅɪɴɢ ꜰɪʟᴇs.", reply_markup=payment_kb())
                    raise StopPropagation
                else:
                    await message.reply_text(ᴍᴀɪɴ_ᴘʀᴇᴍɪᴜᴍ_ᴛᴇxᴛ, reply_markup=main_premium_kb())
                    raise StopPropagation
            return # User is active trial, allow message

    # Block users with no plan at all
    await message.reply_text(ᴍᴀɪɴ_ᴘʀᴇᴍɪᴜᴍ_ᴛᴇxᴛ, reply_markup=main_premium_kb())
    raise StopPropagation

# ==========================================
# 5. ᴄᴀʟʟʙᴀᴄᴋ ʜᴀɴᴅʟᴇʀ (ᴀʟʟ ʙᴜᴛᴛᴏɴs)
# ==========================================
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
            await users_col.update_one(
                {"user_id": user_id}, 
                {"$set": {"trial_start": datetime.utcnow(), "trial_used": True, "is_premium": False, "trial_expired_notified": False}}, 
                upsert=True
            )
            await query.message.delete()
            # Detailed message for starting the trial
            await client.send_message(
                chat_id=user_id,
                text="✅ **ꜰʀᴇᴇ ᴛʀɪᴀʟ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!**\n\nʏᴏᴜ ɴᴏᴡ ʜᴀᴠᴇ **1 ʜᴏᴜʀ** ᴏꜰ ꜰᴜʟʟ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss.\n⏳ **ᴇɴᴅs ɪɴ:** 60 ᴍɪɴᴜᴛᴇs.\n\n🚀 ʏᴏᴜ ᴄᴀɴ ɴᴏᴡ ꜰᴏʀᴡᴀʀᴅ ᴍᴇssᴀɢᴇs!"
            )

    elif data == "buy_premium":
        await query.message.edit_text(ᴘʟᴀɴ_ᴛᴇxᴛ, reply_markup=payment_kb())

    elif data == "pay_upi":
        qr = "https://jolly-sky-b8b7.rihanrazak765.workers.dev"
        await query.message.edit_text(
            f"💳 **ᴜᴘɪ ᴘᴀʏᴍᴇɴᴛ ᴍᴇᴛʜᴏᴅ**\n\n**ᴜᴘɪ ɪᴅ:** `hodystoll@upi` \n📸 **[ᴄʟɪᴄᴋ ᴛᴏ sᴄᴀɴ ǫʀ]({qr})**\n\n‼️ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴛᴏ @Amirkhan_Adminbot",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⇆ ʙᴀᴄᴋ ⇆", callback_data="buy_premium")]]),
            disable_web_page_preview=False
        )

    elif data == "pay_star":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("07 ᴅᴀʏs - 10 ⭐", callback_data="buy_star_7_10"),
             InlineKeyboardButton("15 ᴅᴀʏs - 20 ⭐", callback_data="buy_star_15_20")],
            [InlineKeyboardButton("30 ᴅᴀʏs - 40 ⭐", callback_data="buy_star_30_40"),
             InlineKeyboardButton("45 ᴅᴀʏs - 55 ⭐", callback_data="buy_star_45_55")],
            [InlineKeyboardButton("60 ᴅᴀʏs - 75 ⭐", callback_data="buy_star_60_75")],
            [InlineKeyboardButton("⇆ ʙᴀᴄᴋ ⇆", callback_data="buy_premium")]
        ])
        await query.message.edit_text("⭐ **sᴇʟᴇᴄᴛ ʏᴏᴜʀ sᴛᴀʀ ᴘʟᴀɴ**\nᴘᴀʏ ᴅɪʀᴇᴄᴛʟʏ ᴠɪᴀ ᴛᴇʟᴇɢʀᴀᴍ sᴛᴀʀs:", reply_markup=kb)

    elif data.startswith("buy_star_"):
        parts = data.split("_")
        d = parts[2]
        s = int(parts[3])
        
        await client.send_invoice(
            chat_id=user_id,
            title=f"ᴘʀᴇᴍɪᴜᴍ - {d} ᴅᴀʏs",
            description="ᴜᴘɢʀᴀᴅᴇ ꜰᴏʀᴡᴀʀᴅᴇʀ ʙᴏᴛ ᴀᴄᴄᴇss",
            payload=f"star_{d}_{s}",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice("Premium", s)],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"ᴘᴀʏ {s} ⭐", pay=True)],
                [InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data="premium_main")]
            ])
        )


