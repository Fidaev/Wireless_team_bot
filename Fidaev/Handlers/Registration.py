from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from Fidaev.Config_bot import admin_id
from Fidaev.Create_bot import dp, bot
from Fidaev import Keyboards
from Fidaev import SampleSql


class FSM(StatesGroup):
    User_name = State()
    finish = State()
    verification = State()


# начала регистрации пишем в словарь юзер айди
# @dp.message_handler(Text(equals='Регистрация', ignore_case=True), state=None)
async def process_user_id(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['User_ID'] = message.from_user.id
        await bot.send_message(chat_id=message.from_user.id, text="Как ваше имя?", reply_markup=Keyboards.markup)
        await FSM.User_name.set()
    except:
        await message.answer('Здравствуйте, Вас приветствует бот-помощник "BSC&RNC"!'
                             '\nДля начала необходимо пройти регистрацию!'
                             '\nПрошу нажмите кнопку "Регистрация"',
                             reply_markup=Keyboards.registration)


# ловим имя и пишем в словарь
# @dp.message_handler(state=FSM.User_name)
async def process_user_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Name'] = message.text
    await FSM.next()
    await message.reply('Отправьте пожалуйста свой контакт для регистрации'
                        '\n\nВыберите "Отправить контакт"', reply_markup=Keyboards.send_contact)


# ловим контакт и пишем в словарь
# @dp.message_handler(state=FSM.finish, content_types=['contact'])
async def process_finish_registration(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['contact'] = message.contact.phone_number
            data['Verification'] = 'NO'
            print(data)
        await SampleSql.sql_user_registration(state)
        await message.reply('Ваш запрос отправлен!'
                            '\n\nЖдите подтверждения или свяжитесь с администратором', reply_markup=Keyboards.markup)
        await bot.send_message(chat_id=admin_id,
                               text=f"Пользователь {data['Name']}(ID: {message.from_user.id}) отправил запрос на "
                                    f"регистрацию.")
        await state.finish()
    except:
        await message.reply(f'Мы вас знаем! Этот номер ранее был зарегистрирован.'
                            f'\n\nВыберите пункт',
                            reply_markup=Keyboards.main_menu)
        await state.finish()


def registeration_handlers(dp: Dispatcher):
    dp.register_message_handler(process_user_id, Text(equals='Регистрация', ignore_case=True), state=None)
    dp.register_message_handler(process_user_name, state=FSM.User_name)
    dp.register_message_handler(process_finish_registration, content_types=['contact'], state=FSM.finish)
