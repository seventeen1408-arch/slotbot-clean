"""Обработчик VIP подписки."""

from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("vip"))
async def vip_command(message: types.Message) -> None:
    """VIP подписка."""
    try:
        vip_text = (
            "👑 *VIP Подписка*\n\n"
            "Получите премиум доступ!\n\n"
            "✨ Что включено:\n"
            "• Сигналы за 30 минут\n"
            "• Точность 85%+\n"
            "• Приватный чат\n"
            "• Поддержка 24/7\n\n"
            "💰 Цена: $9.99/месяц\n\n"
            "Оплата через CryptoBot (TON)\n"
        )
        
        await message.answer(vip_text)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
