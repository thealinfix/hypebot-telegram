#!/usr/bin/env python3
"""
HypeBot - Telegram bot for @ChinaPack channel
"""

import sys
import os

# Добавляем корневую директорию в path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.main import HypeBot

if __name__ == "__main__":
    bot = HypeBot()
    bot.run()
