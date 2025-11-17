import os
import logging
from datetime import time
from typing import List, Dict, Any, Optional
from pathlib import Path

from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ChatMemberStatus

TOKEN = os.getenv("TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID", "0"))
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

queue: List[Dict[str, Any]] = []
fixed_text: Optional[str] = None
fixed_photo_id: Optional[str] = None
fixed_caption: str = ""
waiting_for_fixed_media: bool = False


async def is_group_admin(bot, user_id: int, chat_id: int) -> bool:
    """Prüft ob User Admin oder Owner der Gruppe ist"""
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except Exception as e:
        logger.error(f"Fehler beim Admin-Check: {e}")
        return False


def is_owner(user_id: int) -> bool:
    """Prüft ob User der Bot-Owner ist"""
    return user_id == OWNER_ID


async def only_admins_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Filter: Nur Admins in der Zielgruppe"""
    if update.effective_chat.id != GROUP_ID:
        return False
    return await is_group_admin(context.bot, update.effective_user.id, GROUP_ID)


async def send_random_from_queue(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sendet zufälliges Item aus der Queue oder festen Text/Bild"""
    try:
        if fixed_text is not None:
            await context.bot.send_message(
                chat_id=GROUP_ID,
                text=fixed_text,
                parse_mode='HTML'
            )
            logger.info("Fester Text gepostet")
            
            if fixed_photo_id:
                await context.bot.send_photo(
                    chat_id=GROUP_ID,
                    photo=fixed_photo_id,
                    caption=fixed_caption,
                    parse_mode='HTML' if fixed_caption else None
                )
                logger.info("Festes Bild gepostet")
            return
        
        if not queue:
            logger.warning("Queue leer, kein Posting")
            return
        
        import random
        item = random.choice(queue)
        
        if item['type'] == 'text':
            await context.bot.send_message(
                chat_id=GROUP_ID,
                text=item['content'],
                parse_mode='HTML'
            )
            logger.info("Text gepostet")
        elif item['type'] == 'photo':
            await context.bot.send_photo(
                chat_id=GROUP_ID,
                photo=item['file_id'],
                caption=item.get('caption', ''),
                parse_mode='HTML' if item.get('caption') else None
            )
            logger.info("Bild gepostet")
    except Exception as e:
        logger.error(f"Fehler beim Posten: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start-Befehl"""
    if not await only_admins_filter(update, context):
        return
    
    await update.message.reply_text(
        "🤖 Admin-Only Poster aktiv\n\n"
        "Nur Gruppen-Administratoren dürfen:\n"
        "/addtext <Text>\n"
        "/addimage → Bild hochladen\n"
        "Nachricht weiterleiten → wird gespeichert\n"
        "/queue → Warteschlange anzeigen\n"
        "/settext <Text> → Fester Text setzen\n"
        "/setmedia → Fester Text + Bild kombinieren\n"
        "/randommode → Zurück zur Zufalls-Warteschlange\n"
        "/post → Manuell posten\n"
        "/schedule → Auto-Posting planen\n"
        "/stop → Auto-Posting stoppen\n\n"
        "Nur Owner:\n/clear → Warteschlange leeren"
    )
    logger.info(f"Start-Befehl von Admin {update.effective_user.id}")


async def add_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Text zur Queue hinzufügen"""
    if not await only_admins_filter(update, context):
        return
    
    if not context.args:
        await update.message.reply_text("❌ Nutze: /addtext <dein Text>")
        return
    
    text = " ".join(context.args)
    queue.append({'type': 'text', 'content': text})
    await update.message.reply_text(
        f"✅ Text hinzugefügt von Admin {update.effective_user.first_name}"
    )
    logger.info(f"Text hinzugefügt von Admin {update.effective_user.id}")


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bild zur Queue hinzufügen"""
    if not await only_admins_filter(update, context):
        return
    
    if not update.message.photo:
        return
    
    if waiting_for_fixed_media:
        return
    
    file_id = update.message.photo[-1].file_id
    caption = update.message.caption or ""
    queue.append({'type': 'photo', 'file_id': file_id, 'caption': caption})
    await update.message.reply_text(
        f"✅ Bild hinzugefügt von Admin {update.effective_user.first_name}"
    )
    logger.info(f"Bild hinzugefügt von Admin {update.effective_user.id}")


async def handle_forward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Weitergeleitete Nachricht zur Queue hinzufügen"""
    if not await only_admins_filter(update, context):
        return
    
    if not update.message.forward_date:
        return
    
    try:
        if update.message.text:
            queue.append({
                'type': 'text',
                'content': update.message.text_html or update.message.text
            })
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            queue.append({
                'type': 'photo',
                'file_id': file_id,
                'caption': update.message.caption_html or update.message.caption or ""
            })
        await update.message.reply_text(
            f"✅ Weitergeleitet von Admin {update.effective_user.first_name}"
        )
        logger.info(f"Weiterleitung hinzugefügt von Admin {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Fehler bei Weiterleitung: {e}")


async def show_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Queue anzeigen"""
    if not await only_admins_filter(update, context):
        return
    
    if not queue:
        await update.message.reply_text("📭 Warteschlange leer")
        return
    
    text = f"📋 Warteschlange ({len(queue)} Einträge):\n\n"
    for i, item in enumerate(queue, 1):
        if item['type'] == 'text':
            preview = item['content'][:50] + ("..." if len(item['content']) > 50 else "")
            text += f"{i}. Text: {preview}\n"
        else:
            caption_preview = ""
            if item.get('caption'):
                caption_preview = f" – {item['caption'][:30]}..."
            text += f"{i}. Bild{caption_preview}\n"
    
    await update.message.reply_text(text)
    logger.info(f"Queue angezeigt von Admin {update.effective_user.id}")


async def post_now(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manuelles Posten (nur Admins)"""
    if not await only_admins_filter(update, context):
        return
    
    await send_random_from_queue(context)
    await update.message.reply_text("✅ Manuell gepostet")
    logger.info(f"Manuelles Posting von Admin {update.effective_user.id}")


async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Auto-Posting planen (nur Admins)"""
    if not await only_admins_filter(update, context):
        return
    
    if not context.args:
        await update.message.reply_text("❌ Nutze: /schedule 30min | 1h | 4h | daily")
        return
    
    arg = context.args[0].lower()
    
    for job in context.job_queue.jobs():
        job.schedule_removal()
    
    try:
        if arg == "30min":
            context.job_queue.run_repeating(
                send_random_from_queue,
                interval=1800,
                first=10
            )
            msg = "alle 30 Minuten"
        elif arg == "1h":
            context.job_queue.run_repeating(
                send_random_from_queue,
                interval=3600,
                first=10
            )
            msg = "stündlich"
        elif arg == "4h":
            context.job_queue.run_repeating(
                send_random_from_queue,
                interval=14400,
                first=10
            )
            msg = "alle 4 Stunden"
        elif arg == "daily":
            context.job_queue.run_daily(
                send_random_from_queue,
                time=time(12, 0)
            )
            msg = "täglich um 12:00"
        else:
            await update.message.reply_text("❌ Unbekanntes Intervall")
            return
        
        await update.message.reply_text(f"✅ Auto-Posting: {msg}")
        logger.info(f"Scheduling geändert: {msg} von Admin {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Fehler beim Scheduling: {e}")
        await update.message.reply_text("❌ Fehler beim Setzen des Schedules")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Auto-Posting stoppen (nur Admins)"""
    if not await only_admins_filter(update, context):
        return
    
    for job in context.job_queue.jobs():
        job.schedule_removal()
    
    await update.message.reply_text("🛑 Auto-Posting gestoppt")
    logger.info(f"Auto-Posting gestoppt von Admin {update.effective_user.id}")


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Queue leeren (nur Owner)"""
    if not is_owner(update.effective_user.id):
        return
    
    queue.clear()
    await update.message.reply_text("🗑️ Warteschlange geleert")
    logger.info("Queue geleert von Owner")


async def set_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Festen Text setzen (nur Admins)"""
    if not await only_admins_filter(update, context):
        return
    
    if not context.args:
        await update.message.reply_text("❌ Nutze: /settext <dein Text>")
        return
    
    global fixed_text, fixed_photo_id, fixed_caption, waiting_for_fixed_media
    
    fixed_text = " ".join(context.args)
    fixed_photo_id = None
    fixed_caption = ""
    waiting_for_fixed_media = False
    
    await update.message.reply_text(
        f"✅ Fester Text gesetzt:\n{fixed_text}\n(Bild deaktiviert)"
    )
    logger.info(f"Fester Text gesetzt von Admin {update.effective_user.id}")


async def set_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fester Text + Bild kombinieren (nur Admins)"""
    if not await only_admins_filter(update, context):
        return
    
    global waiting_for_fixed_media
    
    if fixed_text is None:
        await update.message.reply_text(
            "❌ Zuerst /settext verwenden, dann /setmedia"
        )
        return
    
    waiting_for_fixed_media = True
    await update.message.reply_text(
        "📸 Schick mir jetzt das feste Bild (kann Caption haben)"
    )
    logger.info(f"Warte auf festes Bild von Admin {update.effective_user.id}")


async def random_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Zurück zur Zufalls-Warteschlange (nur Admins)"""
    if not await only_admins_filter(update, context):
        return
    
    global fixed_text, fixed_photo_id, fixed_caption, waiting_for_fixed_media
    
    fixed_text = None
    fixed_photo_id = None
    fixed_caption = ""
    waiting_for_fixed_media = False
    
    await update.message.reply_text(
        "✅ Zufallsmodus wieder aktiviert (Warteschlange)"
    )
    logger.info(f"Zufallsmodus aktiviert von Admin {update.effective_user.id}")


async def handle_fixed_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler für festes Bild nach /setmedia"""
    if not await only_admins_filter(update, context):
        return
    
    if not waiting_for_fixed_media or not update.message.photo:
        return
    
    global fixed_photo_id, fixed_caption, waiting_for_fixed_media
    
    fixed_photo_id = update.message.photo[-1].file_id
    fixed_caption = update.message.caption or ""
    waiting_for_fixed_media = False
    
    await update.message.reply_text("✅ Festes Bild + Text aktiviert!")
    logger.info(f"Festes Bild gesetzt von Admin {update.effective_user.id}")


async def register_commands(app: Application) -> None:
    """Registriert Bot-Befehle"""
    commands = [
        BotCommand("start", "Bot-Info anzeigen"),
        BotCommand("addtext", "Text zur Warteschlange hinzufügen"),
        BotCommand("queue", "Warteschlange anzeigen"),
        BotCommand("settext", "Festen Text setzen (wird immer gepostet)"),
        BotCommand("setmedia", "Fester Text + Bild kombinieren"),
        BotCommand("randommode", "Zurück zur Zufalls-Warteschlange"),
        BotCommand("post", "Manuell posten"),
        BotCommand("schedule", "Auto-Posting planen"),
        BotCommand("stop", "Auto-Posting stoppen"),
        BotCommand("clear", "Warteschlange leeren (nur Owner)"),
    ]
    
    try:
        await app.bot.set_my_commands(commands)
        logger.info("Bot-Befehle registriert")
    except Exception as e:
        logger.error(f"Fehler beim Registrieren der Befehle: {e}")


def main() -> None:
    """Main-Funktion"""
    if not TOKEN:
        logger.error("TOKEN nicht gesetzt")
        return
    
    if GROUP_ID == 0:
        logger.error("GROUP_ID nicht gesetzt")
        return
    
    if OWNER_ID == 0:
        logger.error("OWNER_ID nicht gesetzt")
        return
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addtext", add_text))
    app.add_handler(CommandHandler("queue", show_queue))
    app.add_handler(CommandHandler("settext", set_text))
    app.add_handler(CommandHandler("setmedia", set_media))
    app.add_handler(CommandHandler("randommode", random_mode))
    app.add_handler(CommandHandler("post", post_now))
    app.add_handler(CommandHandler("schedule", schedule))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("clear", clear))
    
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_fixed_media), group=1)
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_image), group=2)
    app.add_handler(MessageHandler(filters.FORWARDED & ~filters.COMMAND, handle_forward))
    
    app.post_init.register(register_commands)
    
    logger.info("Bot gestartet")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

