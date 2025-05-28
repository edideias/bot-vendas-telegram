
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

# Produtos
products = {
    "iptv": {
        "name": "IPTV Mensal",
        "price": 25,
        "instructions": "📥 IPTV ativado! Baixe o app 'IPTV Pro' e use esta lista M3U: https://seulink.com/iptv"
    },
    "vpn": {
        "name": "Internet VPN Mensal",
        "price": 25,
        "instructions": "🔐 VPN ativado! Baixe o app 'WireGuard' e importe este arquivo: https://seulink.com/vpn"
    }
}

PIX_KEY = "seu_email@pix.com"
ADMIN_ID = 6801764001  # Substitua pelo seu ID do Telegram
BOT_TOKEN = os.getenv("7080244498:AAEXs1jqn_nJzx6MoLilgQin6bqpHXl0R30")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("📺 IPTV - R$25", callback_data="iptv")],
        [InlineKeyboardButton("🌐 Internet VPN - R$25", callback_data="vpn")]
    ]
    await update.message.reply_text(
        "👋 Olá! Escolha um serviço:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product = query.data
    context.user_data["product"] = product

    await query.edit_message_text(
        f"🛒 Produto: {products[product]['name']}
💰 Valor: R$25,00

"
        f"Para pagar, envie R$25,00 via Pix para a chave:
🔑 `{PIX_KEY}`

"
        "Após o pagamento, clique em 'Já paguei'.",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Já paguei", callback_data="confirm")]])
    )

async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product = context.user_data.get("product", "iptv")
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📥 Solicitação de ativação:
Usuário: @{query.from_user.username} (ID: {query.from_user.id})
Produto: {product.upper()}",
    )
    await query.edit_message_text("✅ Pedido enviado para aprovação. Aguarde a liberação em até 15 minutos.")

async def admin_activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    try:
        _, uid, product = update.message.text.split()
        await context.bot.send_message(chat_id=int(uid), text=products[product]["instructions"])
        await update.message.reply_text("✅ Produto enviado.")
    except:
        await update.message.reply_text("❌ Erro! Use: /aprovar <id> <iptv|vpn>")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aprovar", admin_activate))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(iptv|vpn)$"))
    app.add_handler(CallbackQueryHandler(confirm_payment, pattern="^confirm$"))

    app.run_polling()

if __name__ == "__main__":
    main()
