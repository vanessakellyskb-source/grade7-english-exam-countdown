GRADE 7 TELEGRAM COUNTDOWN BOT

1. Keep your new BotFather token secret. Never put it in source code or screenshots.
2. Get the group chat ID (a negative number, often beginning with -100) using a trusted method or a temporary getUpdates call after sending a message to the group. Do not share your token.
3. Configure environment variables TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID on your hosting platform.
4. Install dependencies: pip install -r requirements.txt
5. Run: python bot.py
6. Pin the first countdown image in Telegram.

IMPORTANT: The process must run continuously on a hosting service. This sample keeps the message ID only in memory, so restarting it posts a new message; pin the new message and remove the old one. Images refresh every 60 seconds. Seconds reflect the instant of each refresh, not a live ticking clock. Target is midnight at the start of 26 November 2026 UAE time.
