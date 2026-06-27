import os
import random
import asyncio
import re
import json
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
import sys

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Token - REPLACE WITH YOUR BOT TOKEN
BOT_TOKEN = "8774218095:AAHE5UNCY9hSnJe1Pxv0EkWeJk0twpXCAq8"

# Owner usernames
OWNERS = {"usernames": ["DevilWillCryBitch", "MY_FALAH_M", "PV_KiTANAM", "Pxcio", "DevilWillCry1Bitch", "Pv_TERlYAKM"]}

BOT_DIR = "downloads_bot1"
if not os.path.exists(BOT_DIR):
    os.mkdir(BOT_DIR)

files_defaults = {
    "Kheshab.txt": "ONLINE",
    "targetid.txt": "1",
    "Caption.txt": "",
    "time.txt": "2",
    "fwd_source_channel.txt": "",
    "fwd_source_msg_id.txt": "0",
    "fwd_delay_min.txt": "3",
    "fwd_delay_max.txt": "10",
    "fwd_extra_text.txt": "",
    "fwd_extra_position.txt": "after",
    "clone_target.txt": ""
}

for filename, content in files_defaults.items():
    path = os.path.join(BOT_DIR, filename)
    if not os.path.exists(path):
        with open(path, 'w', encoding="utf-8") as f:
            f.write(content)

Spammer = [False]
ForwardSpammer = [False]
target_chat_id = None

async def spam_function(context: ContextTypes.DEFAULT_TYPE):
    print("Text spam thread started")
    chat_id = target_chat_id
    while Spammer[0] and chat_id:
        try:
            with open(os.path.join(BOT_DIR, 'Kheshab.txt'), 'r', encoding="utf-8") as f:
                messages = f.readlines()
            with open(os.path.join(BOT_DIR, 'Caption.txt'), 'r', encoding="utf-8") as f:
                caption = f.read().strip()
            with open(os.path.join(BOT_DIR, 'time.txt'), 'r') as f:
                delay = int(f.read().strip())
        except Exception as e:
            print(f"Config error: {e}")
            delay = 2
            messages = []

        if messages:
            try:
                text = random.choice(messages).strip()
                if text:
                    print(f"📤 Sending: {text[:30]}...")
                    msg = f"{text}\n\n{caption}" if caption else text
                    await context.bot.send_message(chat_id, msg)
            except Exception as e:
                print(f"Send error: {e}")
        await asyncio.sleep(delay)
    print("Text spam stopped")

async def forward_spam_function(context: ContextTypes.DEFAULT_TYPE):
    print("Forward spam thread started")
    chat_id = target_chat_id
    while ForwardSpammer[0] and chat_id:
        try:
            with open(os.path.join(BOT_DIR, 'fwd_source_channel.txt'), 'r', encoding="utf-8") as f:
                source_channel = f.read().strip()
            with open(os.path.join(BOT_DIR, 'fwd_source_msg_id.txt'), 'r') as f:
                source_msg_id = int(f.read().strip())
            with open(os.path.join(BOT_DIR, 'fwd_delay_min.txt'), 'r') as f:
                delay_min = float(f.read().strip())
            with open(os.path.join(BOT_DIR, 'fwd_delay_max.txt'), 'r') as f:
                delay_max = float(f.read().strip())
            with open(os.path.join(BOT_DIR, 'fwd_extra_text.txt'), 'r', encoding="utf-8") as f:
                extra_text = f.read().strip()
            with open(os.path.join(BOT_DIR, 'fwd_extra_position.txt'), 'r', encoding="utf-8") as f:
                extra_pos = f.read().strip()
        except Exception as e:
            print(f"Config read error: {e}")
            await asyncio.sleep(5)
            continue

        if not source_channel or source_msg_id == 0:
            print(" No source set. Use /setfwd <message_link>")
            ForwardSpammer[0] = False
            break

        try:
            await context.bot.send_message(
                chat_id, 
                f"Forwarding from {source_channel} (Message ID: {source_msg_id})"
            )

            if extra_text:
                if extra_pos == "before":
                    await context.bot.send_message(chat_id, f"{extra_text}\n\n")
                else:
                    await context.bot.send_message(chat_id, f"\n\n{extra_text}")

            print(f" Forwarded to {chat_id}")

            delay = random.uniform(delay_min, delay_max)
            await asyncio.sleep(delay)

        except Exception as e:
            print(f"Forward error: {e}")
            await asyncio.sleep(5)

    print("fwdspamstop")

