#!/usr/bin/env python3
# Патч для исправления отображения обложки в мыслях

# 1. Найдите в файле строку 2074 (elif data == "gen_thought_cover":)
# И замените весь блок до следующего elif/else на:

        elif data == "gen_thought_cover":
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
                        caption=f"💭 <b>Пост-размышление:</b>\n\n{thought_data['text']}\n\n🎨 Обложка сгенерирована!",
                        parse_mode=ParseMode.HTML,
                        reply_markup=keyboard
                    )
                else:
                    await query.edit_message_text("❌ Ошибка при генерации обложки")
            return

# 2. Исправьте функцию publish_thought (найдите elif data == "publish_thought":)
# Замените на:

        elif data == "publish_thought":
            # Публикация мысли
            thought_data = state.get("current_thought")
            if thought_data:
                try:
                    channel = state.get("channel", TELEGRAM_CHANNEL)
                    
                    # Проверяем есть ли изображение
                    if thought_data.get("image_url"):
                        # Сгенерированная обложка
                        await context.bot.send_photo(
                            channel,
                            thought_data["image_url"],
                            caption=thought_data["text"],
                            parse_mode=ParseMode.HTML
                        )
                    elif thought_data.get("custom_photo"):
                        # Кастомное фото
                        await context.bot.send_photo(
                            channel,
                            thought_data["custom_photo"],
                            caption=thought_data["text"],
                            parse_mode=ParseMode.HTML
                        )
                    else:
                        # Только текст
                        await context.bot.send_message(
                            channel,
                            thought_data["text"],
                            parse_mode=ParseMode.HTML
                        )
                    
                    await query.edit_message_text("✅ Мысли опубликованы!")
                    state.pop("current_thought", None)
                    save_state()
                except Exception as e:
                    await query.edit_message_text(f"❌ Ошибка публикации: {e}")
            return
