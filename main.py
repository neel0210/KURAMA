# main.py
import logging
import os
import qrcode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Internal Scrolls
import config
import database
import system_utils
from tools import download_audio, search_youtube
from ranks import get_rank, is_sudo

logging.basicConfig(level=logging.INFO)
KURAMA_IMAGE_PATH = "kurama.png"

class KuramaProfessional:
    def __init__(self):
        self.app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
        self._setup_handlers()

    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("menu", self.cmd_start))
        self.app.add_handler(CommandHandler("search", self.cmd_search))
        self.app.add_handler(CommandHandler("dl", self.cmd_dl))
        self.app.add_handler(CommandHandler("qr", self.cmd_qr)) # New Command
        self.app.add_handler(CallbackQueryHandler(self.handle_callbacks))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_messages))
        self.app.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO | filters.VOICE, self.handle_files))

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        database.update_user_stats(user.id, user.username)
        rank = get_rank(user.id)
        
        if rank in ["SAGE", "AKATSUKI", "HOKAGE"]:
            rank_msg = f"🎖️ <b>Standing:</b> {rank}\nGreetings, Master. You have all the access. My power is yours."
        else:
            rank_msg = f"🎖️ <b>Standing:</b> {rank}\nTch. A mere {rank}? Try not to waste my chakra, human."

        menu_text = (
            f"🏮 <b>KURAMA</b> 🏮\n\n"
            f"Greetings, I am <b>Kurama the bot</b>, created by <b>@neel0210</b>.\n\n"
            f"{rank_msg}\n\n"
            "📥 <b>/search [name]</b>: Youtube Search.\n"
            "🎵 <b>/dl [link]</b>: Download YT audio.\n"
            "🏁 <b>/qr [text]</b>: Generate QR Code.\n"
            "📊 <b>Stats</b>: View records."
        )

        keyboard = [[InlineKeyboardButton("📊 My Stats", callback_data='nav_stats'),
                     InlineKeyboardButton("⚙️ System Status", callback_data='nav_sys')],
                    [InlineKeyboardButton("❌ Close Seal", callback_data='nav_close')]]

        if os.path.exists(KURAMA_IMAGE_PATH):
            with open(KURAMA_IMAGE_PATH, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption=menu_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        else:
            await update.message.reply_text(menu_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

    async def cmd_qr(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generates a QR code from text."""
        text_to_encode = " ".join(context.args)
        if not text_to_encode:
            await update.message.reply_text("Tch. Give me some text to seal: /qr [text]")
            return

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.UPLOAD_PHOTO)
        
        qr_path = f"qr_{update.effective_user.id}.png"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(text_to_encode)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_path)

        with open(qr_path, 'rb') as qr_file:
            await update.message.reply_photo(photo=qr_file, caption=f"🏮 <b>QR Seal Manifested</b>\nContent: <code>{text_to_encode}</code>", parse_mode='HTML')
        
        os.remove(qr_path)

    async def cmd_search(self, update, context):
        query = " ".join(context.args)
        if not query:
            await update.message.reply_text("Usage: /search [song name]")
            return
        success, results = search_youtube(query)
        if success:
            keyboard = [[InlineKeyboardButton(f"▶️ {v['title'][:40]}", callback_data=f"sel_{v['id']}")] for v in results]
            await update.message.reply_text("👁️ <b>BYAKUGAN RESULTS</b>:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

    async def cmd_dl(self, update, context):
        url = " ".join(context.args)
        if not url or not url.startswith("http"):
            await update.message.reply_text("Usage: /dl [link]")
            return
        await self.process_download(update.message, context, url)

    async def handle_callbacks(self, update, context):
        query = update.callback_query
        await query.answer()
        if query.data.startswith("sel_"):
            url = f"https://www.youtube.com/watch?v={query.data.split('_')[1]}"
            await query.message.reply_text(f"🎯 <b>Target</b>\nCopy for /dl:\n<code>{url}</code>", parse_mode='HTML')
        elif query.data == 'nav_stats':
            stats = database.load_db().get(str(query.from_user.id), {"downloads": 0})
            await query.message.reply_text(f"📊 <b>Stats:</b> {stats['downloads']} raids.")
        elif query.data == 'nav_sys':
            if is_sudo(query.from_user.id):
                await query.message.reply_text(system_utils.get_system_report(), parse_mode='HTML')
        elif query.data == 'nav_close':
            await query.message.delete()

    async def handle_messages(self, update, context):
        if update.message.text.startswith("http"):
            await self.process_download(update.message, context, update.message.text)
        else:
            await update.message.reply_text("Send /start to know more.")

    async def process_download(self, message_obj, context, url):
        chat_id = message_obj.chat_id
        await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.UPLOAD_DOCUMENT)
        status = await context.bot.send_message(chat_id=chat_id, text="⚡ <b>Extracting...</b>", parse_mode='HTML')
        success, result = download_audio(url, bitrate="320")
        if success:
            database.update_user_stats(message_obj.from_user.id, message_obj.from_user.username, download=True)
            with open(result, 'rb') as f:
                await context.bot.send_audio(chat_id=chat_id, audio=f, caption="🏮 Master: @neel0210")
            os.remove(result)
            await status.delete()
        else:
            await status.edit_text(f"❌ Failed: {result}")

    async def handle_files(self, update, context):
        file = update.message.document or update.message.video or update.message.voice
        keyboard = [[InlineKeyboardButton("🎵 To MP3", callback_data=f"conv_mp3_{file.file_id}")]]
        await update.message.reply_text("🔮 <b>TRANSMUTATION</b>?", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

if __name__ == '__main__':
    print("🔥 KURAMA S-RANK INTERFACE: ONLINE 🔥")
    bot = KuramaProfessional()
    bot.app.run_polling()
