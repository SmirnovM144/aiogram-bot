from aiogram import Dispatcher
from .common import router as common_router
from .catalog import router as catalog_router
from .order import router as order_router


def register_all_handlers(dp: Dispatcher):
    """
    Регистрирует все роутеры в диспетчере.
    Порядок включения имеет значение (сверху вниз).
    """
    dp.include_router(common_router)
    dp.include_router(catalog_router)
    dp.include_router(order_router)
