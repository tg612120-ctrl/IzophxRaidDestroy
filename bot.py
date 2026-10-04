import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Environment variable se token uthayega
TOKEN = os.getenv("BOT_TOKEN")

async def send_custom_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # Custom message extract karna (e.g., /send hello cutie)
    if context.args:
        message_text = " ".join(context.args)
    else:
        message_text = "hello"
    
    end_time = asyncio.get_event_loop().time() + 60  # Exact 1 minute
    
    # Bina kisi delay ke full speed mein spam karna
    while asyncio.get_event_loop().time() < end_time:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message_text)
        except Exception:
            # Agar rate limit ya koi error aaye toh loop crash na ho
            pass

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN environment variable set nahi hai!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("send", send_custom_message))
    
    print("Bot start ho raha hai...")
    app.run_polling()

if __name__ == "__main__":
    main()
      
