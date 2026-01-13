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
TOKEN = "8217989034:AAHVFQmarB8_2gDex_ukEBRwq3bsi2cWdx4"
ARQUIVO_PONTOS = "pontos.json"

FOTO_CONCESSIONARIA = "6842878824"
FOTO_IMOBILIARIA = "6842878824"

STICKER_SET = "YonseiCards_by_fStikBot"

ENERGIA_MAX = 400
VIDA_MAX = 100

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

# ===== CONCESSIONÁRIA =====
CONCESSIONARIA = {
    "usado": {
        "nome": "𝐀𝐮𝐭𝐨𝐦𝐨́𝐯𝐞𝐥 usado",
        "parcelas": 12,
        "parcela": 833
    },
    "zerado_antigo": {
        "nome": "𝐀𝐮𝐭𝐨𝐦𝐨́𝐯𝐞𝐥 zerado (fora de linha)",
        "parcelas": 12,
        "parcela": 1000
    },
    "zerado_atual": {
        "nome": "𝐀𝐮𝐭𝐨𝐦𝐨́𝐯𝐞𝐥 zerado (atual)",
        "parcelas": 12,
        "parcela": 8333
    }
}

# ===== IMOBILIÁRIA =====
IMOBILIARIA = {
    "simples": {"nome": "𝐂𝐚𝐬𝐚/AP simples", "aluguel": 450},
    "medio": {"nome": "𝐂𝐚𝐬𝐚/AP médio", "aluguel": 750},
    "luxo": {"nome": "𝐂𝐚𝐬𝐚/AP luxo", "aluguel": 2340}
}

