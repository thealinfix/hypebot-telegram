from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.models.state import StateManager
from bot.services.image_generator import ImageGenerator
from bot.config import CHANNEL_USERNAME
from bot.constants import IMAGE_STYLES
from bot.utils.logger import logger

class CallbackHandler:
    def __init__(self, state_manager: StateManager, image_generator: ImageGenerator):
        self.state = state_manager
        self.image_gen = image_generator
    
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Главный обработчик callback запросов"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        # Роутинг по типам callback
        if data.startswith("cmd_"):
            await self._handle_command(query, context, data)
        elif data in ["create_thought", "cancel_thought", "gen_thought_cover", "publish_thought"]:
            await self._handle_thought(query, context, data)
        elif ":" in data:
            await self._handle_moderation(query, context, data)
        elif data == "noop":
            return
        else:
            await query.edit_message_text("❌ Неизвестная команда")
    
    async def _handle_thought(self, query, context, data):
        """Обработка действий с мыслями"""
        if data == "gen_thought_cover":
            await self._generate_thought_cover(query, context)
        elif data == "publish_thought":
            await self._publish_thought(query, context)
        elif data == "cancel_thought":
            await self._cancel_thought(query)
        # ... другие обработчики
    
    async def _generate_thought_cover(self, query, context):
        """Генерация обложки для мысли"""
        thought_data = self.state.get("current_thought")
        
        if not thought_data or "topic" not in thought_data:
            await query.answer("❌ Данные мысли не найдены")
            return
        
        await query.edit_message_text("🎨 Генерирую обложку для мысли...")
        
        try:
            style_config = IMAGE_STYLES["thoughts"]
            prompt = style_config["prompt_template"].format(topic=thought_data["topic"])
            image_url = await self.image_gen.generate(prompt, style_config["style"])
            
            if image_url:
                thought_data["image_url"] = image_url
                self.state.set("current_thought", thought_data)
                
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("📤 Опубликовать", callback_data="publish_thought")],
                    [InlineKeyboardButton("🔄 Перегенерировать", callback_data="gen_thought_cover")],
                    [InlineKeyboardButton("⬅️ Назад", callback_data="create_thought")]
                ])
                
                await query.message.reply_photo(
                    photo=image_url,
                    caption=f"🎨 Обложка готова!\n\n"
                           f"💭 *{thought_data['topic']}*\n"
                           f"📝 {thought_data['text'][:100]}...",
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
                await query.message.delete()
            else:
                await query.edit_message_text(
                    "❌ Не удалось сгенерировать обложку",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🔄 Повторить", callback_data="gen_thought_cover"),
                        InlineKeyboardButton("⬅️ Назад", callback_data="create_thought")
                    ]])
                )
        except Exception as e:
            logger.error(f"Error generating thought cover: {e}")
            await query.answer("❌ Ошибка генерации")
