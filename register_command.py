# В функции main() найдите строку где регистрируются команды
# (app.add_handler(CommandHandler("thoughts", thoughts_command)))
# И добавьте после нее:

app.add_handler(CommandHandler("thoughtsphoto", thoughts_photo_command))
