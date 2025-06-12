# Исправление публикации мыслей с изображением

        elif data == "publish_thought" or data == "publish_thought_with_cover":
            thought_data = state.get("current_thought")
            if thought_data:
                try:
                    channel = state.get("channel", TELEGRAM_CHANNEL)
                    
                    # Проверяем какое изображение использовать
                    if thought_data.get("generated_image_url"):
                        # Сгенерированная обложка
                        await context.bot.send_photo(
                            channel,
                            thought_data["generated_image_url"],
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
                    elif thought_data.get("image_url"):
                        # Анализированное изображение
                        await context.bot.send_photo(
                            channel,
                            thought_data["image_url"],
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
