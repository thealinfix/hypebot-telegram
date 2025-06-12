# В функции on_callback добавьте обработчик для regen_thought_photo:

        elif data == "regen_thought_photo":
            # Перегенерация текста для фото
            thought_data = state.get("current_thought")
            if thought_data and thought_data.get("custom_photo"):
                await query.edit_message_caption("🔄 Генерирую новый текст...")
                
                new_thought = await gen_caption(
                    thought_data["topic"], 
                    "", 
                    "sneakers", 
                    is_thought=True
                )
                hashtags = get_hashtags(thought_data["topic"], "sneakers")
                final_text = f"{new_thought}\n\n{hashtags}"
                
                thought_data["text"] = final_text
                state["current_thought"] = thought_data
                save_state()
                
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("📤 Опубликовать", callback_data="publish_thought")],
                    [InlineKeyboardButton("🔄 Перегенерировать", callback_data="regen_thought_photo")],
                    [InlineKeyboardButton("❌ Отмена", callback_data="cancel_thought")]
                ])
                
                await query.edit_message_caption(
                    caption=f"💭 <b>Пост-размышление с вашим фото:</b>\n\n{final_text}",
                    parse_mode=ParseMode.HTML,
                    reply_markup=keyboard
                )
            return
