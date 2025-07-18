import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_BOT_TOKEN = "7997139629:AAFLVtfS0cuzjbqnmXkiZI1yCDfpAAXN1IU"
GROQ_API_KEY = "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"

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Eu sou um bot com IA da Groq. Mande sua pergunta!")

async def reply_with_groq(prompt: str) -> str:
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Você é um assistente útil e simpático."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 400
    }

    try:
        response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Erro ao acessar Groq: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    resposta = await reply_with_groq(user_input)
    await update.message.reply_text(resposta)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("✅ Bot iniciado com GroqCloud!")
    app.run_polling()
    from gtts import gTTS
import os

