import os
import logging
from datetime import time
from typing import List, Dict, Any, Optional
from collections import defaultdict

from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ChatMemberStatus

TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

groups_data: Dict[int, Dict[str, Any]] = defaultdict(lambda: {
    'queue': [],
    'fixed_text': None,
    'fixed_photo_id': None,
    'fixed_caption': '',
    'waiting_for_fixed_media': False
})


def get_group_data(chat_id: int) -> Dict[str, Any]:
    """Holt Gruppen-Daten"""
    return groups_data[chat_id]


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
    """Filter: Nur Admins in Gruppen"""
    if update.effective_chat.type not in ('group', 'supergroup'):
        return False
    return await is_group_admin(context.bot, update.effective_user.id, update.effective_chat.id)


async def send_random_from_queue(context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> None:
    """Sendet zufälliges Item aus der Queue oder festen Text/Bild"""
    group_data = get_group_data(chat_id)
    
    try:
        if group_data['fixed_text'] is not None:
            await context.bot.send_message(
                chat_id=chat_id,
                text=group_data['fixed_text'],
                parse_mode='HTML'
            )
            logger.info(f"Fester Text gepostet in Gruppe {chat_id}")
            
            if group_data['fixed_photo_id']:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=group_data['fixed_photo_id'],
                    caption=group_data['fixed_caption'],
                    parse_mode='HTML' if group_data['fixed_caption'] else None
                )
                logger.info(f"Festes Bild gepostet in Gruppe {chat_id}")
            return
        
        if not group_data['queue']:
            logger.warning(f"Queue leer in Gruppe {chat_id}, kein Posting")
            return
        
        import random
        item = random.choice(group_data['queue'])
        
        if item['type'] == 'text':
            await context.bot.send_message(
                chat_id=chat_id,
                text=item['content'],
                parse_mode='HTML'
            )
            logger.info(f"Text gepostet in Gruppe {chat_id}")
        elif item['type'] == 'photo':
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=item['file_id'],
                caption=item.get('caption', ''),
                parse_mode='HTML' if item.get('caption') else None
            )
            logger.info(f"Bild gepostet in Gruppe {chat_id}")
    except Exception as e:
        logger.error(f"Fehler beim Posten in Gruppe {chat_id}: {e}")


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
    logger.info(f"Start-Befehl von Admin {update.effective_user.id} in Gruppe {update.effective_chat.id}")


async def add_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Text zur Queue hinzufügen"""
    if not await only_admins_filter(update, context):
        return
    
    if not context.args:
        await update.message.reply_text("❌ Nutze: /addtext <dein Text>")
        return
    
    group_data = get_group_data(update.effective_chat.id)
    text = " ".join(context.args)
    group_data['queue'].append({'type': 'text', 'content': text})
    await update.message.reply_text(
        f"✅ Text hinzugefügt von Admin {update.effective_user.first_name}"
    )
    logger.info(f"Text hinzugefügt von Admin {update.effective_user.id} in Gruppe {update.effective_chat.id}")


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bild zur Queue hinzufügen"""
    if not await only_admins_filter(update, context):
        return
    
    if not update.message.photo:
        return
    
    group_data = get_group_data(update.effective_chat.id)
    
    if group_data['waiting_for_fixed_media']:
        return
    
    file_id = update.message.photo[-1].file_id
    caption = update.message.caption or ""
    group_data['queue'].append({'type': 'photo', 'file_id': file_id, 'caption': caption})
    await update.message.reply_text(
        f"✅ Bild hinzugefügt von Admin {update.effective_user.first_name}"
    )
    logger.info(f"Bild hinzugefügt von Admin {update.effective_user.id} in Gruppe {update.effective_chat.id}")


async def handle_forward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Weitergeleitete Nachricht zur Queue hinzufügen"""
    if not await only_admins_filter(update, context):
        return
    
    if not update.message.forward_date:
        return
    
    group_data = get_group_data(update.effective_chat.id)
    
    try:
        if update.message.text:
            group_data['queue'].append({
                'type': 'text',
                'content': update.message.text_html or update.message.text
            })
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            group_data['queue'].append({
                'type': 'photo',
                'file_id': file_id,
                'caption': update.message.caption_html or update.message.caption or ""
            })
        await update.message.reply_text(
            f"✅ Weitergeleitet von Admin {update.effective_user.first_name}"
        )
        logger.info(f"Weiterleitung hinzugefügt von Admin {update.effective_user.id} in Gruppe {update.effective_chat.id}")
    except Exception as e:
        logger.error(f"Fehler bei Weiterleitung: {e}")


async def show_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Queue anzeigen"""
    if not await only_admins_filter(update, context):
        return
    
    group_data = get_group_data(update.effective_chat.id)
    
    if not group_data['queue']:
        await update.message.reply_text("📭 Warteschlange leer")
        return
    
    text = f"📋 Warteschlange ({len(group_data['queue'])} Einträge):\n\n"
    for i, item in enumerate(group_data['queue'], 1):
        if item['type'] == 'text':
            preview = item['content'][:50] + ("..." if len(item['content']) > 50 else "")
            text += f"{i}. Text: {preview}\n"
        else:
            caption_preview = ""
            if item.get('caption'):
                caption_preview = f" – {item['caption'][:30]}..."
            text += f"{i}. Bild{caption_preview}\n"
    
    await update.message.reply_text(text)
    logger.info(f"Queue angezeigt von Admin {update.effective_user.id} in Gruppe {update.effective_chat.id}")


