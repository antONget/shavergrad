import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import admin_handlers_menu_add, user_handlers, admin_handlers, admin_handlers_menu_edit,\
    admin_handlers_menu_delete, admin_handlers_promotion, other_handlers
from handlers.user_handlers import router
from middlewares.outer import FirstOuterMiddleware


# Инициализируем logger
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        filename="py_log.log",
        filemode='w',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    # logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
    # logging.debug("A DEBUG Message")
    # logging.info("An INFO")
    # logging.warning("A WARNING")
    # logging.error("An ERROR")
    # logging.critical("A message of CRITICAL severity")

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
    dp.include_router(admin_handlers_promotion.router)
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Здесь будем регистрировать миддлвари
    router.message.middleware(FirstOuterMiddleware())
    router.callback_query.middleware(FirstOuterMiddleware())

    # Пропускаем накопившиеся update и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
