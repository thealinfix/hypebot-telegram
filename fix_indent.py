# Читаем файл и находим правильный отступ
with open('hypebot.py', 'r') as f:
    lines = f.readlines()

# Находим строку с elif data == 
for i, line in enumerate(lines):
    if 'elif data == "cmd_help":' in line:
        # Считаем пробелы
        spaces = len(line) - len(line.lstrip())
        print(f"Найдено {spaces} пробелов перед elif")
        break

# Теперь исправляем строку 2073 (индекс 2072)
if 'elif data == "gen_thought_cover":' in lines[2073]:
    lines[2073] = ' ' * spaces + 'elif data == "gen_thought_cover":\n'
    
    # Исправляем остальные строки блока
    indent_level = spaces + 4
    i = 2074
    while i < len(lines) and not (lines[i].strip().startswith('elif') or lines[i].strip().startswith('else')):
        if lines[i].strip():
            # Определяем относительный отступ
            current_indent = len(lines[i]) - len(lines[i].lstrip())
            if i == 2074:  # Первая строка после elif
                base_indent = current_indent
            relative_indent = current_indent - base_indent
            lines[i] = ' ' * (indent_level + relative_indent) + lines[i].lstrip()
        i += 1

# Сохраняем
with open('hypebot_fixed.py', 'w') as f:
    f.writelines(lines)

print("Файл исправлен и сохранен как hypebot_fixed.py")
