from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r'\.help(?:[ ]+([\w]+))?', outgoing=True))
    async def help_jutsu(event):
        arg = event.pattern_match.group(1)
        if arg:
            arg = arg.lower()
        
        # --- SUB-HELP: STICKERS & QUOTES (.help q) ---
        if arg in ["q", "sticker", "stickers", "kang"]:
            help_text = (
                "🏮 **【 JUTSU: SEALING ARTS 】** 🏮\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "🌀 **QUOTE:** `.q` \n"
                "📝 *Usage:* Reply to a text. Replicates QuotLy bubbles.\n\n"
                "🎨 **KANG:** `.kang [emoji] [pack]` \n"
                "📝 *Usage:* Reply to an image. Adds to permanent pack.\n\n"
                "✍️ **TEXT:** `.stext [text]` \n"
                "📝 *Usage:* `.stext Kurama` creates a text sticker.\n"
                "━━━━━━━━━━━━━━━━━━━━"
            )

        # --- SUB-HELP: DOWNLOADS (.help dl) ---
        elif arg in ["dl", "mp3", "video", "audio"]:
            help_text = (
                "🏮 **【 JUTSU: EXTRACTION 】** 🏮\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "🎥 **VIDEO:** `.dl [URL]` \n"
                "📝 *Usage:* `.dl https://link` downloads 1080p video.\n\n"
                "🎵 **AUDIO:** `.mp3 [URL]` \n"
                "📝 *Usage:* `.mp3 https://link` extracts 320kbps audio.\n"
                "━━━━━━━━━━━━━━━━━━━━"
            )

        # --- SUB-HELP: PURGE & CLEAN (.help purge) ---
        elif arg in ["purge", "del", "clean", "cleanup"]:
            help_text = (
                "🏮 **【 JUTSU: BATTLEFIELD CLEANUP 】** 🏮\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "🛡️ **PURGE:** `.purge [number]` \n"
                "📝 *Usage:* `.purge 10` deletes last 10 messages.\n\n"
                "⚔️ **DELETE:** `.del` \n"
                "📝 *Usage:* Reply to a message + `.del` to erase it.\n\n"
                "🧹 **CLEANUP:** `.cleanup` \n"
                "📝 *Usage:* Removes temporary files from the bot's storage.\n"
                "━━━━━━━━━━━━━━━━━━━━"
            )

        # --- SUB-HELP: TOOLS & UTILS (.help tools) ---
        elif arg in ["tools", "translate", "tr", "barcode", "notes"]:
            help_text = (
                "🏮 **【 JUTSU: UTILITY TOOLS 】** 🏮\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "🌐 **TRANSLATE:** `.tr [lang_code]` \n"
                "📝 *Usage:* Reply to text with `.tr en` to translate to English.\n\n"
                "📊 **BARCODE:** `.barcode [text]` \n"
                "📝 *Usage:* Generates a barcode image from your input.\n\n"
                "📓 **NOTES:** `.save [name]` | `.get [name]` \n"
                "📝 *Usage:* Save and retrieve snippets for later use.\n"
                "━━━━━━━━━━━━━━━━━━━━"
            )

        # --- SUB-HELP: SYSTEM (.help status) ---
        elif arg in ["status", "info", "system", "logs"]:
            help_text = (
                "🏮 **【 JUTSU: MONITORING 】** 🏮\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📊 **STATUS:** `.status` \n"
                "📝 *Usage:* Displays CPU, RAM, and Bot Uptime.\n\n"
                "👤 **INFO:** `.info` \n"
                "📝 *Usage:* Shows Shinobi credentials & Source link.\n\n"
                "🛡️ **LOGS:** `.test_logs` \n"
                "📝 *Usage:* Checks if Error Reporting is active.\n"
                "━━━━━━━━━━━━━━━━━━━━"
            )

        # --- MAIN HELP MENU (The Full Arsenal) ---
        else:
            await event.edit("`Unrolling the Full Arsenal...` 📜")
            help_text = (
                "🏮 **【 KURAMA FULL ARSENAL 】** 🏮\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                "🖼️ **SEALING MODULES**\n"
                "• `.q` | `.kang` | `.stext` \n"
                "🔹 *Help:* `.help q`\n\n"
                
                "⚡ **EXTRACTION MODULES**\n"
                "• `.dl` | `.mp3` \n"
                "🔹 *Help:* `.help dl`\n\n"
                
                "🛠️ **CLEANUP MODULES**\n"
                "• `.purge` | `.del` | `.cleanup` \n"
                "🔹 *Help:* `.help purge`\n\n"
                
                "🌐 **UTILITY MODULES**\n"
                "• `.tr` | `.barcode` | `.notes` \n"
                "🔹 *Help:* `.help tools`\n\n"
                
                "⚙️ **SYSTEM MODULES**\n"
                "• `.status` | `.info` | `.test_logs` \n"
                "🔹 *Help:* `.help status`\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "💡 **DECIDE YOUR JUTSU:** *Type .help [category]*"
            )
        
        await event.edit(help_text)