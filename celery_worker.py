from celery import Celery
from src.core.config.settings import settings

celery_app = Celery(
    "real_estate_bot",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def send_reminder(reminder_id: int):
    # Тут логіка: надіслати повідомлення через бота
    print(f"[Reminder] Time to notify about reminder ID: {reminder_id}")