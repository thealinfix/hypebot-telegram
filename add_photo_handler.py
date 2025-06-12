# В функции handle_photo (примерно строка 1580) добавьте после блока if waiting_data["type"] == "thoughts":

        elif waiting_data["type"] == "thoughts_custom_photo":
            # Мысли с кастомным фото
            await msg.edit_text("💭 Генерирую текст для вашего фото...")
            
            photo_file_id = update.message.photo[-1].file_id
            
            thought_text = await gen_caption(
                waiting_data["topic"], 
                "", 
                "sneakers", 
                is_thought=True
            )
            
            hashtags = get_hashtags(waiting_data["topic"], "sneakers")
            final_text = f"{thought_text}\n\n{hashtags}"
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📤 Опубликовать", callback_data="publish_thought")],
                [InlineKeyboardButton("🔄 Перегенерировать", callback_data="regen_thought_photo")],
                [InlineKeyboardButton("❌ Отмена", callback_data="cancel_thought")]
            ])
            
            state["current_thought"] = {
                "text": final_text,
                "topic": waiting_data["topic"],
                "custom_photo": photo_file_id
            }
            save_state()
            
            # Удаляем сообщение "Генерирую..."
            await msg.delete()
            
            # Отправляем превью с фото
            await context.bot.send_photo(
                update.message.chat.id,
                photo=photo_file_id,
                caption=f"💭 <b>Пост-размышление с вашим фото:</b>\n\n{final_text}",
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
            )
