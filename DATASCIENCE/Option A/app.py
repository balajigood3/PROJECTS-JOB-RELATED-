import os

# Create the data folder automatically in the correct directory
data_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(data_dir, exist_ok=True)

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from rag import RAGSystem

# Initialize RAG - it will now find the 'data' folder
rag = RAGSystem()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to AI RAG Bot!\n\n"
        "Use:\n"
        "/ask <your question>\n"
        "/help"
    )

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/ask What is AI?\n"
        "/help"
    )

# /ask
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)

    if not query:
        await update.message.reply_text("❌ Please provide a question.\nExample: /ask What is AI?")
        return

    await update.message.reply_text("Thinking...")

    answer, sources = rag.ask(query)

    response = f"Answer:\n{answer}\n\n Sources:\n"
    for i, src in enumerate(sources, 1):
        response += f"{i}. {src[:100]}...\n"

    await update.message.reply_text(response)

# MAIN
if __name__ == "__main__":
    TOKEN = "YOUR TELEGRAM BOT TOKEN" # I verified with my key and hide it due to safety reason as per telegram bot and github T&C

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ask", ask))

    print("🚀 Bot running...")
    app.run_polling()

