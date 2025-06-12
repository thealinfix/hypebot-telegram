with open('hypebot.py', 'r') as f:
    content = f.read()

# Проверяем, есть ли уже правильный обработчик
if 'elif data == "gen_thought_cover":' in content and 'thought_data = state.get("current_thought")' in content:
    print("✅ Обработчик gen_thought_cover уже существует!")
    exit(0)

# Находим место для вставки - перед cancel_thought
import re
pattern = r'(\s+)(elif data == "cancel_thought":)'
match = re.search(pattern, content)

if match:
    indent = match.group(1)
    
    # Готовим новый блок с правильными отступами
    new_block = f'''
{indent}elif data == "gen_thought_cover":
{indent}    # Генерация обложки для мысли
{indent}    thought_data = state.get("current_thought")
{indent}    if not thought_data:
{indent}        await query.answer("❌ Данные мысли не найдены")
{indent}        return
{indent}    
{indent}    if "topic" not in thought_data:
{indent}        await query.answer("❌ Тема мысли не указана")
{indent}        return
{indent}    
{indent}    await query.edit_message_text("🎨 Генерирую обложку для мысли...")
{indent}    
{indent}    try:
{indent}        style_config = IMAGE_STYLES["thoughts"]
{indent}        prompt = style_config["prompt_template"].format(topic=thought_data["topic"])
{indent}        image_url = await generate_image(prompt, style_config["style"])
{indent}        
{indent}        if image_url:
{indent}            thought_data["image_url"] = image_url
{indent}            state["current_thought"] = thought_data
{indent}            save_state()
{indent}            
{indent}            keyboard = InlineKeyboardMarkup([
{indent}                [InlineKeyboardButton("📤 Опубликовать мысль", callback_data="publish_thought")],
{indent}                [InlineKeyboardButton("🔄 Перегенерировать", callback_data="gen_thought_cover")],
{indent}                [InlineKeyboardButton("⬅️ Назад", callback_data="create_thought")]
{indent}            ])
{indent}            
{indent}            await query.message.reply_photo(
{indent}                photo=image_url,
{indent}                caption=f"🎨 Обложка для мысли готова!\\n\\n"
{indent}                        f"💭 *Тема:* {{thought_data['topic']}}\\n"
{indent}                        f"📝 *Текст:* {{thought_data['text'][:100]}}...",
{indent}                reply_markup=keyboard,
{indent}                parse_mode="Markdown"
{indent}            )
{indent}            await query.message.delete()
{indent}        else:
{indent}            await query.edit_message_text(
{indent}                "❌ Не удалось сгенерировать обложку.",
{indent}                reply_markup=InlineKeyboardMarkup([
{indent}                    [InlineKeyboardButton("🔄 Попробовать снова", callback_data="gen_thought_cover")],
{indent}                    [InlineKeyboardButton("⬅️ Назад", callback_data="create_thought")]
{indent}                ])
{indent}            )
{indent}    except Exception as e:
{indent}        logger.error(f"Ошибка при генерации обложки: {{e}}")
{indent}        await query.edit_message_text(
{indent}            "❌ Произошла ошибка при генерации.",
{indent}            reply_markup=InlineKeyboardMarkup([
{indent}                [InlineKeyboardButton("⬅️ Назад", callback_data="create_thought")]
{indent}            ])
{indent}        )

{indent}'''
    
    # Вставляем перед cancel_thought
    new_content = content.replace(match.group(0), new_block + match.group(0))
    
    # Сохраняем
    with open('hypebot.py', 'w') as f:
        f.write(new_content)
    
    print("✅ Обработчик gen_thought_cover успешно добавлен!")
else:
    print("❌ Не найден блок cancel_thought")
