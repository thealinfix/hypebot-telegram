#!/usr/bin/env python3
import asyncio
import signal
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from bot.config import BOT_TOKEN, ADMIN_ID
from bot.models.state import StateManager
from bot.services.image_generator import ImageGenerator
from bot.services.openai_service import OpenAIService
from bot.services.scheduler import Scheduler
from bot.services.publisher import Publisher
from bot.services.release_checker import ReleaseChecker
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
        self.publisher = None  # Инициализируется после создания bot
        self.release_checker = None
        
        # Обработчики
        self.callback_handler = None
        self.command_handler = None
        self.message_handler = None
        
        # Приложение Telegram
        self.app = None
    
    async def check_releases(self):
        """Проверка новых релизов"""
        try:
            logger.info("Checking for new releases...")
            releases = await self.release_checker.check_all_sources()
            
            if releases:
                await self.release_checker.process_releases(releases)
            else:
                logger.info("No new releases found")
                
        except Exception as e:
            logger.error(f"Error in check_releases: {e}")
    
    async def post_scheduled(self):
        """Публикация по расписанию"""
        try:
            scheduled = self.state.get("scheduled_posts", [])
            
            if scheduled:
                post = scheduled.pop(0)
                self.state.set("scheduled_posts", scheduled)
                
                success = await self.publisher.publish_release(post)
                if success:
                    logger.info(f"Posted scheduled: {post['title']}")
                else:
                    # Возвращаем обратно в очередь
                    scheduled.insert(0, post)
                    self.state.set("scheduled_posts", scheduled)
            else:
                logger.info("No scheduled posts")
                
        except Exception as e:
            logger.error(f"Error in post_scheduled: {e}")
    
    def setup_handlers(self):
        """Настройка обработчиков"""
        # Инициализация сервисов, требующих bot
        self.publisher = Publisher(self.app.bot, self.state)
        self.release_checker = ReleaseChecker(
            self.state, self.image_gen, self.openai, self.publisher
        )
        
        # Инициализация обработчиков
        self.callback_handler = CallbackHandler(
            self.state, self.image_gen, self.openai, self.publisher
        )
        self.command_handler = BotCommandHandler(self.state)
        self.message_handler = BotMessageHandler(self.state, self.openai)
        
        # Регистрация обработчиков
        self.app.add_handler(CommandHandler("start", self.command_handler.start))
        self.app.add_handler(CommandHandler("help", self.command_handler.help))
        self.app.add_handler(CommandHandler("preview", self.command_handler.preview))
        self.app.add_handler(CommandHandler("check", self.command_handler.check))
        self.app.add_handler(CommandHandler("thoughts", self.command_handler.thoughts))
        self.app.add_handler(CommandHandler("scheduled", self.command_handler.scheduled))
        
        # Callback queries
        self.app.add_handler(CallbackQueryHandler(self.callback_handler.handle))
        
        # Сообщения
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_ID),
            self.message_handler.handle
        ))
    
    def setup_jobs(self):
        """Настройка задач планировщика"""
        self.scheduler.add_check_releases_job(
            lambda: asyncio.create_task(self.check_releases())
        )
        self.scheduler.add_posting_jobs(
            lambda: asyncio.create_task(self.post_scheduled())
        )
        self.scheduler.start()
    
    async def startup(self):
        """Действия при запуске"""
        logger.info("=== HypeBot Starting ===")
        logger.info(f"Admin ID: {ADMIN_ID}")
        logger.info(f"Channel: {CHANNEL_USERNAME}")
        
        # Запускаем планировщик
        self.setup_jobs()
        
        # Первая проверка через 10 секунд
        asyncio.create_task(asyncio.sleep(10)).add_done_callback(
            lambda _: asyncio.create_task(self.check_releases())
        )
    
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
