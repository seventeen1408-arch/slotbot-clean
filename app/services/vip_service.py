"""Сервис VIP подписки."""

import json
import os
from datetime import datetime, timedelta


class VIPService:
    """Управление VIP подписками."""
    
    def __init__(self):
        """Инициализировать сервис."""
        self.vip_users = {}
        self.load_vip_users()
    
    def load_vip_users(self):
        """Загрузить VIP пользователей."""
        try:
            if os.path.exists("vip_users.json"):
                with open("vip_users.json", "r") as f:
                    self.vip_users = json.load(f)
        except Exception as e:
            print(f"❌ Ошибка загрузки VIP: {e}")
    
    def save_vip_users(self):
        """Сохранить VIP пользователей."""
        try:
            with open("vip_users.json", "w") as f:
                json.dump(self.vip_users, f)
        except Exception as e:
            print(f"❌ Ошибка сохранения VIP: {e}")
    
    def add_vip(self, user_id: int, days: int = 30):
        """Добавить VIP подписку."""
        expiry = (datetime.now() + timedelta(days=days)).isoformat()
        self.vip_users[str(user_id)] = {
            "expiry": expiry,
            "created": datetime.now().isoformat()
        }
        self.save_vip_users()
        print(f"✅ VIP добавлен пользователю {user_id}")
    
    def is_vip(self, user_id: int) -> bool:
        """Проверить VIP статус."""
        if str(user_id) not in self.vip_users:
            return False
        
        expiry = datetime.fromisoformat(self.vip_users[str(user_id)]["expiry"])
        return datetime.now() < expiry
    
    def get_vip_expiry(self, user_id: int) -> str:
        """Получить дату истечения VIP."""
        if str(user_id) not in self.vip_users:
            return "Не активен"
        
        expiry = datetime.fromisoformat(self.vip_users[str(user_id)]["expiry"])
        return expiry.strftime("%Y-%m-%d %H:%M")
