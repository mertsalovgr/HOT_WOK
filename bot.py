from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, CHANNEL_USERNAME

WELCOME_MESSAGE = (
    "Привет! 👋\n"
    "*HOT WOK* — твоя любимая лапша в Тбилиси 🍜\n"
    "Здесь ты можешь выбрать удобную платформу для заказа или получить эксклюзивную скидку!👇"
)

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔹 Заказать через Wolt", url="https://wolt.com/ka/geo/tbilisi/restaurant/hott-wok")],
    [InlineKeyboardButton("🔹 Заказать через Bolt Food", url="https://food.bolt.eu/ru-RU/15/p/135577-hot-wok")],
    [InlineKeyboardButton("🔹 Заказать через Яндекс Go", url="yandextaxi://external?service=eats&href=%2Frestaurant%2Fhot_wok_sn25t%3Futm_campaign%3Dsuperapp_taxi_web%26utm_medium%3Dreferral%26utm_source%3Drst_shared_link")],
    [InlineKeyboardButton("🔹 Заказать через Glovo", url="https://ufv9.adj.st?adjust_deeplink=glovoapp%3A%2F%2Fopen%3Flink_type%3Dstore%26store_id%3D504684&adjust_t=s321jkn")],
    [InlineKeyboardButton("🎁 Получить секретный подарок", callback_data="gift")]
])

async def is_user_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=WELCOME_MESSAGE,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == "gift":
        if await is_user_subscribed(user_id, context):
            await query.answer()
            await query.edit_message_text("🎉 Спасибо за подписку! Вот твой подарок: [Секретный бонус](https://t.me/+zGG8uX1HJdI1NDZi)", parse_mode='Markdown')
        else:
            await query.answer()
            await query.edit_message_text(
                "🙌 Чтобы получить подарок, подпишись на наш канал:\n"
                "👉 [Подписаться](https://t.me/+zGG8uX1HJdI1NDZi)\n\n"
                "После подписки нажми снова на кнопку 🎁.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔁 Проверить подписку", callback_data="gift")]
                ])
            )

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    print("Бот запущен...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())