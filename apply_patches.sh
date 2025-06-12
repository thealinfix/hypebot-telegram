#!/bin/bash
# Скрипт для применения патчей

echo "Применение патчей к hypebot.py..."

# 1. Открываем файл в nano для ручного редактирования
echo "
ИНСТРУКЦИЯ ПО ПРИМЕНЕНИЮ ПАТЧЕЙ:

1. Откройте файл в редакторе: nano hypebot.py

2. Найдите строку 2074 (Ctrl+W, введите: gen_thought_cover)
   Замените весь блок согласно fix_thought_cover_complete.py

3. Найдите функцию publish_thought и обновите согласно патчу

4. Перед функцией main() добавьте thoughts_photo_command из add_custom_photo_function.py

5. В функции handle_photo добавьте обработку thoughts_custom_photo

6. В функции on_callback добавьте обработчик regen_thought_photo

7. В main() после thoughts_command добавьте регистрацию thoughtsphoto

8. Сохраните файл (Ctrl+X, Y, Enter)

После применения всех патчей запустите:
nohup python3 hypebot.py > ~/hypebot.log 2>&1 &
"

# Открываем файл для редактирования
nano hypebot.py
