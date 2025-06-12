from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Dict

class InlineKeyboards:
    """Фабрика inline клавиатур"""
    
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        """Главное меню"""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 Помощь", callback_data="cmd_help")],
            [InlineKeyboardButton("👀 Превью", callback_data="cmd_preview")],
            [InlineKeyboardButton("🔍 Проверить релизы", callback_data="cmd_check")],
            [InlineKeyboardButton("💭 Мысли", callback_data="cmd_thoughts")],
            [InlineKeyboardButton("📅 Расписание", callback_data="cmd_scheduled")]
        ])
    
    @staticmethod
    def thoughts_menu() -> InlineKeyboardMarkup:
        """Меню работы с мыслями"""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("✍️ Создать мысль", callback_data="create_thought")],
            [InlineKeyboardButton("📝 Мои черновики", callback_data="draft_thoughts")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")]
        ])
    
    @staticmethod
    def thought_actions(has_image: bool = False) -> InlineKeyboardMarkup:
        """Действия с мыслью"""
        buttons = []
        
        if has_image:
            buttons.append([
                InlineKeyboardButton("📤 Опубликовать", callback_data="publish_thought")
            ])
            buttons.append([
                InlineKeyboardButton("🔄 Новая обложка", callback_data="gen_thought_cover")
            ])
        else:
            buttons.append([
                InlineKeyboardButton("🎨 Создать обложку", callback_data="gen_thought_cover")
            ])
        
        buttons.append([
            InlineKeyboardButton("📝 Редактировать", callback_data="edit_thought")
        ])
        buttons.append([
            InlineKeyboardButton("❌ Отмена", callback_data="cancel_thought")
        ])
        
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def moderation(uid: str) -> InlineKeyboardMarkup:
        """Клавиатура модерации"""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Опубликовать", callback_data=f"approve:{uid}")],
            [InlineKeyboardButton("🎨 Новая обложка", callback_data=f"regen:{uid}")],
            [InlineKeyboardButton("❌ Пропустить", callback_data=f"reject:{uid}")]
        ])