async def post_now(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manuelles Posten (nur Admins)"""
    if not await only_admins_filter(update, context):
        return
    
    await send_random_from_queue(context, update.effective_chat.id)
    await update.message.reply_text("✅ Manuell gepostet")
    logger.info(f"Manuelles Posting von Admin {update.effective_user.id} in Gruppe {update.effective_chat.id}")


def create_post_job(chat_id: int):
    """Erstellt Post-Job für eine Gruppe"""
    async def job(context: ContextTypes.DEFAULT_TYPE):
        await send_random_from_queue(context, chat_id)
    return job


async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Auto-Posting planen (nur Admins)"""
    if not await only_admins_filter(update, context):
        return
    
    if not context.args:
        await update.message.reply_text("❌ Nutze: /schedule 30min | 1h | 4h | daily")
        return
    
    chat_id = update.effective_chat.id
    arg = context.args[0].lower()
    
    for job in context.job_queue.jobs():
        if job.data and job.data.get('chat_id') == chat_id:
            job.schedule_removal()
    
    try:
        job_data = {'chat_id': chat_id}
        post_job = create_post_job(chat_id)
        
        if arg == "30min":
            context.job_queue.run_repeating(
                post_job,
                interval=1800,
                first=10,
                data=job_data
            )
            msg = "alle 30 Minuten"
        elif arg == "1h":
            context.job_queue.run_repeating(
                post_job,
                interval=3600,
                first=10,
                data=job_data
            )
            msg = "stündlich"
        elif arg == "4h":
            context.job_queue.run_repeating(
                post_job,
                interval=14400,
                first=10,
                data=job_data
            )
            msg = "alle 4 Stunden"
        elif arg == "daily":
            context.job_queue.run_daily(
                post_job,
                time=time(12, 0),
                data=job_data
            )
            msg = "täglich um 12:00"
        else:
            await update.message.reply_text("❌ Unbekanntes Intervall")
            return
        
        await update.message.reply_text(f"✅ Auto-Posting: {msg}")
        logger.info(f"Scheduling geändert: {msg} von Admin {update.effective_user.id} in Gruppe {chat_id}")
    except Exception as e:
        logger.error(f"Fehler beim Scheduling: {e}")
        await update.message.reply_text("❌ Fehler beim Setzen des Schedules")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Auto-Posting stoppen (nur Admins)"""
    if not await only_admins_filter(update, context):
        return
    
    chat_id = update.effective_chat.id
    
    for job in context.job_queue.jobs():
        if job.data and job.data.get('chat_id') == chat_id:
            job.schedule_removal()
    
    await update.message.reply_text("🛑 Auto-Posting gestoppt")
    logger.info(f"Auto-Posting gestoppt von Admin {update.effective_user.id} in Gruppe {chat_id}")


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Queue leeren (nur Owner)"""
    if not is_owner(update.effective_user.id):
        return
    
    group_data = get_group_data(update.effective_chat.id)
    group_data['queue'].clear()
    await update.message.reply_text("🗑️ Warteschlange geleert")
    logger.info(f"Queue geleert von Owner in Gruppe {update.effective_chat.id}")


async def set_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Festen Text setzen (nur Admins)"""
    if not await only_admins_filter(update, context):
        return
    
    if not context.args:
        await update.message.reply_text("❌ Nutze: /settext <dein Text>")
        return
    
    group_data = get_group_data(update.effective_chat.id)
    
    group_data['fixed_text'] = " ".join(context.args)
    group_data['fixed_photo_id'] = None
    group_data['fixed_caption'] = ""
    group_data['waiting_for_fixed_media'] = False
    
    await update.message.reply_text(
        f"✅ Fester Text gesetzt:\n{group_data['fixed_text']}\n(Bild deaktiviert)"
    )
    logger.info(f"Fester Text gesetzt von Admin {update.effective_user.id} in Gruppe {update.effective_chat.id}")


async def set_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fester Text + Bild kombinieren (nur Admins)"""
    if not await only_admins_filter(update, context):
        return
    
    group_data = get_group_data(update.effective_chat.id)
    
    if group_data['fixed_text'] is None:
        await update.message.reply_text(
            "❌ Zuerst /settext verwenden, dann /setmedia"
        )
        return
    
    group_data['waiting_for_fixed_media'] = True
    await update.message.reply_text(
        "📸 Schick mir jetzt das feste Bild (kann Caption haben)"
    )
    logger.info(f"Warte auf festes Bild von Admin {update.effective_user.id} in Gruppe {update.effective_chat.id}")


async def random_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Zurück zur Zufalls-Warteschlange (nur Admins)"""
    if not await only_admins_filter(update, context):
        return
    
    group_data = get_group_data(update.effective_chat.id)
    
    group_data['fixed_text'] = None
    group_data['fixed_photo_id'] = None
    group_data['fixed_caption'] = ""
    group_data['waiting_for_fixed_media'] = False
    
    await update.message.reply_text(
        "✅ Zufallsmodus wieder aktiviert (Warteschlange)"
    )
    logger.info(f"Zufallsmodus aktiviert von Admin {update.effective_user.id} in Gruppe {update.effective_chat.id}")


async def handle_fixed_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler für festes Bild nach /setmedia"""
    if not await only_admins_filter(update, context):
        return
    
    group_data = get_group_data(update.effective_chat.id)
    
    if not group_data['waiting_for_fixed_media'] or not update.message.photo:
        return
    
    group_data['fixed_photo_id'] = update.message.photo[-1].file_id
    group_data['fixed_caption'] = update.message.caption or ""
    group_data['waiting_for_fixed_media'] = False
    
    await update.message.reply_text("✅ Festes Bild + Text aktiviert!")
    logger.info(f"Festes Bild gesetzt von Admin {update.effective_user.id} in Gruppe {update.effective_chat.id}")


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
    
    if OWNER_ID == 0:
        logger.warning("OWNER_ID nicht gesetzt - /clear funktioniert nicht")
    
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
    
    logger.info("Bot gestartet - Multi-Group Support aktiviert")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

