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
ADMIN_ID = 6801764001  # Substitua pelo seu ID real do Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Agora está correto!

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
        f"🛒 Produto: {products[product]['name']}\n"
        f"💰 Valor: R$25,00\n\n"
        f"Para pagar, envie R$25,00 via Pix para a chave:\n🔑 `{PIX_KEY}`\n\n"
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
        text=f"📥 Solicitação de ativação:\n"
             f"Usuário: @{query.from_user.username} (ID: {query.from
