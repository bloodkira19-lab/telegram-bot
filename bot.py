# ===== IMPORTS =====
import random
import re
import json
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler
)

# ===== CONSTANTES =====
ARQUIVO_PONTOS = "pontos.json"
TOKEN = "SEU_TOKEN_AQUI"
STICKER_SET = "YonseiCards_by_fStikBot"

# ===== MENSALIDADES =====
MENSALIDADES = {
    "direito": {"nome": "𝐃𝐢𝐫𝐞𝐢𝐭𝐨", "valor": 4300},
    "cinema": {"nome": "𝐂𝐢𝐧𝐞𝐦𝐚", "valor": 2135},
    "moda": {"nome": "𝐌𝐨𝐝𝐚", "valor": 2300},
    "sociais": {"nome": "𝐂𝐢𝐞̂𝐧𝐜𝐢𝐚𝐬 𝐒𝐨𝐜𝐢𝐚𝐢𝐬", "valor": 1800},
    "musica": {"nome": "𝐌𝐮́𝐬𝐢𝐜𝐚", "valor": 1790},
    "aero": {"nome": "𝐄𝐧𝐠𝐞𝐧𝐡𝐚𝐫𝐢𝐚 𝐀𝐞𝐫𝐨𝐞𝐬𝐩𝐚𝐜𝐢𝐚𝐥", "valor": 5000},
    "vet": {"nome": "𝐕𝐞𝐭𝐞𝐫𝐢𝐧𝐚́𝐫𝐢𝐚", "valor": 4800},
    "jornal": {"nome": "𝐉𝐨𝐫𝐧𝐚𝐥𝐢𝐬𝐦𝐨", "valor": 1950}
}

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
    if user_id not in pontos:
        pontos[user_id] = {
            "w": 0,
            "energia": 100,
            "vida": 100
        }

# ===== COMANDOS =====
async def start(update, context):
    await update.message.reply_text(
        "🎓 *Sistema Yonsei*\n\n"
        "/sorteio – carta aleatória\n"
        "/pontuar +10 – alterar ₩˚₊‧\n"
        "/energia +10 – alterar ✶˚₊‧\n"
        "/vida +10 – alterar ♡˚₊‧\n"
        "/mensalidade – pagar faculdade\n"
        "/pontos – ver status\n"
        "/reset – resetar tudo",
        parse_mode="Markdown"
    )

async def sorteio(update, context):
    sticker_set = await context.bot.get_sticker_set(STICKER_SET)
    sticker = random.choice(sticker_set.stickers)
    await update.message.reply_sticker(sticker.file_id)

# ===== ₩ =====
async def pontuar(update, context):
    user = update.effective_user
    user_id = str(user.id)

    match = re.search(r'([+-]\d+)', " ".join(context.args))
    if not match:
        await update.message.reply_text("❌ Use /pontuar +10 ou -5")
        return

    valor = int(match.group(1))
    garantir_usuario(user_id)

    pontos[user_id]["w"] += valor
    salvar_pontos(pontos)

    await update.message.reply_text(
        f"₩˚₊‧ {user.first_name}\n"
        f"Alteração: {valor:+}₩˚₊‧\n"
        f"Total: {pontos[user_id]['w']}₩˚₊‧"
    )

# ===== ✶ =====
async def alterar_energia(update, context):
    user_id = str(update.effective_user.id)
    match = re.search(r'([+-]\d+)', " ".join(context.args))

    if not match:
        await update.message.reply_text("❌ Use /energia +10 ou -5")
        return

    valor = int(match.group(1))
    garantir_usuario(user_id)

    pontos[user_id]["energia"] = max(0, pontos[user_id]["energia"] + valor)
    salvar_pontos(pontos)

    await update.message.reply_text(
        f"✶˚₊‧ Energia: {pontos[user_id]['energia']}"
    )

# ===== ♡ =====
async def alterar_vida(update, context):
    user_id = str(update.effective_user.id)
    match = re.search(r'([+-]\d+)', " ".join(context.args))

    if not match:
        await update.message.reply_text("❌ Use /vida +10 ou -5")
        return

    valor = int(match.group(1))
    garantir_usuario(user_id)

    pontos[user_id]["vida"] = max(0, pontos[user_id]["vida"] + valor)
    salvar_pontos(pontos)

    await update.message.reply_text(
        f"♡˚₊‧ Vida: {pontos[user_id]['vida']}"
    )

# ===== STATUS =====
async def ver_pontos(update, context):
    user = update.effective_user
    user_id = str(user.id)

    garantir_usuario(user_id)

    await update.message.reply_text(
        f"📊 *Status de {user.first_name}*\n\n"
        f"₩˚₊‧ ₩: {pontos[user_id]['w']}\n"
        f"✶˚₊‧ Energia: {pontos[user_id]['energia']}\n"
        f"♡˚₊‧ Vida: {pontos[user_id]['vida']}",
        parse_mode="Markdown"
    )

# ===== RESET =====
async def reset_pontos(update, context):
    user_id = str(update.effective_user.id)

    pontos[user_id] = {
        "w": 0,
        "energia": 100,
        "vida": 100
    }
    salvar_pontos(pontos)

    await update.message.reply_text("🔄 Status resetado.")

# ===== MENSALIDADE =====
async def mensalidade(update, context):
    keyboard = [
        [InlineKeyboardButton(
            f"{dados['nome']}: {dados['valor']}₩˚₊‧",
            callback_data=f"pagar|{curso}"
        )]
        for curso, dados in MENSALIDADES.items()
    ]

    await update.message.reply_text(
        "📚 *𝐌𝐞𝐧𝐬𝐚𝐥𝐢𝐝𝐚𝐝𝐞𝐬*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def pagar_mensalidade(update, context):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    garantir_usuario(user_id)

    curso_id = query.data.split("|")[1]
    curso = MENSALIDADES[curso_id]
    valor = curso["valor"]

    if pontos[user_id]["w"] < valor:
        await query.edit_message_text(
            f"❌ Saldo insuficiente\n"
            f"Você tem {pontos[user_id]['w']}₩˚₊‧"
        )
        return

    pontos[user_id]["w"] -= valor
    salvar_pontos(pontos)

    await query.edit_message_text(
        f"✅ *Mensalidade paga*\n\n"
        f"{curso['nome']}\n"
        f"-{valor}₩˚₊‧\n"
        f"Saldo: {pontos[user_id]['w']}₩˚₊‧",
        parse_mode="Markdown"
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
app.add_handler(CommandHandler("mensalidade", mensalidade))
app.add_handler(CallbackQueryHandler(pagar_mensalidade, pattern="^pagar\\|"))

print("🤖 Bot rodando via webhook...")

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN,
    webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
)
