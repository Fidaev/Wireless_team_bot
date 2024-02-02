import asyncio
import schedule
from aiogram import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import SampleSql
from Handlers import Other_handlers, Main_Handlers, admin_handlers, Registration, Auto_send_handlers
from Handlers.Auto_send_handlers import on_startup


def main():
    from Handlers.Other_handlers import dp, sent_to_admin
    # asyncio.run(main2())
    Other_handlers.register_other_handlers(dp)
    admin_handlers.register_admin_handlers(dp)
    Main_Handlers.register_main_handlers(dp)
    Registration.registeration_handlers(dp)
    # Auto_send_handlers.register_autosend_handlers(dp)

    executor.start_polling(dp, on_startup=sent_to_admin)


if __name__ == "__main__":
    main()