async def check_owner(update: Update) -> bool:
    user = update.effective_user
    if user and user.username and user.username in OWNERS["usernames"]:
        return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        await update.message.reply_text("You are not authorized to use this bot.")
        return
    await update.message.reply_text("🤖 Bot is running!\nUse /help to see available commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        return
    help_text = """
**Commands**

/chatid - Get current chat/group ID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/setgp <id> - Set TARGET chat ID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/showfwd - Show config
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/setfosh <text> - Set caption
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/speed <n> - Set speed in seconds
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/spamon - Start text spam
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/spamoff - Stop text spam
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/ping - Bot status

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Coded by BrianMoser 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    await update.message.reply_text(help_text)

async def chatid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        return
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Chat ID: `{chat_id}`")

async def set_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        return
    global target_chat_id
    try:
        group_id = context.args[0]
        target_chat_id = int(group_id)
        with open(os.path.join(BOT_DIR, 'targetid.txt'), 'w') as f:
            f.write(group_id)
        await update.message.reply_text(f"Target set: `{group_id}`")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /setgp <chat_id>")

async def set_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        return
    if not context.args:
        await update.message.reply_text("Usage: /setfosh <text>")
        return
    caption = " ".join(context.args)
    with open(os.path.join(BOT_DIR, 'Caption.txt'), 'w', encoding="utf-8") as f:
        f.write(caption)
    await update.message.reply_text(f"Caption set: {caption[:50]}...")

async def set_speed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        return
    try:
        speed = int(context.args[0])
        if speed > 0:
            with open(os.path.join(BOT_DIR, 'time.txt'), 'w') as f:
                f.write(str(speed))
            await update.message.reply_text(f"Speed set to {speed} seconds")
        else:
            await update.message.reply_text("Speed must be greater than 0")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /speed <seconds>")

async def spam_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        return
    global target_chat_id
    if target_chat_id is None:
        with open(os.path.join(BOT_DIR, 'targetid.txt'), 'r') as f:
            target_chat_id = int(f.read().strip())
        if target_chat_id == 1:
            await update.message.reply_text("Set target first: /setgp <id>")
            return
    if not Spammer[0]:
        Spammer[0] = True
        asyncio.create_task(spam_function(context))
        await update.message.reply_text("lets go fuck them ")
    else:
        await update.message.reply_text("Already spamming")

async def spam_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        return
    if Spammer[0]:
        Spammer[0] = False
        await update.message.reply_text("some nigga stop me ")
    else:
        await update.message.reply_text("Not spamming")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        return
    await update.message.reply_text("never left ")

async def set_forward_from_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        return
    if not context.args:
        await update.message.reply_text("Usage: /setfwd <message_link>")
        return
    link = context.args[0]
    try:
        parts = link.replace("https://t.me/", "").split("/")
        if parts[0] == "c":
            channel_id = int("-100" + parts[1])
            msg_id = int(parts[2])
            channel_username = str(channel_id)
        else:
            channel_username = parts[0]
            msg_id = int(parts[1])
        with open(os.path.join(BOT_DIR, 'fwd_source_channel.txt'), 'w', encoding="utf-8") as f:
            f.write(channel_username)
        with open(os.path.join(BOT_DIR, 'fwd_source_msg_id.txt'), 'w') as f:
            f.write(str(msg_id))
        await update.message.reply_text(f" Source set!\nChannel: {channel_username}\nMessage ID: {msg_id}")
    except Exception as e:
        await update.message.reply_text(f" Failed to parse link: {e}")

async def forward_spam_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        return
    global target_chat_id
    if target_chat_id is None:
        with open(os.path.join(BOT_DIR, 'targetid.txt'), 'r') as f:
            target_chat_id = int(f.read().strip())
        if target_chat_id == 1:
            await update.message.reply_text("Set target first: /setgp <id>")
            return
    if not ForwardSpammer[0]:
        ForwardSpammer[0] = True
        asyncio.create_task(forward_spam_function(context))
        await update.message.reply_text("fspam")
    else:
        await update.message.reply_text("its run")

async def forward_spam_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        return
    if ForwardSpammer[0]:
        ForwardSpammer[0] = False
        await update.message.reply_text("fwdspamrun")
    else:
        await update.message.reply_text("Not running")

async def show_forward_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        return
    with open(os.path.join(BOT_DIR, 'targetid.txt'), 'r') as f:
        target = f.read().strip()
    with open(os.path.join(BOT_DIR, 'fwd_source_channel.txt'), 'r', encoding="utf-8") as f:
        source = f.read().strip()
    with open(os.path.join(BOT_DIR, 'fwd_source_msg_id.txt'), 'r') as f:
        msg_id = f.read().strip()
    status = "you stop it before" if not ForwardSpammer[0] else "run"
    await update.message.reply_text(
        f"**Forward Config - {status}**\n"
        f"• TARGET: `{target}`\n"
        f"• SOURCE: `{source}/{msg_id}`"
    )

async def join_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update):
        return
    if not context.args:
        await update.message.reply_text("Usage: /join <link>")
        return
    await update.message.reply_text(
        " Bots cannot join groups/channels automatically.\n"
        "Please add the bot manually to the group or channel."
    )

async def run_bot():
    """Async main function"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("chatid", chatid))
    application.add_handler(CommandHandler("setgp", set_group))
    application.add_handler(CommandHandler("setfosh", set_caption))
    application.add_handler(CommandHandler("speed", set_speed))
    application.add_handler(CommandHandler("spamon", spam_on))
    application.add_handler(CommandHandler("spamoff", spam_off))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("setfwd", set_forward_from_link))
    application.add_handler(CommandHandler("fwdspam_on", forward_spam_on))
    application.add_handler(CommandHandler("fwdspam_off", forward_spam_off))
    application.add_handler(CommandHandler("showfwd", show_forward_config))
    application.add_handler(CommandHandler("join", join_command))

    print("="*40)
    print("🔥 Bot running with token!")
    print("Commands: /help")
    print("="*40)
    
    # Initialize and start the bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped")
        await application.updater.stop()
        await application.stop()
        await application.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped")
