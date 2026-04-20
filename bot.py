import random
import datetime
import asyncio
import threading
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

BOT_TOKEN = "8779969705:AAF2p2dOGynWzbbSACpazQTMRQdZZYYI2aM"
REGISTER_LINK = "https://luckyshots.org/#/register?invitationCode=987773116271"

# User lock system
user_active = {}

# ===== KEEP RENDER ALIVE (PORT + HEAD FIX) =====
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_server).start()

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Register Here", url=REGISTER_LINK)],
        [InlineKeyboardButton("📢 Join Group", url="https://t.me/luckyshotpridiction")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await update.message.reply_photo(
            photo="https://thecolourtrading.in/wp-content/uploads/2026/04/ChatGPT-Image-Apr-21-2026-12_41_57-AM.png",
            caption=(
                "🔥 100% Working Hack 🔥\n\n"
                "👉 First make account using below button\n"
                "👉 Then use bot for 100% accuracy\n\n"
                "⚠️ IMPORTANT:\n"
                "Before starting, ensure your wallet is prepared with a 6-level fund maintenance strategy.\n\n"
                "👇 Enter last 3 digit to start"
            ),
            reply_markup=reply_markup
        )
    except:
        await update.message.reply_text("⚠️ Please press /start again")

# ===== TIMER =====
def get_remaining_seconds():
    now = datetime.datetime.now()
    return 60 - now.second

# ===== BACKGROUND TIMER TASK =====
async def handle_timer(context, chat_id, msg_id, user_id):
    remaining = get_remaining_seconds()
    await asyncio.sleep(remaining)

    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
    except:
        pass

    await context.bot.send_message(chat_id=chat_id, text="✅ Result Declared")

    user_active[user_id] = False

# ===== MESSAGE HANDLER =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if text.isdigit() and len(text) == 3:

        if user_active.get(user_id, False):
            await update.message.reply_text("⚠️ Period already running, please wait")
            return

        user_active[user_id] = True

        result_type = random.choice(["🔴 RED", "🟢 GREEN", "🔼 BIG", "🔽 SMALL"])

        temp_msg = await update.message.reply_text(f"""
🎯 Wingo Server 1min 🎯

📊 Period Number: {text}

⚡ Result: {result_type}
""")

        # 🔥 NON-BLOCKING TASK
        asyncio.create_task(
            handle_timer(context, chat_id, temp_msg.message_id, user_id)
        )

    else:
        await update.message.reply_text("❌ Please send only last 3 digits")

# ===== BOT SETUP (TIMEOUT FIX) =====
request = HTTPXRequest(connect_timeout=30, read_timeout=30)

app = ApplicationBuilder().token(BOT_TOKEN).request(request).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running (ULTIMATE VERSION 🔥)...")

# Stable polling
app.run_polling(drop_pending_updates=True)
