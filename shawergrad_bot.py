import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import admin_handlers_menu_add, user_handlers, admin_handlers, admin_handlers_menu_edit, admin_handlers_menu_delete


# Инициализируем logger
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher()

    # Регистрируем router в диспетчере

    dp.include_router(admin_handlers.router)
    dp.include_router(admin_handlers_menu_add.router)
    dp.include_router(admin_handlers_menu_edit.router)
    dp.include_router(admin_handlers_menu_delete.router)

    # Пропускаем накопившиеся update и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
