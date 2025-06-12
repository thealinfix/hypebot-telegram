import json
import os
from datetime import datetime
from typing import Dict, Any

class StateManager:
    def __init__(self, state_file: str):
        self.state_file = state_file
        self.state = self.load_state()
    
    def load_state(self) -> Dict[str, Any]:
        """Загрузка состояния из файла"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "posted": [],
            "pending": {},
            "generated_images": {},
            "current_thought": None,
            "scheduled_posts": []
        }
    
    def save(self):
        """Сохранение состояния в файл"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
    
    def get(self, key: str, default=None):
        return self.state.get(key, default)
    
    def set(self, key: str, value: Any):
        self.state[key] = value
        self.save()
    
    def pop(self, key: str, default=None):
        value = self.state.pop(key, default)
        self.save()
        return value
