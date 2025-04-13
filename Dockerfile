# Dockerfile for Real Estate CRM Bot
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project
COPY . .

# Install dependencies
RUN pip install --upgrade pip     && pip install poetry     && poetry export -f requirements.txt --output requirements.txt --without-hashes     && pip install -r requirements.txt

# Environment
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
# Запуск планувальника в окремому процесі
CMD ["sh", "-c", "python -m src.bot.scheduler & python main.py"]
