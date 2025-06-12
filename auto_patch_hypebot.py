#!/usr/bin/env python3
import re
import sys

# Читаем файл
with open('hypebot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Патч для gen_thought_cover
gen_thought_cover_patch = '''        elif data == "gen_thought_cover":
            # Генерация обложки для мысли
            thought_data = state.get("current_thought")
            if thought_data:
                await query.edit_message_text("🎨 Генерирую обложку для мысли...")
                
                style_config = IMAGE_STYLES["thoughts"]
                prompt = style_config["prompt_template"].format(topic=thought_data["topic"])
                
                image_url = await generate_image(prompt, style_config["style"])
                
                if image_url:
                    thought_data["image_url"] = image_url
                    state["current_thought"] = thought_data
                    save_state()
                    
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("📤 Опубликовать", callback_data="publish_thought")],
                        [InlineKeyboardButton("🔄 Перегенерировать текст", callback_data="regen_thought")],
                        [InlineKeyboardButton("🎨 Новая обложка", callback_data="gen_thought_cover")],
                        [InlineKeyboardButton("❌ Отмена", callback_data="cancel_thought")]
                    ])
                    
                    # Удаляем старое сообщение
                    await query.message.delete()
                    
                    # Отправляем новое с фото
                    await context.bot.send_photo(
                        query.message.chat.id,
                        photo=image_url,
                        caption=f"💭 <b>Пост-размышление:</b>\\n\\n{thought_data['text']}\\n\\n🎨 Обложка сгенерирована!",
                        parse_mode=ParseMode.HTML,
                        reply_markup=keyboard
                    )
                else:
                    await query.edit_message_text("❌ Ошибка при генерации обложки")
            return'''

# Находим и заменяем блок gen_thought_cover
pattern = r'elif data == "gen_thought_cover":\s*\n(?:.*\n)*?.*?return'
content = re.sub(pattern, gen_thought_cover_patch, content, flags=re.MULTILINE | re.DOTALL)

# 2. Добавляем функцию thoughts_photo_command перед main()
thoughts_photo_func = '''
async def thoughts_photo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для создания поста-размышления с кастомным фото"""
    try:
        user_id = update.message.from_user.id
        if ADMIN_CHAT_ID and user_id != ADMIN_CHAT_ID:
            await update.message.reply_text("❌ Эта команда доступна только администратору")
            return
        
        if not context.args:
            await update.message.reply_text(
                "📸 <b>Создание мысли с фото</b>\\n\\n"
                "Использование:\\n"
                "<code>/thoughtsphoto тема поста</code>\\n\\n"
                "Пример:\\n"
                "<code>/thoughtsphoto новые Jordan 4 в черном цвете</code>\\n\\n"
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

'''

# Добавляем функцию перед main()
main_pattern = r'(def main\(\) -> None:)'
content = re.sub(main_pattern, thoughts_photo_func + r'\1', content)

# 3. Добавляем регистрацию команды thoughtsphoto
command_pattern = r'(app\.add_handler\(CommandHandler\("thoughts", thoughts_command\)\))'
content = re.sub(command_pattern, r'\1\n    app.add_handler(CommandHandler("thoughtsphoto", thoughts_photo_command))', content)

# Сохраняем изменения
with open('hypebot_patched.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Патч успешно применен! Файл сохранен как hypebot_patched.py")
