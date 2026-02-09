# Архитектура SlotSignalsBot

Описание архитектуры и дизайна бота.

## 🏗️ Общая архитектура

```
┌─────────────────────────────────────────────────────────┐
│                    Telegram API                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                  Polling (getUpdates)
                       │
┌──────────────────────▼──────────────────────────────────┐
│                    aiogram 3.x                          │
│  (Dispatcher, Router, Handlers, FSM)                    │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   Handlers         Services      Storage
   ├─ start.py      ├─ VIPService  ├─ vip_users.json
   ├─ signals.py    └─ PostbackService
   ├─ funnel.py        └─ postbacks.json
   └─ vip.py
```

## 📦 Компоненты

### 1. main.py - Точка входа

**Ответственность:**
- Инициализация бота и диспетчера
- Регистрация роутеров
- Запуск polling
- Управление жизненным циклом

**Ключевые функции:**
```python
async def main():
    # 1. Создать Bot и Dispatcher
    # 2. Инициализировать сервисы
    # 3. Зарегистрировать роутеры
    # 4. Удалить webhook
    # 5. Запустить polling
```

### 2. Handlers - Обработчики команд

#### start.py
- `/start` - Главное меню
- `/help` - Справка

#### signals.py
- `/signals` - Текущие сигналы

#### funnel.py
- `/funnel` - Воронка продаж

#### vip.py
- `/vip` - VIP подписка

**Паттерн обработчика:**
```python
@router.message(Command("command"))
async def handler(message: types.Message):
    try:
        # Логика обработки
        await message.answer(text)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
```

### 3. Services - Бизнес-логика

#### VIPService
**Ответственность:**
- Управление VIP подписками
- Проверка VIP статуса
- Хранение в JSON

**Методы:**
```python
add_vip(user_id, days)      # Добавить VIP
is_vip(user_id)              # Проверить VIP
get_vip_expiry(user_id)      # Получить дату истечения
```

#### PostbackService
**Ответственность:**
- Отслеживание постбеков
- Расчет заработков
- Хранение в JSON

**Методы:**
```python
add_postback(user_id, partner, amount, status)
get_user_postbacks(user_id)
get_total_earnings(user_id)
```

## 🔄 Поток данных

### Получение сообщения

```
Telegram API
    │
    ▼
Polling (getUpdates)
    │
    ▼
aiogram Dispatcher
    │
    ▼
Router (выбор обработчика)
    │
    ▼
Handler (обработка)
    │
    ▼
Service (бизнес-логика)
    │
    ▼
JSON Storage (сохранение)
    │
    ▼
Ответ пользователю
```

## 💾 Хранилище данных

### JSON-based Storage

**Преимущества:**
- ✅ Простота (нет БД)
- ✅ Портативность (один файл)
- ✅ Легко масштабировать
- ✅ Легко бэкапить

**Недостатки:**
- Медленнее БД при большом объеме
- Нет конкурентного доступа

**Файлы:**
- `vip_users.json` - VIP подписки
- `postbacks.json` - Постбеки

### Структура данных

**vip_users.json:**
```json
{
  "123456": {
    "expiry": "2026-03-11T07:58:00",
    "created": "2026-02-09T07:58:00"
  }
}
```

**postbacks.json:**
```json
[
  {
    "user_id": 123456,
    "partner": "1win",
    "amount": 50.0,
    "status": "completed",
    "timestamp": "2026-02-09T07:58:00"
  }
]
```

## 🔐 Безопасность

### Защита токена
- BOT_TOKEN в переменных окружения
- Не коммитить .env в Git
- Использовать .gitignore

### Обработка ошибок
- Try-except в каждом обработчике
- Логирование ошибок
- Graceful degradation

### Валидация
- Проверка типов сообщений
- Обработка исключений

## 📊 Масштабируемость

### Текущая архитектура
- ✅ Один процесс
- ✅ Polling (не требует открытого порта)
- ✅ JSON хранилище
- ✅ Работает на Railway

### Для масштабирования

**Если нужна БД:**
```python
# Заменить JSON на SQLAlchemy
from sqlalchemy import create_engine
engine = create_engine("postgresql://...")
```

**Если нужны фоновые задачи:**
```python
# Добавить Celery
from celery import Celery
celery = Celery('bot')
```

**Если нужен webhook:**
```python
# Заменить polling на webhook
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
```

## 🧪 Тестирование

### Unit тесты

```python
def test_vip_service():
    vip = VIPService()
    vip.add_vip(123456, days=30)
    assert vip.is_vip(123456) == True
```

### Интеграционные тесты

```python
async def test_start_handler():
    message = Mock()
    await start_command(message)
    message.answer.assert_called_once()
```

## 🚀 Развертывание

### Локально
```bash
python main.py
```

### На Railway
```
Procfile: worker: python main.py
```

### Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## 📈 Мониторинг

### Логирование
```python
logger.info("✅ Событие")
logger.error("❌ Ошибка", exc_info=True)
```

### Метрики
- Количество пользователей
- Количество команд
- Количество VIP подписок
- Заработки

## 🔄 Жизненный цикл

```
Запуск
  │
  ▼
Инициализация сервисов
  │
  ▼
Регистрация роутеров
  │
  ▼
Удаление webhook
  │
  ▼
Запуск polling
  │
  ▼
Получение обновлений
  │
  ▼
Обработка сообщений
  │
  ▼
Отправка ответов
  │
  ▼
Сохранение данных
  │
  ▼
Повтор (получение обновлений)
```

## 🎯 Принципы дизайна

1. **Простота:** Минимум зависимостей, чистый код
2. **Модульность:** Разделение на handlers/services
3. **Надежность:** Обработка ошибок везде
4. **Масштабируемость:** Легко добавлять новые команды
5. **Портативность:** Работает везде (Railway, VPS, локально)

## 📝 Добавление новой команды

1. **Создать обработчик:**
```python
# app/handlers/new_command.py
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("newcommand"))
async def new_command(message: types.Message):
    await message.answer("Ответ")
```

2. **Зарегистрировать в main.py:**
```python
from app.handlers import new_command
dp.include_router(new_command.router)
```

3. **Готово!** Команда работает

## 📝 Добавление нового сервиса

1. **Создать сервис:**
```python
# app/services/new_service.py
class NewService:
    def method(self):
        pass
```

2. **Инициализировать в main.py:**
```python
new_service = NewService()
dp.workflow_data["new_service"] = new_service
```

3. **Использовать в обработчике:**
```python
new_service = message.bot.get("new_service")
new_service.method()
```
