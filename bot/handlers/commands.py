from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.models.state import StateManager
from bot.config import ADMIN_ID
from bot.utils.logger import logger

class CommandHandler:
    """Обработчик команд бота"""
    
    def __init__(self, state_manager: StateManager):
        self.state = state_manager
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ Бот доступен только администратору")
            return
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 Помощь", callback_data="cmd_help")],
            [InlineKeyboardButton("👀 Превью постов", callback_data="cmd_preview")],
            [InlineKeyboardButton("🔍 Проверить релизы", callback_data="cmd_check")],
            [InlineKeyboardButton("💭 Мысли", callback_data="cmd_thoughts")],
            [InlineKeyboardButton("📅 Расписание", callback_data="cmd_scheduled")]
        ])
        
        await update.message.reply_text(
            "🚀 *HypeBot Admin Panel*\n\n"
            "Выберите действие:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        
        logger.info(f"Start command from user {user_id}")
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /help или callback cmd_help"""
        help_text = """
📋 *Команды бота:*

/start - Главное меню
/help - Эта справка
/preview - Просмотр отложенных постов
/check - Проверить новые релизы
/thoughts - Управление мыслями
/scheduled - Просмотр расписания

💭 *Работа с мыслями:*
1. Нажмите "Мысли" → "Создать"
2. Введите тему для размышления
3. Бот сгенерирует текст
4. Можете создать обложку
5. Опубликуйте в канал

🔍 *Модерация:*
- Бот автоматически проверяет источники
- Отправляет посты на модерацию
- Вы решаете что публиковать

⚙️ *Настройки:*
- Канал: {channel}
- Проверка каждые: {interval} мин
- Timezone: {tz}
        """.format(
            channel=self.state.get("channel", "@ChinaPack"),
            interval=self.state.get("check_interval", 30),
            tz=self.state.get("timezone", "Europe/Moscow")
        )
        
        if hasattr(update, "callback_query"):
            await update.callback_query.edit_message_text(
                help_text,
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                help_text,
                parse_mode="Markdown"
            )
