from celery import Celery
from aiogram import Bot
from src.core.config.settings import settings
from src.core.database.session import get_sync_session
from src.core.database.models import Reminder, User
import logging

celery_app = Celery(
    "real_estate_bot",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

bot = Bot(token=settings.TELEGRAM_API_TOKEN, parse_mode="HTML")

@celery_app.task
def send_reminder(reminder_id: int):
    session = get_sync_session()
    try:
        reminder = session.query(Reminder).filter(Reminder.id == reminder_id).first()
        if not reminder or reminder.is_completed:
            return
        user = session.query(User).filter(User.id == reminder.agent_id).first()
        if not user:
            return
        message = f"🔔 <b>Нагадування:</b>\n{reminder.text}\n🕒 {reminder.reminder_datetime}"
        bot.send_message(chat_id=user.id, text=message)
        reminder.is_completed = True
        session.commit()
    except Exception as e:
        logging.error(f"[Reminder Error] {e}")
    finally:
        session.close()