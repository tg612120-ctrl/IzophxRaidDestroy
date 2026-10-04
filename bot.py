import os
import asyncio

from telegram import Update
from telegram.error import RetryAfter, TelegramError
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")


async def send_messages(context, chat_id, message_text, end_time):
    while asyncio.get_running_loop().time() < end_time:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=message_text
            )

            # Normal pacing — group flood limits ko trigger na karne ke liye
            await asyncio.sleep(1)

        except RetryAfter as e:
            # Telegram jitna wait bolta hai, utna hi wait karo
            await asyncio.sleep(float(e.retry_after) + 0.5)

        except TelegramError as e:
            print(f"Telegram error: {e}")
            await asyncio.sleep(2)

        except Exception as e:
            print(f"Unexpected error: {e}")
            await asyncio.sleep(2)


async def send_custom_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    chat_id = update.effective_chat.id

    if context.args:
        message_text = " ".join(context.args)
    else:
        message_text = "hello"

    end_time = asyncio.get_running_loop().time() + 60

    await send_messages(
        context,
        chat_id,
        message_text,
        end_time
    )


def main():
    if not TOKEN:
        print("Error: BOT_TOKEN set nahi hai!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("send", send_custom_message)
    )

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
