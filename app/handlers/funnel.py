"""Обработчик воронки продаж."""

from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("funnel"))
async def funnel_command(message: types.Message) -> None:
    """Воронка продаж."""
    try:
        funnel_text = (
            "🎯 *Специальное предложение:*\n\n"
            "Получите доступ к премиум сигналам!\n\n"
            "✨ Премиум функции:\n"
            "• Сигналы за 30 минут до события\n"
            "• Точность 85%+\n"
            "• Поддержка 24/7\n\n"
            "Стоимость: $9.99/месяц\n\n"
            "Нажмите /vip для оплаты\n"
        )
        
        await message.answer(funnel_text)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
