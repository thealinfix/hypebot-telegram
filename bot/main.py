#!/usr/bin/env python3
import asyncio
import signal
import sys
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from bot.config import BOT_TOKEN, ADMIN_ID
from bot.models.state import StateManager
from bot.services.image_generator import ImageGenerator
from bot.services.openai_service import OpenAIService
from bot.services.scheduler import Scheduler
from bot.handlers.callback import CallbackHandler
from bot.handlers.commands import CommandHandler as BotCommandHandler
from bot.handlers.messages import MessageHandler as BotMessageHandler
from bot.utils.logger import logger

class HypeBot:
    def __init__(self):
        # Инициализация сервисов
        self.state = StateManager("state.json")
        self.image_gen = ImageGenerator()
        self.openai = OpenAIService()
        self.scheduler = Scheduler()
        
        # Инициализация обработчиков
        self.callback_handler = CallbackHandler(self.state, self.image_gen, self.openai)
        self.command_handler = BotCommandHandler(self.state)
        self.message_handler = BotMessageHandler(self.state, self.openai)
        
        # Приложение Telegram
        self.app = None
    
    async def check_releases(self):
        """Проверка новых релизов"""
        logger.info("Checking for new releases...")
        # TODO: Implement release checking
    
    async def post_scheduled(self):
        """Публикация по расписанию"""
        logger.info("Posting scheduled content...")
        # TODO: Implement scheduled posting
    
    def setup_handlers(self):
        """Настройка обработчиков"""
        # Команды
        self.app.add_handler(CommandHandler("start", self.command_handler.start))
        self.app.add_handler(CommandHandler("help", self.command_handler.help))
        
        # Callback queries
        self.app.add_handler(CallbackQueryHandler(self.callback_handler.handle))
        
        # Сообщения
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_ID),
            self.message_handler.handle
        ))
    
    def setup_jobs(self):
        """Настройка задач планировщика"""
        self.scheduler.add_check_releases_job(self.check_releases)
        self.scheduler.add_posting_jobs(self.post_scheduled)
        self.scheduler.start()
    
    async def startup(self):
        """Действия при запуске"""
        logger.info("=== HypeBot Starting ===")
        logger.info(f"Admin ID: {ADMIN_ID}")
        logger.info(f"State file: {self.state.state_file}")
        
        # Запускаем планировщик
        self.setup_jobs()
    
    async def shutdown(self):
        """Действия при остановке"""
        logger.info("=== HypeBot Stopping ===")
        self.scheduler.shutdown()
        self.state.save()
    
    def run(self):
        """Запуск бота"""
        # Создаем приложение
        self.app = Application.builder().token(BOT_TOKEN).build()
        
        # Настраиваем обработчики
        self.setup_handlers()
        
        # Добавляем startup/shutdown
        self.app.post_init = self.startup
        self.app.post_shutdown = self.shutdown
        
        # Обработка сигналов
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, lambda s, f: asyncio.create_task(self.shutdown()))
        
        # Запуск
        logger.info("Bot started. Press Ctrl+C to stop.")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = HypeBot()
    bot.run()
