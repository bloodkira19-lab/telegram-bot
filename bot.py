import random
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8217989034:AAHVFQmarB8_2gDex_ukEBRwq3bsi2cWdx4"
STICKER_SET = "YonseiCards_by_fStikBot"

async def start(update, context):
    await update.message.reply_text(
        "🎲 Envie /sorteio para sortear uma carta aleatória!"
    )

async def sorteio(update, context):
    sticker_set = await context.bot.get_sticker_set(STICKER_SET)
    sticker = random.choice(sticker_set.stickers)
    await update.message.reply_sticker(sticker.file_id)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("sorteio", sorteio))

print("🤖 Bot de figurinhas rodando...")
app.run_polling()
