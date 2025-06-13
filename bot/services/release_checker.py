from typing import List, Dict
from bot.services.parsers.factory import ParserFactory
from bot.services.image_generator import ImageGenerator
from bot.services.openai_service import OpenAIService
from bot.services.publisher import Publisher
from bot.models.state import StateManager
from bot.constants import SOURCES, IMAGE_STYLES
from bot.utils.logger import logger

class ReleaseChecker:
    """Сервис проверки новых релизов"""
    
    def __init__(self, state: StateManager, image_gen: ImageGenerator, 
                 openai: OpenAIService, publisher: Publisher):
        self.state = state
        self.image_gen = image_gen
        self.openai = openai
        self.publisher = publisher
    
    async def check_all_sources(self) -> List[Dict]:
        """Проверка всех источников"""
        all_releases = []
        
        for source_key, source_config in SOURCES.items():
            logger.info(f"Checking source: {source_config['name']}")
            
            try:
                parser = ParserFactory.create(source_config)
                releases = await parser.parse()
                
                # Фильтруем уже опубликованные
                posted_ids = [p["id"] for p in self.state.get("posted", [])]
                new_releases = [r for r in releases if r["id"] not in posted_ids]
                
                all_releases.extend(new_releases)
                
            except Exception as e:
                logger.error(f"Error checking {source_config['name']}: {e}")
        
        logger.info(f"Found {len(all_releases)} new releases total")
        return all_releases
    
    async def process_releases(self, releases: List[Dict]):
        """Обработка найденных релизов"""
        pending = self.state.get("pending", {})
        
        for release in releases[:10]:  # Максимум 10 за раз
            try:
                # Генерируем улучшенное описание
                if self.openai:
                    improved = await self.openai.improve_caption(
                        release["title"], 
                        release.get("description", "")
                    )
                    if improved:
                        release["description"] = improved
                
                # Генерируем изображение
                if not release.get("image_url"):
                    style_config = IMAGE_STYLES.get(release["style"], IMAGE_STYLES["sneakers"])
                    prompt = style_config["prompt_template"].format(
                        title=release["title"],
                        brand=release.get("brand", "")
                    )
                    
                    image_url = await self.image_gen.generate(prompt, style_config["style"])
                    if image_url:
                        release["image_url"] = image_url
                        self.state.set(f"generated_images.{release['id']}", image_url)
                
                # Добавляем в очередь модерации
                pending[release["id"]] = release
                
                # Отправляем на модерацию
                await self.publisher.send_to_moderation(release)
                
            except Exception as e:
                logger.error(f"Error processing release {release.get('title')}: {e}")
        
        self.state.set("pending", pending)
