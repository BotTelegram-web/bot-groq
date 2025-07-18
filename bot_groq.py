import os
import logging
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
import http

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Carregar variáveis de ambiente
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Olá! Sou um chatbot com IA Groq.\nDigite qualquer coisa para conversar comigo!\nUse /ajuda para ver os comandos.")

# Comando /ajuda
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛠️ Comandos disponíveis:\n/start - Inicia o bot\n/ajuda - Mostra esta ajuda\n/menu - Exibe opções\n/voz - (em breve)")

# Comando /menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Menu:\n1. Falar com IA\n2. Gerar voz (em breve)\n3. Ver ajuda (/ajuda)")

# Tratar mensagens de texto e responder com IA da Groq
async def responder_com_groq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "Você é um assistente inteligente e amigável."},
            {"role": "user", "content": user_message}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                reply = data['choices'][0]['message']['content']
            else:
                reply = "❌ Erro ao se conectar com a Groq API."

    await update.message.reply_text(reply)

# Inicializar o bot
async def main():
    if not TELEGRAM_BOT_TOKEN or not GROQ_API_KEY:
        raise ValueError("As variáveis TELEGRAM_BOT_TOKEN e GROQ_API_KEY não foram definidas.")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_com_groq))

    print("✅ Bot com Groq iniciado com sucesso!")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
