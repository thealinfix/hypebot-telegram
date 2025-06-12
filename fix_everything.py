with open('hypebot.py', 'r') as f:
   lines = f.readlines()

# Находим строку с noop
noop_line = None
for i, line in enumerate(lines):
   if 'elif data == "noop":' in line and 'cancel_thought' in ''.join(lines[max(0,i-10):i]):
       noop_line = i
       break

if noop_line:
   # Вставляем ПЕРЕД noop
   new_block = '''        elif data == "gen_thought_cover":
           # Генерация обложки для мысли
           thought_data = state.get("current_thought")
           if not thought_data:
               await query.answer("❌ Данные мысли не найдены")
               return
           
           if "topic" not in thought_data:
               await query.answer("❌ Тема мысли не указана")
               return
           
           await query.edit_message_text("🎨 Генерирую обложку для мысли...")
           
           try:
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
                   await query.message.delete()
               else:
                   await query.edit_message_text(
                       "❌ Не удалось сгенерировать обложку. Попробуйте еще раз.",
                       reply_markup=InlineKeyboardMarkup([
                           [InlineKeyboardButton("🔄 Попробовать снова", callback_data="gen_thought_cover")],
                           [InlineKeyboardButton("⬅️ Назад", callback_data="create_thought")]
                       ])
                   )
           except Exception as e:
               logger.error(f"Ошибка при генерации обложки: {e}")
               await query.edit_message_text(
                   "❌ Произошла ошибка при генерации обложки.",
                   reply_markup=InlineKeyboardMarkup([
                       [InlineKeyboardButton("⬅️ Назад", callback_data="create_thought")]
                   ])
               )

'''
   
   # Вставляем блок
   lines.insert(noop_line, new_block)
   
   # Сохраняем
   with open('hypebot_fixed.py', 'w') as f:
       f.writelines(lines)
   
   print(f"✅ Файл сохранен как hypebot_fixed.py")
   print(f"Блок вставлен перед строкой {noop_line}")
else:
   print("❌ Не найден блок noop после cancel_thought")
