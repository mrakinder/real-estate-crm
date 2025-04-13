"""
Main entry point for the Real Estate CRM application.
"""
import asyncio
import os
import logging
import nest_asyncio
from pathlib import Path

from flask import Flask, render_template, jsonify

# Застосовуємо nest_asyncio для вирішення проблем з event loop
nest_asyncio.apply()

# Configure basic logging
logging.basicConfig(level=logging.INFO)

# Ensure all required directories exist
Path("logs").mkdir(exist_ok=True)
Path("media/uploads/images").mkdir(exist_ok=True, parents=True)
Path("media/uploads/documents").mkdir(exist_ok=True, parents=True)
Path("templates").mkdir(exist_ok=True)

# Create Flask app for the web interface
app = Flask(__name__)
from src.web.admin import admin_bp
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "development_key")
app.register_blueprint(admin_bp)

# Web routes
@app.route('/')
def index():
    # Отримуємо статистику для дашборду
    property_count = 0
    user_count = 0
    booking_count = 0
    
    # Тут буде код для отримання реальних даних з бази даних
    try:
        from src.core.database.models import Property, User, Booking
        from src.core.database.session import async_session
        import asyncio
        
        async def get_stats():
            from sqlalchemy import text
            async with async_session() as session:
                property_query = await session.execute(text("SELECT COUNT(*) FROM properties"))
                user_query = await session.execute(text("SELECT COUNT(*) FROM users"))
                booking_query = await session.execute(text("SELECT COUNT(*) FROM bookings WHERE status = 'confirmed'"))
                
                return {
                    'property_count': property_query.scalar() or 0,
                    'user_count': user_query.scalar() or 0,
                    'booking_count': booking_query.scalar() or 0
                }
        
        # Запускаємо асинхронну функцію через nest_asyncio
        loop = asyncio.get_event_loop()
        stats = loop.run_until_complete(get_stats())
        
        property_count = stats['property_count']
        user_count = stats['user_count']
        booking_count = stats['booking_count']
    except Exception as e:
        logging.error(f"Error fetching stats: {e}")
    
    return render_template('index.html',
                          property_count=property_count,
                          user_count=user_count,
                          booking_count=booking_count)

@app.route('/stats')
def stats():
    # Тут буде код для отримання статистики
    return render_template('stats.html')

@app.route('/properties')
def properties():
    properties_list = []
    
    # Тут буде код для отримання списку об'єктів нерухомості
    try:
        from src.core.database.models import Property
        from src.core.database.session import async_session
        import asyncio
        
        async def get_properties():
            from sqlalchemy import text
            async with async_session() as session:
                result = await session.execute(text("SELECT id, title, address, price, type, rooms, area FROM properties ORDER BY id DESC"))
                properties = result.fetchall()
                
                # Перетворюємо результат у список словників
                property_list = []
                for prop in properties:
                    property_list.append({
                        'id': prop[0],
                        'title': prop[1],
                        'address': prop[2],
                        'price': prop[3],
                        'type': prop[4],
                        'rooms': prop[5],
                        'area': prop[6]
                    })
                
                return property_list
        
        # Запускаємо асинхронну функцію через nest_asyncio
        loop = asyncio.get_event_loop()
        properties_list = loop.run_until_complete(get_properties())
    except Exception as e:
        logging.error(f"Error fetching properties: {e}")
    
    return render_template('properties.html', properties=properties_list)

@app.route('/users')
def users():
    users_list = []
    
    # Тут буде код для отримання списку користувачів
    try:
        from src.core.database.models import User
        from src.core.database.session import async_session
        import asyncio
        
        async def get_users():
            from sqlalchemy import text
            async with async_session() as session:
                result = await session.execute(text("SELECT id, full_name, role, language_code, created_at FROM users ORDER BY id DESC"))
                users = result.fetchall()
                
                # Перетворюємо результат у список словників
                user_list = []
                for user in users:
                    user_list.append({
                        'id': user[0],
                        'full_name': user[1],
                        'role': user[2],
                        'language': user[3],
                        'created_at': user[4]
                    })
                
                return user_list
        
        # Запускаємо асинхронну функцію через nest_asyncio
        loop = asyncio.get_event_loop()
        users_list = loop.run_until_complete(get_users())
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
    
    return render_template('users.html', users=users_list)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

async def setup_database():
    """Initialize the database."""
    from src.core.database.session import init_db
    await init_db()

async def setup_app():
    """Set up the application without running."""
    # Set up the database
    await setup_database()

def run_app():
    """Run the application."""
    # Import and run the bot
    from src.bot.main import run_bot
    
    # Не намагаємося керувати event loop, дозволяємо aiogram це робити
    # Використовуємо nest_asyncio для вирішення конфліктів
    run_bot()

if __name__ == "__main__":
    print("Starting Real Estate CRM Telegram Bot...")
    token = os.environ.get('TELEGRAM_API_TOKEN', 'Not set')
    # Виводимо лише перші та останні цифри токену для безпеки
    masked_token = f"{token[:5]}...{token[-4:]}" if len(token) > 10 else "Not set - check your .env file"
    print(f"Bot API Token: {masked_token}")
    
    # Використовуємо nest_asyncio для вирішення конфліктів циклів подій
    try:
        # Запускаємо налаштування бази даних
        loop = asyncio.get_event_loop()
        loop.run_until_complete(setup_app())
        
        # Запускаємо бота
        run_app()
    except KeyboardInterrupt:
        print("Bot stopped by user.")
    except Exception as e:
        print(f"Error running bot: {e}")
