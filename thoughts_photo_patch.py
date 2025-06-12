# Патч для добавления кастомных фото в мысли

# Найдите функцию handle_photo и добавьте после waiting_data["type"] == "thoughts":
        
        # Для мыслей с кастомным фото
        elif waiting_data["type"] == "thoughts_custom_photo":
            # Сохраняем фото
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
                [InlineKeyboardButton("🔄 Перегенерировать", callback_data="regen_thought")],
                [InlineKeyboardButton("❌ Отмена", callback_data="cancel_thought")]
            ])
            
            state["current_thought"] = {
                "text": final_text,
                "topic": waiting_data["topic"],
                "custom_photo": photo_file_id
            }
            save_state()
            
            await msg.edit_text(
                f"💭 <b>Пост-размышление с вашим фото:</b>\n\n{final_text}",
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
            )
