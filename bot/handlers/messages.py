from telegram import Update
from telegram.ext import ContextTypes
from bot.models.state import StateManager
from bot.services.openai_service import OpenAIService
from bot.keyboards.inline import InlineKeyboards
from bot.utils.logger import logger

class MessageHandler:
    """Обработчик текстовых сообщений"""
    
    def __init__(self, state_manager: StateManager, openai_service: OpenAIService):
        self.state = state_manager
        self.openai = openai_service
    
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        text = update.message.text
        
        # Ожидание темы для мысли
        if self.state.get("waiting_for_thought_topic"):
            await self._handle_thought_topic(update, context, text)
        
        # Редактирование мысли
        elif self.state.get("editing_thought"):
            await self._handle_thought_edit(update, context, text)
        
        # Ожидание времени для планирования
        elif self.state.get("waiting_for_schedule_time"):
            await self._handle_schedule_time(update, context, text)
    
    async def _handle_thought_topic(self, update: Update, context: ContextTypes.DEFAULT_TYPE, topic: str):
        """Обработка темы для мысли"""
        self.state.set("thought_topic", topic)
        self.state.pop("waiting_for_thought_topic")
        
        await update.message.reply_text("🤔 Генерирую мысль на эту тему...")
        
        # Генерация текста
        thought_text = await self.openai.generate_thought(topic)
        
        if thought_text:
            self.state.set("current_thought", {
                "topic": topic,
                "text": thought_text
            })
            
            keyboard = InlineKeyboards.thought_actions(has_image=False)
            
            await update.message.reply_text(
                f"💭 *Тема:* {topic}\n\n"
                f"*Текст:*\n{thought_text}",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("❌ Не удалось сгенерировать мысль")
