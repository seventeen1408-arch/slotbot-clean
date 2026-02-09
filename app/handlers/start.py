"""Обработчик команды /start."""

from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message) -> None:
    """Обработчик команды /start."""
    try:
        welcome_text = (
            "🎰 *Добро пожаловать в SlotSignalsBot!*\n\n"
            "Я помогу вам получать сигналы для игры в слоты.\n\n"
            "*Команды:*\n"
            "/signals - Получить сигналы\n"
            "/vip - Информация о VIP подписке\n"
            "/help - Справка\n"
        )
        
        await message.answer(welcome_text)
        print(f"✅ /start от {message.from_user.id}")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
        print(f"❌ Ошибка /start: {e}")


@router.message(Command("help"))
async def help_command(message: types.Message) -> None:
    """Обработчик команды /help."""
    try:
        help_text = (
            "📖 *Справка по командам:*\n\n"
            "/start - Главное меню\n"
            "/signals - Получить сигналы\n"
            "/vip - VIP подписка\n"
            "/help - Эта справка\n"
        )
        
        await message.answer(help_text)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
