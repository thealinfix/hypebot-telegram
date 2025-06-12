# Читаем файл
with open('hypebot.py', 'r') as f:
    lines = f.readlines()

# Находим строку с cancel_thought
cancel_line = None
for i, line in enumerate(lines):
    if 'elif data == "cancel_thought":' in line:
        cancel_line = i
        break

if cancel_line:
    # Находим конец блока cancel_thought
    end_line = cancel_line + 1
    while end_line < len(lines):
        # Ищем следующий elif или else на том же уровне отступа
        if lines[end_line].strip() and not lines[end_line].startswith('    '):
            if 'elif' in lines[end_line] or 'else:' in lines[end_line]:
                break
        end_line += 1
    
    # Вставляем новый блок
    new_block = '''
        elif data == "gen_thought_cover":
            # Генерация обложки для мысли
            thought_data = state.get("current_thought")
            if thought_data and "topic" in thought_data:
                await query.edit_message_text("🎨 Генерирую обложку для мысли...")
                style_config = IMAGE_STYLES["thoughts"]
                prompt = style_config["prompt_template"].format(topic=thought_data["topic"])
                image_url = await generate_image(prompt, style_config["style"])
                if image_url:
                    thought_data["image_url"] = image_url
                    state["current_thought"] = thought_data
                    save_state()
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("📤 Опубликовать мысль", callback_data="publish_thought")],
                        [InlineKeyboardButton("🔄 Перегенерировать", callback_data="gen_thought_cover")],
                        [InlineKeyboardButton("⬅️ Назад", callback_data="create_thought")]
                    ])
                    await query.message.reply_photo(
                        photo=image_url,
                        caption=f"🎨 Обложка для мысли готова!\\n\\n"
                                f"💭 *Тема:* {thought_data['topic']}\\n"
                                f"📝 *Текст:* {thought_data['text'][:100]}...",
                        reply_markup=keyboard,
                        parse_mode="Markdown"
                    )
                else:
                    await query.edit_message_text(
                        "❌ Не удалось сгенерировать обложку. Попробуйте еще раз.",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("🔄 Попробовать снова", callback_data="gen_thought_cover")],
                            [InlineKeyboardButton("⬅️ Назад", callback_data="create_thought")]
                        ])
                    )

'''
    
    # Вставляем блок
    lines.insert(end_line, new_block)
    
    # Сохраняем
    with open('hypebot_new.py', 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Блок добавлен после строки {end_line}")
