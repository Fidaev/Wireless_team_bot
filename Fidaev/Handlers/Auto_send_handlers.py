import asyncio
import datetime
from Fidaev import Config_bot
from Fidaev import SampleSql
from Fidaev.Create_bot import dp, bot
import aioschedule


async def auto_send():
    admin = [98908667, 55226487, 2224478, 409102496, 427471753]
    ya_i_iskan = [98908667]
    for Chat_id in ya_i_iskan:
        try:
            await SampleSql.get_Average_Subsystem_CPU_Usage(Chat_id)
            await bot.send_message(chat_id=98908667, text=f"{Config_bot.username(Chat_id)} получил Performance_RNC_Subsystem_CPU_Usage!")
        except:
            await bot.send_message(chat_id=98908667, text=f"{Config_bot.username(Chat_id)} не получил!")


async def scheduler():
    """Планировщик для отправки сообщений."""
    # имейте в виду, что это время удаленного сервера
    aioschedule.every().day.at("10:00").do(auto_send)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    """Функция запуска."""
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:')
    print(f'Время запуска: {start_time}\nПодключена база данных')
    await bot.send_message(chat_id=Config_bot.admin_id, text=f"Время запуска: {start_time}\nБот запущен")
    asyncio.create_task(scheduler())

