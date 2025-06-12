# Добавление команды для кастомного фото

async def thoughts_photo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для создания поста-размышления с кастомным фото"""
    try:
        user_id = update.message.from_user.id
        if ADMIN_CHAT_ID and user_id != ADMIN_CHAT_ID:
            await update.message.reply_text("❌ Эта команда доступна только администратору")
            return
        
        if not context.args:
            await update.message.reply_text(
                "📸 Использование команды:\n"
                "/thoughtsphoto <описание>\n\n"
                "После отправки команды прикрепите фото"
            )
            return
        
        topic = " ".join(context.args)
        
        state["waiting_for_image"] = {
            "type": "thoughts_custom_photo",
            "topic": topic,
            "message_id": update.message.message_id
        }
        save_state()
        
        await update.message.reply_text("📸 Отправьте фото для поста-размышления")
        
    except Exception as e:
        logging.error(f"Ошибка в thoughts_photo_command: {e}")
        await update.message.reply_text("❌ Произошла ошибка")

# Добавьте в main():
app.add_handler(CommandHandler("thoughtsphoto", thoughts_photo_command))
