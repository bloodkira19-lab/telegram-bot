# ===== IMPORTS =====
import random
import re
import json
from telegram.ext import ApplicationBuilder, CommandHandler

ARQUIVO_PONTOS = "pontos.json"

def carregar_pontos():
    try:
        with open(ARQUIVO_PONTOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def salvar_pontos(pontos):
    with open(ARQUIVO_PONTOS, "w", encoding="utf-8") as f:
        json.dump(pontos, f, indent=4)

# ===== VARIÁVEIS =====
pontos = carregar_pontos()

TOKEN = "8217989034:AAHVFQmarB8_2gDex_ukEBRwq3bsi2cWdx4"
STICKER_SET = "YonseiCards_by_fStikBot"

# ===== FUNÇÕES =====
async def start(update, context):
    await update.message.reply_text(
        "🎲 Envie /sorteio para sortear uma carta aleatória!"
    )

async def sorteio(update, context):
    sticker_set = await context.bot.get_sticker_set(STICKER_SET)
    sticker = random.choice(sticker_set.stickers)
    await update.message.reply_sticker(sticker.file_id)

async def reset_pontos(update, context):
    user_id = str(update.effective_user.id)
    nome = update.effective_user.first_name

    pontos[user_id] = 0
    salvar_pontos(pontos)

    await update.message.reply_text(
        f"♻️ {nome}, seus pontos foram resetados para 0."
    )

async def pontuar(update, context):
    user = update.effective_user
    user_id = str(user.id)

    texto = " ".join(context.args)

    if not texto:
        await update.message.reply_text(
            "❌ Use assim:\n"
            "/pontuar +10\n"
            "/pontuar -5"
        )
        return

    match = re.search(r'([+-]\d+)', texto)

    if not match:
        await update.message.reply_text("❌ Não encontrei pontos no texto.")
        return

    valor = int(match.group(1))

    pontos[user_id] = pontos.get(user_id, 0) + valor
    salvar_pontos(pontos)

    await update.message.reply_text(
        f"⭐ {user.first_name}\n"
        f"Alteração: {valor:+}\n"
        f"Total de pontos: {pontos[user_id]}"
    )

async def ver_pontos(update, context):
    user_id = str(update.effective_user.id)
    total = pontos.get(user_id, 0)

    await update.message.reply_text(f"⭐ Você tem {total} pontos.")

# ===== APP =====
app = ApplicationBuilder().token(TOKEN).build()

# ===== HANDLERS =====
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("sorteio", sorteio))
app.add_handler(CommandHandler("pontuar", pontuar))
app.add_handler(CommandHandler("pontos", ver_pontos))
app.add_handler(CommandHandler("reset", reset_pontos))

# ===== START BOT =====
print("🤖 Bot de figurinhas rodando...")
app.run_polling()
