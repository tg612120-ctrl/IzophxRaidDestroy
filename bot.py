import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def send_custom_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # Custom message extract karna
    if context.args:
        message_text = " ".join(context.args)
    else:
        message_text = "hello"
    
    end_time = asyncio.get_event_loop().time() + 60  # Exact 1 minute (60 seconds)
    
    # Speed ko maximum rakhne ke liye parallel batches chalana
    while asyncio.get_event_loop().time() < end_time:
        tasks = []
        # Ek batch mein 15 messages ek sath fire honge (Fastest safe group limit)
        for _ in range(15):
            if asyncio.get_event_loop().time() >= end_time:
                break
            tasks.append(context.bot.send_message(chat_id=chat_id, text=message_text))
        
        if tasks:
            # Sabhi ko ek sath bhej kar error catch karna taaki bot crash na ho
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if isinstance(res, Exception):
                    # Agar Telegram ne roka, toh chhota sa pause le lega
                    await asyncio.sleep(0.5)
        
        # Batch ke beech mein bilkul na ke barabar gap taaki speed top notch rahe
        await asyncio.sleep(0.05)

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN set nahi hai!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("send", send_custom_message))
    
    print("Turbo Speed Bot start ho raha hai...")
    app.run_polling()

if __name__ == "__main__":
    main()
            
