"""
RELATE18TV MEDIA — Telegram Bot
Full automation script with all service flows
Deploy on Railway.app or Render.com (free)
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes, ConversationHandler
)

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with token from @BotFather
ADMIN_ID = 1113585793  # @CEORelate18tv — receives all "ready" notifications

logging.basicConfig(level=logging.INFO)

# ─── STATES ───────────────────────────────────────────────────────────────────
MAIN_MENU, AWAIT_PROCEED, AWAIT_AGE_CHECK = range(3)

# ─── ADMIN CONTACT TEXT ───────────────────────────────────────────────────────
ADMIN_TEXT = (
    "✅ Great! Reach admin now:\n\n"
    "⚡ *Telegram (Very Fast):*\n"
    "👉 https://t.me/CEORELATE18TV\n\n"
    "📱 *WhatsApp (Slow):*\n"
    "👉 https://wa.me/2348112280619\n\n"
    "_Admin will attend to you shortly. Be ready with your details._"
)

SAVE_CONTACT_TEXT = (
    "No worries! 👍\n\n"
    "While you think about it, save our contact so you can see our *status/story posts & reviews*:\n\n"
    "📲 *To view our Story/Status:*\n"
    "1. Make sure you have Telegram installed\n"
    "2. Save *+2348112280619* as *RELATE18TV*\n"
    "3. Done! You'll always see our posts ✅\n\n"
    "⭐ *Reviews since 2021:*\n"
    "👉 https://t.me/relate18tvfeedbackpage\n\n"
    "_Come back when you're ready. We'll be here._ 🔥"
)

# ─── INTERNATIONAL FEES ───────────────────────────────────────────────────────
INTL_FEES = """
🌍 *International Linkup Fees:*

🇬🇧 UK (London, Manchester, Birmingham etc) — ₦100k
🇺🇸 USA (Houston, New York) — ₦100k
🇨🇦 Canada (Toronto, Ontario) — ₦100k
🇫🇷 Paris — ₦100k
🇦🇪 Dubai — ₦50k
🇹🇷 Turkey — ₦70k
🇮🇪 Dublin — ₦70k
🇬🇭 Ghana — ₦30k
🇿🇦 South Africa — ₦50k

