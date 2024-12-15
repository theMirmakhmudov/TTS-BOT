from aiogram import Dispatcher
from handlers import start, select_parameters, inline_mode_on


def register_all_handlers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(select_parameters.router)
    dp.include_router(inline_mode_on.router)
