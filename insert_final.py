with open('hypebot.py', 'r') as f:
    lines = f.readlines()

# Находим строку с elif data == "noop"
noop_line = None
for i, line in enumerate(lines):
    if 'elif data == "noop":' in line:
        noop_line = i
        break

if noop_line:
    # Вставляем перед noop
    block = '''
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
    
    lines.insert(noop_line, block)
    
    with open('hypebot.py', 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Вставлено перед строкой {noop_line} (noop)")
else:
    print("❌ Не найден блок noop")
