import openai
from typing import Optional, List
from bot.config import OPENAI_API_KEY, OPENAI_MODEL
from bot.utils.logger import logger

class OpenAIService:
    """Сервис для работы с OpenAI API"""
    
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.model = OPENAI_MODEL
    
    async def generate_thought(self, topic: str) -> Optional[str]:
        """Генерация мысли на заданную тему"""
        try:
            prompt = f"""Напиши короткое философское размышление на тему "{topic}" для канала о моде и стритвире.
            Требования:
            - Максимум 3-4 предложения
            - Глубокая мысль, но понятным языком
            - Связь с модой/стилем/культурой
            - Без банальностей и клише
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты философ моды и уличной культуры."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating thought: {e}")
            return None
    
    async def improve_caption(self, title: str, description: str = "") -> Optional[str]:
        """Улучшение описания для поста"""
        try:
            prompt = f"""Улучши описание для поста о релизе: "{title}"
            {f'Оригинальное описание: {description}' if description else ''}
            
            Требования:
            - Короткое и емкое (2-3 предложения)
            - Хайповое, но информативное
            - Добавь релевантные эмодзи
            - На русском языке
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты редактор хайпового канала о моде."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error improving caption: {e}")
            return None
