import os
import requests
from gtts import gTTS
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# Tokens (leia de variáveis de ambiente)
TELEGRAM_BOT_TOKEN = os.getenv("7997139629:AAFLVtfS0cuzjbqnmXkiZI1yCDfpAAXN1IU")
GROQ_API_KEY = os.getenv("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")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# === Função de texto para voz ===
async def enviar_audio(update: Update, texto: str):
    tts = gTTS(text=texto, lang='pt-br')
    tts.save("resposta.mp3")

    with open("resposta.mp3", "rb") as audio_file:
        await update.message.reply_voice(voice=audio_file)

    os.remove("resposta.mp3")

# === Geração de resposta com IA da Groq ===
async def reply_with_groq(prompt: str) -> str:
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "Você é um assistente simpático e direto ao ponto."},
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

# === Comando /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Eu sou um bot com IA da Groq. Mande sua pergunta!")

# === Comando /ajuda ===
async def comando_ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ajuda = (
        "📌 *Comandos disponíveis:*\n\n"
        "/start – Iniciar o bot\n"
        "/ajuda – Mostrar ajuda\n"
        "/voz – O bot fala com você\n"
        "/menu – Mostrar opções rápidas\n"
    )
    await update.message.reply_text(ajuda, parse_mode="Markdown")

# === Comando /voz ===
async def comando_voz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "Olá! Eu sou um bot falante com voz. Me mande uma pergunta!"
    await enviar_audio(update, texto)

# === Comando /menu ===
async def comando_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [["/ajuda", "/voz"], ["/start"]]
    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)
    await update.message.reply_text("📋 Menu de comandos:", reply_markup=markup)

# === Mensagem comum (IA + voz) ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    resposta = await reply_with_groq(user_input)
    await update.message.reply_text(resposta)
    await enviar_audio(update, resposta)

# === Início do bot ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", comando_ajuda))
    app.add_handler(CommandHandler("voz", comando_voz))
    app.add_handler(CommandHandler("menu", comando_menu))

    # Mensagens de texto
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("✅ Bot com Groq iniciado com sucesso!")
    app.run_polling()
