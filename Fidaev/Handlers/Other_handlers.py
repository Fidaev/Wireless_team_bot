import datetime
import schedule
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from Fidaev import Keyboards
from Fidaev import SampleSql
from Fidaev.Create_bot import dp, bot
from Fidaev.Config_bot import admin_id


async def sent_to_admin(dp):
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:')
    await bot.send_message(chat_id=admin_id, text=f"Start time: {start_time}"
                                                  f"\nБот запущен")
    print(f'Start time: {start_time}'
          '\nData base connected')


# @dp.message_handler(commands=['start'], state="*")
async def process_start(message: types.Message, state: FSMContext):
    await message.answer('Здравствуйте, Вас приветствует бот-помощник "BSC&RNC"!'
                         '\nДля начала необходимо пройти регистрацию!'
                         '\nПрошу нажмите кнопку "Регистрация"'
                         '\n\n Если вы уже зарегистрированы нажмите "Main menu"', reply_markup=Keyboards.registration)
    await state.finish()


# @dp.message_handler(commands=['main_menu'], state="*")
# @dp.message_handler(Text(equals='🔝Main menu', ignore_case=True), state="*")
async def process_menu(message: types.Message, state: FSMContext):
    if await SampleSql.get_user_confirmation(message.from_user.id) == 'YES':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'NO':
        await bot.send_message(chat_id=admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать Бот (🔝Main menu)")
    #     await message.answer('Извините администратор Вас пока не подтвердил, ждите или свяжитесь с администраторм')
    # else:
    #     await message.answer('Вы не зарегистрированы.')


def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start, commands=['start'], state="*")
    dp.register_message_handler(process_menu, commands=['main_menu'], state="*")
    dp.register_message_handler(process_menu, Text(equals='🔝Main menu', ignore_case=True), state="*")
    dp.register_message_handler(process_menu, Text(equals='Main menu', ignore_case=True), state="*")