# ===== PERSISTÊNCIA =====
def carregar_pontos():
    try:
        with open(ARQUIVO_PONTOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def salvar_pontos():
    with open(ARQUIVO_PONTOS, "w", encoding="utf-8") as f:
        json.dump(pontos, f, indent=4, ensure_ascii=False)

pontos = carregar_pontos()

def garantir_usuario(user_id):
    if user_id not in pontos:
        pontos[user_id] = {
            "w": 0,
            "vida": VIDA_MAX,
            "energia": ENERGIA_MAX,
            "parcelas": [],
            "aluguel": []
        }
# ===== ♡˚₊‧ VIDA =====
async def alterar_vida(update, context):
    user = update.effective_user
    user_id = str(user.id)
    garantir_usuario(user_id)

    match = re.search(r'([+-]\d+)', " ".join(context.args))
    if not match:
        await update.message.reply_text("❌ Use /vida +10 ou -5")
        return

    valor = int(match.group(1))

    pontos[user_id]["vida"] = max(
        0,
        min(VIDA_MAX, pontos[user_id]["vida"] + valor)
    )

    salvar_pontos()

    await update.message.reply_text(
        f"♡˚₊‧ {user.first_name}\n"
        f"Alteração: {valor:+}♡˚₊‧\n"
        f"Total: {pontos[user_id]['vida']}/{VIDA_MAX}♡˚₊‧"
    )
# ===== ✶˚₊‧ ENERGIA =====
async def alterar_energia(update, context):
    user = update.effective_user
    user_id = str(user.id)
    garantir_usuario(user_id)

    match = re.search(r'([+-]\d+)', " ".join(context.args))
    if not match:
        await update.message.reply_text("❌ Use /energia +10 ou -5")
        return

    valor = int(match.group(1))

    pontos[user_id]["energia"] = max(
        0,
        min(ENERGIA_MAX, pontos[user_id]["energia"] + valor)
    )

    salvar_pontos()

    await update.message.reply_text(
        f"✶˚₊‧ {user.first_name}\n"
        f"Alteração: {valor:+}✶˚₊‧\n"
        f"Total: {pontos[user_id]['energia']}/{ENERGIA_MAX}✶˚₊‧"
    )
# ===== ₩˚₊‧ WON =====
async def pontuar(update, context):
    user = update.effective_user
    user_id = str(user.id)
    garantir_usuario(user_id)

    match = re.search(r'([+-]\d+)', " ".join(context.args))
    if not match:
        await update.message.reply_text("❌ Use /pontuar +10 ou -5")
        return

    valor = int(match.group(1))
    pontos[user_id]["w"] += valor

    salvar_pontos()

    await update.message.reply_text(
        f"₩˚₊‧ {user.first_name}\n"
        f"Alteração: {valor:+}₩˚₊‧\n"
        f"Total: {pontos[user_id]['w']}₩˚₊‧"
    )

# ===== START =====
async def start(update, context):
    await update.message.reply_text(
        "🎓 *Sistema Yonsei*\n\n"
        "/imobiliaria\n"
        "/concessionaria\n"
        "/mensalidade\n"
        "/pontos",
        parse_mode="Markdown"
    )

# ===== IMOBILIÁRIA =====
async def imobiliaria(update, context):
    keyboard = [
        [InlineKeyboardButton(
            f"{v['nome']} — ₩{v['aluguel']}/mês",
            callback_data=f"alugar|{k}"
        )]
        for k, v in IMOBILIARIA.items()
    ]

    await update.message.reply_photo(
        photo=FOTO_IMOBILIARIA,
        caption="🏠 *𝐈𝐦𝐨𝐛𝐢𝐥𝐢𝐚́𝐫𝐢𝐚*\nEscolha um imóvel:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def alugar_callback(update, context):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    garantir_usuario(user_id)

    ap_id = query.data.split("|")[1]
    ap = IMOBILIARIA[ap_id]

    pontos[user_id]["aluguel"].append({
        "nome": ap["nome"],
        "valor": ap["aluguel"]
    })

    salvar_pontos()

    await query.edit_message_text(
        f"🏠 *Imóvel alugado*\n\n{ap['nome']}\n₩{ap['aluguel']}/mês",
        parse_mode="Markdown"
    )

# ===== CONCESSIONÁRIA =====
async def concessionaria(update, context):
    keyboard = [
        [InlineKeyboardButton(
            f"{v['nome']} — ₩{v['parcela']} x{v['parcelas']}",
            callback_data=f"carro|{k}"
        )]
        for k, v in CONCESSIONARIA.items()
    ]

    await update.message.reply_photo(
        photo=FOTO_CONCESSIONARIA,
        caption="🚗 *𝐂𝐨𝐧𝐜𝐞𝐬𝐬𝐢𝐨𝐧𝐚́𝐫𝐢𝐚*\nEscolha um veículo:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def comprar_carro_callback(update, context):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    garantir_usuario(user_id)

    carro_id = query.data.split("|")[1]
    carro = CONCESSIONARIA[carro_id]

    pontos[user_id]["parcelas"].append({
        "nome": carro["nome"],
        "valor": carro["parcela"],
        "restantes": carro["parcelas"]
    })

    salvar_pontos()

    await query.edit_message_text(
        f"🚗 *Compra realizada*\n\n{carro['nome']}\n"
        f"{carro['parcelas']}x de ₩{carro['parcela']}",
        parse_mode="Markdown"
    )

# ===== COBRANÇA MENSAL =====
async def cobrar_mes(update, context):
    for dados in pontos.values():

        # parcelas
        novas = []
        for p in dados["parcelas"]:
            if dados["w"] >= p["valor"]:
                dados["w"] -= p["valor"]
                p["restantes"] -= 1
                if p["restantes"] > 0:
                    novas.append(p)
            else:
                novas.append(p)
        dados["parcelas"] = novas

        # aluguel
        for a in dados["aluguel"]:
            if dados["w"] >= a["valor"]:
                dados["w"] -= a["valor"]

    salvar_pontos()
    await update.message.reply_text("📆 Mês encerrado. Cobranças aplicadas.")

# ===== STATUS =====
async def ver_pontos(update, context):
    user_id = str(update.effective_user.id)
    garantir_usuario(user_id)

    d = pontos[user_id]
    await update.message.reply_text(
        f"📊 *Status*\n\n"
        f"₩˚₊‧ {d['w']}\n"
        f"✶˚₊‧ {d['energia']}/{ENERGIA_MAX}\n"
        f"♡˚₊‧ {d['vida']}/{VIDA_MAX}",
        parse_mode="Markdown"
    )

# ===== MENSALIDADE =====
async def mensalidade(update, context):
    keyboard = [
        [InlineKeyboardButton(
            f"{v['nome']} — ₩{v['valor']}",
            callback_data=f"mensal|{k}"
        )]
        for k, v in MENSALIDADES.items()
    ]

    await update.message.reply_text(
        "📚 *Mensalidades*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def pagar_mensalidade(update, context):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    garantir_usuario(user_id)

    curso = MENSALIDADES[query.data.split("|")[1]]
    valor = curso["valor"]

    if pontos[user_id]["w"] < valor:
        await query.edit_message_text("❌ Saldo insuficiente.")
        return

    pontos[user_id]["w"] -= valor
    salvar_pontos()

    await query.edit_message_text(
        f"✅ {curso['nome']} paga\nSaldo: ₩{pontos[user_id]['w']}",
        parse_mode="Markdown"
    )

# ===== APP =====
PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("imobiliaria", imobiliaria))
app.add_handler(CommandHandler("concessionaria", concessionaria))
app.add_handler(CommandHandler("mensalidade", mensalidade))
app.add_handler(CommandHandler("pontos", ver_pontos))
app.add_handler(CommandHandler("cobrar_mes", cobrar_mes))

app.add_handler(CallbackQueryHandler(alugar_callback, pattern="^alugar\\|"))
app.add_handler(CallbackQueryHandler(comprar_carro_callback, pattern="^carro\\|"))
app.add_handler(CallbackQueryHandler(pagar_mensalidade, pattern="^mensal\\|"))
app.add_handler(CommandHandler("vida", alterar_vida))
app.add_handler(CommandHandler("energia", alterar_energia))
app.add_handler(CommandHandler("pontuar", pontuar))

print("🤖 Bot rodando...")

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN,
    webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
)



