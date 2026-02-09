"""Обработчик сигналов."""

from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("signals"))
async def signals_command(message: types.Message) -> None:
    """Получить сигналы."""
    try:
        signals_text = (
            "📊 *Текущие сигналы:*\n\n"
            "🎰 *Slot 1* - HIGH\n"
            "Коэффициент: 2.5x\n"
            "Вероятность: 65%\n\n"
            "🎰 *Slot 2* - MEDIUM\n"
            "Коэффициент: 1.8x\n"
            "Вероятность: 55%\n\n"
            "Для VIP сигналов: /vip\n"
        )
        
        await message.answer(signals_text)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
