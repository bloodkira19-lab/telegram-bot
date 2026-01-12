# ===== IMPORTS =====
import random
import re
import json
import os
from telegram.ext import ApplicationBuilder, CommandHandler

# ===== CONSTANTES =====
ARQUIVO_PONTOS = "pontos.json"
TOKEN = "8217989034:AAHVFQmarB8_2gDex_ukEBRwq3bsi2cWdx4"
STICKER_SET = "YonseiCards_by_fStikBot"

# ===== PERSISTÊNCIA =====
def carregar_pontos():
    try:
        with open(ARQUIVO_PONTOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def salvar_pontos(pontos):
    with open(ARQUIVO_PONTOS, "w", encoding="utf-8") as f:
        json.dump(pontos, f, indent=4, ensure_ascii=False)

# ===== DADOS =====
pontos = carregar_pontos()

def garantir_usuario(user_id):
    if user_id not in pontos or not isinstance(pontos[user_id], dict):
        pontos[user_id] = {
            "w": 0,
            "energia": 100,
            "vida": 100
        }

# ===== FUNÇÕES =====
async def start(update, context):
    await update.message.reply_text(
        "🎮 Comandos disponíveis:\n"
        "/sorteio – carta aleatória\n"
        "/pontuar +10 ou -5 – altera ₩\n"
        "/energia +10 ou -5 – altera ⚡\n"
        "/vida +10 ou -5 – altera ❤️\n"
        "/pontos – ver status\n"
        "/reset – resetar tudo"
    )

async def sorteio(update, context):
    sticker_set = await context.bot.get_sticker_set(STICKER_SET)
    sticker = random.choice(sticker_set.stickers)
    await update.message.reply_sticker(sticker.file_id)

# ===== W (₩) =====
async def pontuar(update, context):
    user = update.effective_user
    user_id = str(user.id)

    texto = " ".join(context.args)
    match = re.search(r'([+-]\d+)', texto)

    if not match:
        await update.message.reply_text("❌ Use: /pontuar +10 ou /pontuar -5")
        return

    valor = int(match.group(1))
    garantir_usuario(user_id)

    pontos[user_id]["w"] += valor
    salvar_pontos(pontos)

    await update.message.reply_text(
        f"💰 {user.first_name}\n"
        f"Alteração: {valor:+}₩\n"
        f"Total: {pontos[user_id]['w']}₩"
    )

# ===== ENERGIA (⚡) =====
async def alterar_energia(update, context):
    user = update.effective_user
    user_id = str(user.id)

    texto = " ".join(context.args)
    match = re.search(r'([+-]\d+)', texto)

    if not match:
        await update.message.reply_text("❌ Use: /energia +10 ou /energia -5")
        return

    valor = int(match.group(1))
    garantir_usuario(user_id)

    pontos[user_id]["energia"] += valor
    if pontos[user_id]["energia"] < 0:
        pontos[user_id]["energia"] = 0

    salvar_pontos(pontos)

    await update.message.reply_text(
        f"⚡ Energia de {user.first_name}\n"
        f"Alteração: {valor:+}\n"
        f"Total: {pontos[user_id]['energia']}⚡"
    )

# ===== VIDA (❤️) =====
async def alterar_vida(update, context):
    user = update.effective_user
    user_id = str(user.id)

    texto = " ".join(context.args)
    match = re.search(r'([+-]\d+)', texto)

    if not match:
        await update.message.reply_text("❌ Use: /vida +10 ou /vida -5")
        return

    valor = int(match.group(1))
    garantir_usuario(user_id)

    pontos[user_id]["vida"] += valor
    if pontos[user_id]["vida"] < 0:
        pontos[user_id]["vida"] = 0

    salvar_pontos(pontos)

    await update.message.reply_text(
        f"❤️ Vida de {user.first_name}\n"
        f"Alteração: {valor:+}\n"
        f"Total: {pontos[user_id]['vida']}❤️"
    )

# ===== VER STATUS =====
async def ver_pontos(update, context):
    user = update.effective_user
    user_id = str(user.id)

    garantir_usuario(user_id)

    await update.message.reply_text(
        f"📊 Status de {user.first_name}\n\n"
        f"💰 ₩: {pontos[user_id]['w']}\n"
        f"⚡ Energia: {pontos[user_id]['energia']}\n"
        f"❤️ Vida: {pontos[user_id]['vida']}"
    )

# ===== RESET =====
async def reset_pontos(update, context):
    user = update.effective_user
    user_id = str(user.id)

    pontos[user_id] = {
        "w": 0,
        "energia": 100,
        "vida": 100
    }
    salvar_pontos(pontos)

    await update.message.reply_text(
        f"🔄 {user.first_name}, seus status foram resetados."
    )

# ===== WEBHOOK =====
PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("sorteio", sorteio))
app.add_handler(CommandHandler("pontuar", pontuar))
app.add_handler(CommandHandler("energia", alterar_energia))
app.add_handler(CommandHandler("vida", alterar_vida))
app.add_handler(CommandHandler("pontos", ver_pontos))
app.add_handler(CommandHandler("reset", reset_pontos))

print("🤖 Bot rodando via webhook...")

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN,
    webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
)