_Price varies by country. Ask if your country isn't listed._
"""

# ─── SERVICE MENU ─────────────────────────────────────────────────────────────
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌍 International Linkup", callback_data="intl_linkup")],
        [InlineKeyboardButton("🤝 Private Hangout & Companionship", callback_data="hangout")],
        [InlineKeyboardButton("💆 Massage Therapist Linkup", callback_data="massage")],
        [InlineKeyboardButton("🏠 Apartment & Shortlet", callback_data="shortlet")],
        [InlineKeyboardButton("🔒 Private Content Access (18+)", callback_data="private_content")],
        [InlineKeyboardButton("👥 Groups (Based on Vibes)", callback_data="groups")],
        [InlineKeyboardButton("✨ Special Requests", callback_data="special")],
        [InlineKeyboardButton("🏨 Hotel & Lifestyle", callback_data="hotel")],
        [InlineKeyboardButton("💊 Intimate Wellness Products (18+)", callback_data="products")],
        [InlineKeyboardButton("📹 Private Video Experience 1-on-1", callback_data="video_call")],
        [InlineKeyboardButton("🛍️ Declutter (Buy & Sell)", callback_data="declutter")],
        [InlineKeyboardButton("⭐ Reviews / Feedback", callback_data="reviews")],
    ])

def proceed_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes, I'm ready", callback_data="proceed_yes")],
        [InlineKeyboardButton("❌ Not ready now", callback_data="proceed_no")],
    ])

def age_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes, I'm 18+", callback_data="age_yes")],
        [InlineKeyboardButton("❌ No", callback_data="age_no")],
    ])

# ─── ACCOUNT DETAILS ──────────────────────────────────────────────────────────
from datetime import date
def account_details():
    today = date.today().strftime("%d/%b/%Y")
    return (
        f"💳 *Payment Details:*\n\n"
        f"Account Number: *8112280619*\n"
        f"Name: *RELATE18TV MEDIA*\n"
        f"Bank: *Moniepoint MFB*\n\n"
        f"▫️ Please send screenshot after payment\n"
        f"🗓️ {today}"
    )

# ─── NOTIFY ADMIN ─────────────────────────────────────────────────────────────
async def notify_admin(context: ContextTypes.DEFAULT_TYPE, user, service: str):
    name = user.full_name or "Unknown"
    username = f"@{user.username}" if user.username else "No username"
    user_id = user.id
    msg = (
        f"🔔 *New Client Alert!*\n\n"
        f"👤 Name: {name}\n"
        f"🆔 Username: {username}\n"
        f"🔗 ID: `{user_id}`\n"
        f"📦 Service: *{service}*\n\n"
        f"They clicked ✅ *Yes, I'm ready* — attend to them now!"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="Markdown")

# ─── HANDLERS ─────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *RELATE18TV MEDIA*\n\n"
        "_Private • Verified • Structured • Since 2021_\n\n"
        "We work with *serious clients only.* Select a service below 👇",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )
    return MAIN_MENU

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── INTERNATIONAL LINKUP ──────────────────────────────────────────────────
    if data == "intl_linkup":
        context.user_data["service"] = "International Linkup"
        await query.edit_message_text(
            INTL_FEES + "\n\nRequest fee is *₦100k* (varies by country).\n\nAre you ready to proceed?",
            parse_mode="Markdown",
            reply_markup=proceed_keyboard()
        )
        return AWAIT_PROCEED

    # ── HANGOUT & COMPANIONSHIP ───────────────────────────────────────────────
    elif data == "hangout":
        context.user_data["service"] = "Private Hangout & Companionship"
        await query.edit_message_text(
            "🤝 *Private Hangout & Companionship*\n\nSame process as linkup.\nRequest fee is *₦100k*.\n\nReady to proceed?",
            parse_mode="Markdown",
            reply_markup=proceed_keyboard()
        )
        return AWAIT_PROCEED

    # ── MASSAGE ───────────────────────────────────────────────────────────────
    elif data == "massage":
        context.user_data["service"] = "Massage Therapist Linkup"
        await query.edit_message_text(
            "💆 *Massage Therapist Linkup*\n\nSame process as linkup. The therapist will send pictures of their massage kit.\nRequest fee is *₦100k*.\n\nReady to proceed?",
            parse_mode="Markdown",
            reply_markup=proceed_keyboard()
        )
        return AWAIT_PROCEED

    # ── SHORTLET / HOTEL ──────────────────────────────────────────────────────
    elif data in ("shortlet", "hotel"):
        await query.edit_message_text(
            "🏠 *Apartment, Shortlet & Hotel Listings*\n\n"
            "See available options on our channel:\n👉 https://t.me/relate18tvmain\n\n"
            "📩 *Contact Shortlet Admin:*\n"
            "Telegram: https://t.me/Dora_shortlet\n"
            "WhatsApp: http://wa.me/2348176969528",
            parse_mode="Markdown"
        )
        return MAIN_MENU

    # ── PRIVATE CONTENT ───────────────────────────────────────────────────────
    elif data == "private_content":
        await query.edit_message_text(
            "🔞 *Age Verification Required*\n\nAre you 18 years or older?",
            parse_mode="Markdown",
            reply_markup=age_keyboard()
        )
        context.user_data["age_service"] = "private_content"
        return AWAIT_AGE_CHECK

    # ── GROUPS ────────────────────────────────────────────────────────────────
    elif data == "groups":
        await query.edit_message_text(
            "👥 *Groups (Based on Vibes)*\n\nPaid access. Request fee applies.\n\nReady to proceed?",
            parse_mode="Markdown",
            reply_markup=proceed_keyboard()
        )
        context.user_data["service"] = "Groups"
        return AWAIT_PROCEED

    # ── SPECIAL REQUEST ───────────────────────────────────────────────────────
    elif data == "special":
        context.user_data["service"] = "Special Request"
        await query.edit_message_text(
            "✨ *Special Requests*\n\nSame process as linkup. Price varies depending on your request.\n\nReady to proceed?",
            parse_mode="Markdown",
            reply_markup=proceed_keyboard()
        )
        return AWAIT_PROCEED

    # ── INTIMATE WELLNESS PRODUCTS ────────────────────────────────────────────
    elif data == "products":
        await query.edit_message_text(
            "🔞 *Age Verification Required*\n\nAre you 18 years or older?",
            parse_mode="Markdown",
            reply_markup=age_keyboard()
        )
        context.user_data["age_service"] = "products"
        return AWAIT_AGE_CHECK

    # ── VIDEO CALL ────────────────────────────────────────────────────────────
    elif data == "video_call":
        await query.edit_message_text(
            "📹 *Private Video Experience 1-on-1*\n\n"
            "Here's the procedure:\n\n"
            "1️⃣ Send *₦10K Airtime* to *08112280619 (GLO)*\n"
            "   _(NOTE: Card airtime, NOT Data)_\n\n"
            "2️⃣ Send us the screenshot\n\n"
            "3️⃣ We link you with available babe _(no pictures sent in advance)_\n\n"
            "4️⃣ You discuss with her\n"
            "   _Minimum pay is ₦30K_\n\n"
            "5️⃣ Make payment to us\n\n"
            "6️⃣ Proceed to video call with her\n\n"
            "7️⃣ Let us know when done & rate her ⭐\n\n"
            "Ready to proceed?",
            parse_mode="Markdown",
            reply_markup=proceed_keyboard()
        )
        context.user_data["service"] = "Private Video Experience"
        return AWAIT_PROCEED

    # ── DECLUTTER ─────────────────────────────────────────────────────────────
    elif data == "declutter":
        await query.edit_message_text(
            "🛍️ *Declutter — Buy & Sell Items*\n\n"
            "We help members sell neatly used items.\n\n"
            "See available items:\n👉 https://t.me/Relate18tvDeclutter\n\n"
            "📩 *Contact Admin:*\n"
            "Telegram: https://t.me/postingadmin",
            parse_mode="Markdown"
        )
        return MAIN_MENU

    # ── REVIEWS ───────────────────────────────────────────────────────────────
    elif data == "reviews":
        await query.edit_message_text(
            "⭐ *Reviews & Feedback (Since 2021)*\n\n"
            "See what our members say:\n"
            "👉 https://t.me/relate18tvfeedbackpage",
            parse_mode="Markdown"
        )
        return MAIN_MENU

    # ── PROCEED YES ───────────────────────────────────────────────────────────
    elif data == "proceed_yes":
        service = context.user_data.get("service", "Unknown Service")
        await notify_admin(context, query.from_user, service)
        await query.edit_message_text(
            ADMIN_TEXT,
            parse_mode="Markdown"
        )
        return MAIN_MENU

    # ── PROCEED NO ────────────────────────────────────────────────────────────
    elif data == "proceed_no":
        await query.edit_message_text(
            SAVE_CONTACT_TEXT,
            parse_mode="Markdown"
        )
        return MAIN_MENU

    # ── AGE CHECK YES ─────────────────────────────────────────────────────────
    elif data == "age_yes":
        svc = context.user_data.get("age_service")
        if svc == "private_content":
            await query.edit_message_text(
                "🔒 *Private Adult Space*\n\n"
                "This is a private space for:\n"
                "• Stress relief\n"
                "• Adult education\n"
                "• Relationship & intimacy growth\n"
                "• Honest conversations for grown adults\n\n"
                "🚫 Strictly 18+ | No minors allowed\n\n"
                "Ready to proceed?",
                parse_mode="Markdown",
                reply_markup=proceed_keyboard()
            )
            context.user_data["service"] = "Private Content Access"
        elif svc == "products":
            await query.edit_message_text(
                "💊 *Intimate Wellness Products*\n\n"
                "See available products:\n"
                "👉 https://t.me/relate18tvtoys\n\n"
                "📩 *Contact Admin:*\n"
                "Telegram: https://t.me/postingadmin\n"
                "WhatsApp: https://wa.link/rd9p0w",
                parse_mode="Markdown"
            )
        return AWAIT_PROCEED if svc == "private_content" else MAIN_MENU

    # ── AGE CHECK NO ──────────────────────────────────────────────────────────
    elif data == "age_no":
        await query.edit_message_text(
            "🚫 Sorry, this service is strictly for adults 18 and above.\n\nYou are not eligible for this service.",
            parse_mode="Markdown"
        )
        return MAIN_MENU

    return MAIN_MENU

# ─── FALLBACK TEXT HANDLER ────────────────────────────────────────────────────
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👇 Use the menu to select a service:",
        reply_markup=main_menu_keyboard()
    )
    return MAIN_MENU

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(button_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, fallback),
            ],
            AWAIT_PROCEED: [
                CallbackQueryHandler(button_handler),
            ],
            AWAIT_AGE_CHECK: [
                CallbackQueryHandler(button_handler),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(conv)
    print("✅ RELATE18TV Bot is running...")
    app.run_polling()
