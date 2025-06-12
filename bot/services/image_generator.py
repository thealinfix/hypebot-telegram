import aiohttp
import asyncio
from typing import Optional
from bot.config import IMAGE_API_URL, IMAGE_API_KEY
from bot.utils.logger import logger

class ImageGenerator:
    def __init__(self):
        self.api_url = IMAGE_API_URL
        self.api_key = IMAGE_API_KEY
    
    async def generate(self, prompt: str, style: str) -> Optional[str]:
        """Генерация изображения через API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "prompt": prompt,
                "aspect_ratio": "1:1",
                "mode": "fast",
                "model": "v6"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/imagine",
                    json=data,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        task_id = result.get("taskId")
                        
                        if task_id:
                            return await self._wait_for_result(task_id)
                    else:
                        logger.error(f"API error: {response.status}")
                        
        except Exception as e:
            logger.error(f"Image generation error: {e}")
            
        return None
    
    async def _wait_for_result(self, task_id: str) -> Optional[str]:
        """Ожидание результата генерации"""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        for _ in range(60):  # Максимум 5 минут
            await asyncio.sleep(5)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/task/{task_id}",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("status") == "completed":
                            return result.get("imageUrl")
                        elif result.get("status") == "failed":
                            logger.error("Image generation failed")
                            return None
        
        logger.error("Image generation timeout")
        return None
