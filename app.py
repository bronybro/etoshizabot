from aiogram import executor
from loader import dp
import handlers
#from utils.notify_admins import on_startup_notify


# async def on_startup(dispatcher):
#     # Уведомляет про запуск
#     await on_startup_notify(dispatcher)

async def shutdown(dispatcher: dp): # Закрываем соединение с машиной состояний
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
