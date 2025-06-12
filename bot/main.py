#!/usr/bin/env python3
import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from bot.config import BOT_TOKEN, ADMIN_ID
from bot.models.state import StateManager
from bot.services.image_generator import ImageGenerator
from bot.handlers.callback import CallbackHandler
from bot.handlers.commands import CommandHandler as BotCommandHandler
from bot.handlers.messages import MessageHandler as BotMessageHandler
from bot.utils.logger import logger

class HypeBot:
    def __init__(self):
        self.state = StateManager("state.json")
        self.image_gen = ImageGenerator()
        self.callback_handler = CallbackHandler(self.state, self.image_gen)
        self.command_handler = BotCommandHandler(self.state)
        self.message_handler = BotMessageHandler(self.state)
    
    def run(self):
        """Запуск бота"""
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Регистрация обработчиков
        app.add_handler(CommandHandler("start", self.command_handler.start))
        app.add_handler(CommandHandler("help", self.command_handler.help))
        app.add_handler(CallbackQueryHandler(self.callback_handler.handle))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler.handle))
        
        # Запуск
        logger.info("Bot started")
        app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = HypeBot()
    bot.run()
