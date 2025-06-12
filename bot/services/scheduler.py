import asyncio
from datetime import datetime, time
from typing import List, Callable
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.config import POSTING_TIMES, TIMEZONE, CHECK_INTERVAL
from bot.utils.logger import logger

class Scheduler:
    """Планировщик задач"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=TIMEZONE)
        
    def add_check_releases_job(self, callback: Callable):
        """Добавление задачи проверки релизов"""
        self.scheduler.add_job(
            callback,
            'interval',
            minutes=CHECK_INTERVAL,
            id='check_releases',
            replace_existing=True
        )
        logger.info(f"Added check releases job every {CHECK_INTERVAL} minutes")
    
    def add_posting_jobs(self, callback: Callable):
        """Добавление задач публикации по расписанию"""
        for time_str in POSTING_TIMES:
            hour, minute = map(int, time_str.split(':'))
            
            self.scheduler.add_job(
                callback,
                CronTrigger(hour=hour, minute=minute),
                id=f'post_{time_str}',
                replace_existing=True
            )
            
        logger.info(f"Added {len(POSTING_TIMES)} posting jobs")
    
    def start(self):
        """Запуск планировщика"""
        self.scheduler.start()
        logger.info("Scheduler started")
    
    def shutdown(self):
        """Остановка планировщика"""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")
