"""
SlotSignalsBot - Telegram бот для сигналов слотов.
Чистая архитектура: только polling, без webhook.
"""

import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode

from app.handlers import start, signals, funnel, vip
from app.services.vip_service import VIPService
from app.services.postback_service import PostbackService

# Загрузить переменные окружения
load_dotenv()

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не установлен!")

logger.info(f"🤖 BOT_TOKEN: {BOT_TOKEN[:20]}...")


async def main() -> None:
    """Главная функция бота."""
    try:
        # Инициализировать бота
        bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        
        # Инициализировать сервисы
        vip_service = VIPService()
        postback_service = PostbackService()
        
        # Сохранить сервисы в контекст
        dp.workflow_data["vip_service"] = vip_service
        dp.workflow_data["postback_service"] = postback_service
        
        logger.info("✅ Сервисы инициализированы")
        
        # Регистрировать роутеры
        dp.include_router(start.router)
        dp.include_router(signals.router)
        dp.include_router(funnel.router)
        dp.include_router(vip.router)
        
        logger.info("✅ Роутеры зарегистрированы")
        
        # Удалить webhook и очистить очередь
        logger.info("🧹 Удаление webhook и очистка очереди...")
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ Webhook удален, очередь очищена")
        
        # Запустить polling
        logger.info("📡 Запуск polling...")
        logger.info("✅ БОТ ГОТОВ К РАБОТЕ!")
        
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            skip_updates=False
        )
    
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)
        raise
    
    finally:
        logger.info("🛑 Бот завершил работу")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Неожиданная ошибка: {e}", exc_info=True)
