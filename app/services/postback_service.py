"""Сервис обработки постбеков (БЕЗ веб-сервера)."""

import json
import os
from datetime import datetime


class PostbackService:
    """Обработка постбеков от партнеров."""
    
    def __init__(self):
        """Инициализировать сервис."""
        self.postbacks = []
        self.load_postbacks()
    
    def load_postbacks(self):
        """Загрузить постбеки."""
        try:
            if os.path.exists("postbacks.json"):
                with open("postbacks.json", "r") as f:
                    self.postbacks = json.load(f)
        except Exception as e:
            print(f"❌ Ошибка загрузки постбеков: {e}")
    
    def save_postbacks(self):
        """Сохранить постбеки."""
        try:
            with open("postbacks.json", "w") as f:
                json.dump(self.postbacks, f, indent=2)
        except Exception as e:
            print(f"❌ Ошибка сохранения постбеков: {e}")
    
    def add_postback(self, user_id: int, partner: str, amount: float, status: str):
        """Добавить постбек."""
        postback = {
            "user_id": user_id,
            "partner": partner,
            "amount": amount,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        self.postbacks.append(postback)
        self.save_postbacks()
        print(f"✅ Постбек добавлен: {user_id} - {partner} - {amount}")
    
    def get_user_postbacks(self, user_id: int) -> list:
        """Получить постбеки пользователя."""
        return [p for p in self.postbacks if p["user_id"] == user_id]
    
    def get_total_earnings(self, user_id: int) -> float:
        """Получить общий заработок пользователя."""
        user_postbacks = self.get_user_postbacks(user_id)
        return sum(p["amount"] for p in user_postbacks if p["status"] == "completed")
