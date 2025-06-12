# Исправление превью обложки для мыслей

# В функции обработки gen_thought_cover найдите и замените:

        elif data == "gen_thought_cover":
            thought_data = state.get("current_thought")
            if thought_data:
                await query.edit_message_text("🎨 Генерирую обложку для мысли...")
                
                style_config = IMAGE_STYLES["thoughts"]
                prompt = style_config["prompt_template"].format(topic=thought_data["topic"])
                
                image_url = await generate_image(prompt, style_config["style"])
                
                if image_url:
                    # Сохраняем URL изображения
                    thought_data["generated_image_url"] = image_url
                    state["current_thought"] = thought_data
                    save_state()
                    
                    # Отправляем превью с изображением
                    try:
                        await query.message.delete()
                        
                        # Отправляем фото с текстом
                        await context.bot.send_photo(
                            chat_id=query.message.chat.id,
                            photo=image_url,
                            caption=f"💭 <b>Пост-размышление:</b>\n\n{thought_data['text']}\n\n🎨 Обложка сгенерирована!",
                            parse_mode=ParseMode.HTML,
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("📤 Опубликовать", callback_data="publish_thought_with_cover")],
                                [InlineKeyboardButton("🔄 Перегенерировать текст", callback_data="regen_thought")],
                                [InlineKeyboardButton("🎨 Новая обложка", callback_data="gen_thought_cover")],
                                [InlineKeyboardButton("❌ Отмена", callback_data="cancel_thought")]
                            ])
                        )
                    except Exception as e:
                        logging.error(f"Ошибка при отправке превью с обложкой: {e}")
                        await query.message.reply_text("❌ Ошибка при отображении превью")
                else:
                    await query.edit_message_text("❌ Ошибка при генерации обложки")
            return
