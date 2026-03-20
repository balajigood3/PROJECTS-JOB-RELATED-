import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from vision import VisionModel

vision = VisionModel()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Vision AI Bot\n\n"
        "Send me an image or use:\n"
        "/image (then upload)\n"
        "/help"
    )

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "Send an image directly\n"
        "/image (then upload image)\n"
    )

# Handle images
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    file_path = "temp.jpg"
    await file.download_to_drive(file_path)

    await update.message.reply_text("Processing image...")

    caption, keywords = vision.describe_image(file_path)

    response = f"Caption:\n{caption}\n\n Tags:\n{', '.join(keywords)}"

    await update.message.reply_text(response)

    os.remove(file_path)

# MAIN
if __name__ == "__main__":
    TOKEN = "YOUR TELEGRAM BOT TOKEN"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # image handler
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    print("Vision Bot Running...")
    app.run_polling()
    