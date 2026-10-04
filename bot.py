import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def spam_message(context, chat_id, message_text, end_time):
    # Ek saath bohot saare concurrent requests bhejne ke liye task list
    while asyncio.get_event_loop().time() < end_time:
        tasks = []
        # Ek batch mein multiple messages ek sath bhejenge
        for _ in range(10):  # Ek baar mein 10 parallel messages
            if asyncio.get_event_loop().time() >= end_time:
                break
            tasks.append(context.bot.send_message(chat_id=chat_id, text=message_text))
        
        if tasks:
            # Sabhi messages ko ek sath fire karna
            await asyncio.gather(*tasks, return_exceptions=True)

async def send_custom_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    if context.args:
        message_text = " ".join(context.args)
    else:
        message_text = "hello"
    
    end_time = asyncio.get_event_loop().time() + 60  # Exact 1 minute
    
    # High-speed spam function call karna
    await spam_message(context, chat_id, message_text, end_time)

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN set nahi hai!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("send", send_custom_message))
    
    print("High-Speed Bot start ho raha hai...")
    app.run_polling()

if __name__ == "__main__":
    main()
