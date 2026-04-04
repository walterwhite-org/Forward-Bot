from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import StopPropagation
import motor.motor_asyncio
from datetime import datetime, timedelta
from config import Config

# Connect to your existing MongoDB Database
db_client = motor.motor_asyncio.AsyncIOMotorClient(Config.DATABASE_URI) 
db = db_client["ForwardBot"]
users_col = db["PremiumStatus"]

# === CHANGE THIS TO YOUR TELEGRAM ID ===
ADMIN_ID = 7689365869  # Replace with your actual numeric Telegram User ID

PREMIUM_TEXT = """
🚫 **PREMIUM FEATURE ONLY** 🚫

Your 1-Day Free Trial has ended, or you don't have an active Premium Subscription! You cannot use the forward features right now.

💎 **PREMIUM PLANS:**
• 1 Month - ₹50
• 3 Months - ₹120
• 5 Months - ₹150
• 1 Year - ₹300

💳 **Payment UPI:** `hodystoll@upi`

After payment, send a screenshot to the Admin to activate your premium!
👨‍💻 **Contact Admin:** @Amirkhan_Adminbot
📢 **Channel:** @HodyStoll
"""

# ==========================================
# ADMIN COMMANDS TO MANAGE USERS
# ==========================================

@Client.on_message(filters.command("addprem") & filters.user(ADMIN_ID))
async def add_premium(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("Usage: `/addprem UserID`")
    
    target_id = int(message.command[1])
    await users_col.update_one(
        {"user_id": target_id}, 
        {"$set": {"is_premium": True}}, 
        upsert=True
    )
    await message.reply_text(f"✅ User `{target_id}` has been granted Premium Access!")

@Client.on_message(filters.command("rmprem") & filters.user(ADMIN_ID))
async def remove_premium(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("Usage: `/rmprem UserID`")
    
    target_id = int(message.command[1])
    await users_col.update_one(
        {"user_id": target_id}, 
        {"$set": {"is_premium": False}}, 
        upsert=True
    )
    await message.reply_text(f"❌ User `{target_id}` Premium Access revoked.")

# ==========================================
# THE GATEKEEPER (Checks trials & premium)
# ==========================================

# group=-1 means this runs BEFORE your normal forward plugins
@Client.on_message(filters.incoming & filters.private, group=-1)
async def gatekeeper(client, message: Message):
    text = message.text or ""
    
    # Let basic commands pass without checking premium
    if text.startswith(("/start", "/help", "/addprem", "/rmprem")):
        return 

    user_id = message.from_user.id
    
    # Admin is always allowed
    if user_id == ADMIN_ID:
        return 
        
    user_data = await users_col.find_one({"user_id": user_id})
    now = datetime.utcnow()

    # 1. NEW USER? Start their 1-day trial
    if not user_data:
        await users_col.insert_one({
            "user_id": user_id,
            "is_premium": False,
            "trial_start": now
        })
        await message.reply_text("🎉 **Your 1-Day Free Trial has started!** You can use the forward features for the next 24 hours.")
        return # Let them pass

    # 2. IS PREMIUM? Let them pass
    if user_data.get("is_premium") == True:
        return 
        
    # 3. CHECK TRIAL EXPIRY
    trial_start = user_data.get("trial_start")
    if trial_start:
        # If current time is less than trial start + 24 hours, they are still in trial
        if now < trial_start + timedelta(days=1):
            return # Let them pass
            
    # 4. IF WE REACH HERE: Trial is over and they are not premium.
    await message.reply_text(PREMIUM_TEXT)
    
    # This magic command completely stops the bot from forwarding their message!
    raise StopPropagation 
