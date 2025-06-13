from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict, Optional
from datetime import datetime
from bot.config import CHANNEL_USERNAME, ADMIN_ID
from bot.models.state import StateManager
from bot.utils.logger import logger

class Publisher:
    """Сервис публикации контента"""
    
    def __init__(self, bot: Bot, state_manager: StateManager):
        self.bot = bot
        self.state = state_manager
    
    async def publish_release(self, release: Dict) -> bool:
        """Публикация релиза в канал"""
        try:
            caption = self._format_release_caption(release)
            
            if release.get("image_url"):
                # Публикация с изображением
                await self.bot.send_photo(
                    chat_id=CHANNEL_USERNAME,
                    photo=release["image_url"],
                    caption=caption,
                    parse_mode="HTML"
                )
            else:
                # Публикация только текста
                await self.bot.send_message(
                    chat_id=CHANNEL_USERNAME,
                    text=caption,
                    parse_mode="HTML"
                )
            
            # Добавляем в опубликованные
            posted = self.state.get("posted", [])
            posted.append({
                "id": release["id"],
                "title": release["title"],
                "timestamp": datetime.now().isoformat()
            })
            self.state.set("posted", posted[-100:])  # Храним последние 100
            
            logger.info(f"Published: {release['title']}")
            return True
            
        except Exception as e:
            logger.error(f"Error publishing release: {e}")
            return False
    
    async def send_to_moderation(self, release: Dict):
        """Отправка на модерацию админу"""
        try:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Опубликовать", callback_data=f"approve:{release['id']}")],
                [InlineKeyboardButton("🎨 Новая обложка", callback_data=f"regen:{release['id']}")],
                [InlineKeyboardButton("❌ Пропустить", callback_data=f"reject:{release['id']}")]
            ])
            
            caption = f"🔍 *Новый релиз для модерации*\n\n{self._format_release_caption(release)}"
            
            if release.get("image_url"):
                await self.bot.send_photo(
                    chat_id=ADMIN_ID,
                    photo=release["image_url"],
                    caption=caption,
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
            else:
                await self.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=caption,
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
                
        except Exception as e:
            logger.error(f"Error sending to moderation: {e}")
    
    def _format_release_caption(self, release: Dict) -> str:
        """Форматирование описания релиза"""
        caption = f"🔥 <b>{release['title']}</b>\n\n"
        
        if release.get("description"):
            caption += f"{release['description']}\n\n"
        
        if release.get("date"):
            caption += f"📅 Дата релиза: {release['date']}\n"
        
        if release.get("price"):
            caption += f"💰 Цена: {release['price']}\n"
        
        caption += f"\n🔗 <a href='{release['link']}'>Подробнее</a>"
        caption += f"\n\n#releases #{release.get('brand', '').lower().replace(' ', '')}"
        
        return caption
