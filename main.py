# main.py
import logging
import os
import platform
import sys
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Internal Scrolls
import config
import database
from tools import download_audio, search_youtube
from ranks import get_rank, is_sudo

# --- HOST OS IDENTIFICATION & PATH OPTIMIZATION ---
BASE_DIR = Path(__file__).resolve().parent
OS_NAME = platform.system().lower()
IS_TERMUX = "com.termux" in os.environ.get("PREFIX", "")

# Set proper pathing for Kurama's Image
# If on Termux, we ensure it looks in the home directory or relative folder
KURAMA_IMAGE_PATH = str(BASE_DIR / "kurama.png")

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class KuramaProfessional:
    def __init__(self):
        # Optimize for Termux resources: use a slightly lower connection pool if on mobile
        self.app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
        self._setup_handlers()

    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("menu", self.cmd_start))
        self.app.add_handler(CommandHandler("search", self.cmd_search))
        self.app.add_handler(CommandHandler("dl", self.cmd_dl))
        self.app.add_handler(CommandHandler("qr", self.cmd_qr))
        self.app.add_handler(CallbackQueryHandler(self.handle_callbacks))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_messages))
        self.app.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO | filters.VOICE, self.handle_files))

    async def _send_kurama_interface(self, update: Update):
        """Dynamic interface tailored by OS and Creator: Neel0210."""
        user = update.effective_user
        rank = get_rank(user.id)
        
        # Adaptive rank message
        if rank in ["SAGE", "AKATSUKI", "HOKAGE"]:
            rank_msg = f"🎖️ <b>Standing:</b> {rank}\nGreetings, Master. You have all the access. My power is yours."
        else:
            rank_msg = f"🎖️ <b>Standing:</b> {rank}\nTch. A mere {rank}? I suppose I can spare some chakra for you."

        # Detect environment for the menu footer
        env_tag = "📱 Termux" if IS_TERMUX else f"💻 {platform.system()}"

        menu_text = (
            f"🏮 <b>KURAMA INTERFACE</b> 🏮\n\n"
            f"I am <b>Kurama</b>, created by <b>Neel0210</b>.\n\n"
            f"{rank_msg}\n\n"
            f"🌐 <b>Realm:</b> {env_tag}\n"
            "📥 <b>/search [name]</b>: Scout for music.\n"
            "🎵 <b>/dl [link]</b>: Extract 320kbps audio.\n"
            "📊 <b>Stats</b>: View your records."
        )

        keyboard = [
            [InlineKeyboardButton("📊 My Stats", callback_data='nav_stats'),
             InlineKeyboardButton("⚙️ System Status", callback_data='nav_sys')],
            [InlineKeyboardButton("❌ Close Seal", callback_data='nav_close')]
        ]

        try:
            # Path-safe image loading
            if os.path.exists(KURAMA_IMAGE_PATH):
                with open(KURAMA_IMAGE_PATH, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo, 
                        caption=menu_text, 
                        reply_markup=InlineKeyboardMarkup(keyboard), 
                        parse_mode='HTML'
                    )
            else:
                await update.message.reply_text(
                    menu_text, 
                    reply_markup=InlineKeyboardMarkup(keyboard), 
                    parse_mode='HTML'
                )
        except Exception as e:
            logging.error(f"Pathing/Interface Error: {e}")

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        database.update_user_stats(update.effective_user.id, update.effective_user.username)
        await self._send_kurama_interface(update)

    async def handle_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if text.startswith("http"):
            await self.process_download(update.message, context, text)
        else:
            await update.message.reply_text("Send /start to know more.")

    async def cmd_search(self, update, context):
        query = " ".join(context.args)
        if not query:
            await update.message.reply_text("Usage: /search [song name]")
            return
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
        success, results = search_youtube(query)
        if success:
            keyboard = [[InlineKeyboardButton(f"▶️ {v['title'][:40]}", callback_data=f"sel_{v['id']}")] for v in results]
            await update.message.reply_text("👁️ <b>SEARCH RESULTS</b>:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

    async def cmd_dl(self, update, context):
        url = " ".join(context.args)
        if not url or not url.startswith("http"):
            await update.message.reply_text("Usage: /dl [link]")
            return
        await self.process_download(update.message, context, url)

    async def cmd_qr(self, update, context):
        import qrcode
        text = " ".join(context.args)
        if not text:
            await update.message.reply_text("Usage: /qr [text]")
            return
        
        qr_file = str(BASE_DIR / f"qr_{update.effective_user.id}.png")
        img = qrcode.make(text)
        img.save(qr_file)
        with open(qr_file, 'rb') as f:
            await update.message.reply_photo(photo=f, caption=f"🏁 <b>QR Seal</b>: <code>{text}</code>", parse_mode='HTML')
        if os.path.exists(qr_file):
            os.remove(qr_file)

    async def handle_callbacks(self, update, context):
        query = update.callback_query
        await query.answer()
        if query.data.startswith("sel_"):
            url = f"https://www.youtube.com/watch?v={query.data.split('_')[1]}"
            await query.message.reply_text(f"🎯 <b>Target Found</b>\nCopy for /dl:\n<code>{url}</code>", parse_mode='HTML')
        elif query.data == 'nav_stats':
            stats = database.load_db().get(str(query.from_user.id), {"downloads": 0})
            await query.message.reply_text(f"📊 <b>Raids:</b> {stats['downloads']} extractions.")
        elif query.data == 'nav_sys':
            if is_sudo(query.from_user.id):
                # Import here to avoid overhead on Termux if not needed
                from system_utils import get_system_report
                await query.message.reply_text(get_system_report(), parse_mode='HTML')
        elif query.data == 'nav_close':
            await query.message.delete()

    async def process_download(self, message_obj, context, url):
        chat_id = message_obj.chat_id
        await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.UPLOAD_DOCUMENT)
        status = await context.bot.send_message(chat_id=chat_id, text="⚡ <b>Extracting...</b>", parse_mode='HTML')
        
        # Audio pathing is usually handled by tools.py, ensuring relative paths work
        success, result = download_audio(url, bitrate="320")
        if success:
            database.update_user_stats(message_obj.from_user.id, message_obj.from_user.username, download=True)
            with open(result, 'rb') as f:
                await context.bot.send_audio(chat_id=chat_id, audio=f, caption=f"🏮 Done.\nCreated by <b>Neel0210</b>", parse_mode='HTML')
            if os.path.exists(result):
                os.remove(result)
            await status.delete()
        else:
            await status.edit_text(f"❌ Failed: {result}")

    async def handle_files(self, update, context):
        file = update.message.document or update.message.video or update.message.voice
        keyboard = [[InlineKeyboardButton("🎵 To MP3", callback_data=f"conv_mp3_{file.file_id}")]]
        await update.message.reply_text("🔮 <b>TRANSMUTATION</b>: Convert to audio?", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

if __name__ == '__main__':
    print(f"🔥 KURAMA ADAPTIVE BY NEEL0210 🔥")
    print(f"📍 Base Path: {BASE_DIR}")
    print(f"🌐 Detect OS: {platform.system()}")
    bot = KuramaProfessional()
    bot.app.run_polling()
