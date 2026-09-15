from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8967126323:AAEK21B0MpsoNmi8t_kS0hjmG2f2H5Q1S2g"
ADMIN_ID = 688966791

(
    NAME,
    PHONE,
    DOG_NAME,
    BREED,
    AGE,
    WEIGHT,
    SERVICE,
    NOTES,
) = range(8)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🐾 Записаться на знакомство"]]
    await update.message.reply_text(
        "Добро пожаловать в Хвостатый клуб 🐾",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        ),
    )

async def begin_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Как вас зовут?")
    return NAME

async def get_name(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Ваш телефон?")
    return PHONE

async def get_phone(update, context):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Кличка собаки?")
    return DOG_NAME

async def get_dog_name(update, context):
    context.user_data["dog_name"] = update.message.text
    await update.message.reply_text("Порода?")
    return BREED

async def get_breed(update, context):
    context.user_data["breed"] = update.message.text
    await update.message.reply_text("Возраст собаки?")
    return AGE

async def get_age(update, context):
    context.user_data["age"] = update.message.text
    await update.message.reply_text("Вес собаки?")
    return WEIGHT

async def get_weight(update, context):
    context.user_data["weight"] = update.message.text
    await update.message.reply_text(
        "Какая услуга интересует?\n"
        "Дневной сад / Передержка / И то и другое"
    )
    return SERVICE

async def get_service(update, context):
    context.user_data["service"] = update.message.text
    await update.message.reply_text(
        "Есть ли особенности характера, поведения или здоровья?"
    )
    return NOTES

async def finish(update, context):
    context.user_data["notes"] = update.message.text

    text = f"""
🐾 Новая заявка

👤 Владелец: {context.user_data['name']}
📞 Телефон: {context.user_data['phone']}

🐶 Кличка: {context.user_data['dog_name']}
🐕 Порода: {context.user_data['breed']}
🎂 Возраст: {context.user_data['age']}
⚖️ Вес: {context.user_data['weight']}

📌 Услуга: {context.user_data['service']}

📝 Особенности:
{context.user_data['notes']}
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text,
    )

    await update.message.reply_text(
        "Спасибо! Мы получили заявку и скоро свяжемся с вами 🐾"
    )

    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^🐾 Записаться на знакомство$"),
                begin_form
            )
        ],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            DOG_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_dog_name)],
            BREED: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_breed)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_weight)],
            SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_service)],
            NOTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish)],
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)

    app.run_polling()

if __name__ == "__main__":
    main()

