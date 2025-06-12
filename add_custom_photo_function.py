# Добавьте эту функцию перед функцией main() (примерно строка 2900):

async def thoughts_photo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для создания поста-размышления с кастомным фото"""
    try:
        user_id = update.message.from_user.id
        if ADMIN_CHAT_ID and user_id != ADMIN_CHAT_ID:
            await update.message.reply_text("❌ Эта команда доступна только администратору")
            return
        
        if not context.args:
            await update.message.reply_text(
                "📸 <b>Создание мысли с фото</b>\n\n"
                "Использование:\n"
                "<code>/thoughtsphoto тема поста</code>\n\n"
                "Пример:\n"
                "<code>/thoughtsphoto новые Jordan 4 в черном цвете</code>\n\n"
                "После команды отправьте фото",
                parse_mode=ParseMode.HTML
            )
            return
        
        topic = " ".join(context.args)
        
        state["waiting_for_image"] = {
            "type": "thoughts_custom_photo",
            "topic": topic,
            "message_id": update.message.message_id
        }
        save_state()
        
        await update.message.reply_text("📸 Теперь отправьте фото для поста-размышления")
        
    except Exception as e:
        logging.error(f"Ошибка в thoughts_photo_command: {e}")
        await update.message.reply_text("❌ Произошла ошибка")
