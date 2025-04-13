# Real Estate CRM Bot

## Опис
Telegram-бот та веб-панель для управління нерухомістю, клієнтами, нагадуваннями, бронюваннями.

## 📦 Встановлення

```bash
python -m venv venv
source venv/bin/activate  # або .\venv\Scripts\activate на Windows
pip install -r requirements.txt  # якщо генеруєш requirements.txt з pyproject.toml
```

### ⚙️ Налаштування
1. Створи `.env` на основі `.env.example`
2. Запусти ініціалізацію БД:

```bash
python main.py
```

## 🚀 Запуск
```bash
python main.py
```

Telegram бот і Flask веб-панель запускаються одночасно.