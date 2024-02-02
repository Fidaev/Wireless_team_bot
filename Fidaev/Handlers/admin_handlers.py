import os
from aiogram.types import InputFile
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from pytube import YouTube
from Fidaev import Config_bot
from Fidaev import Keyboards
from Fidaev import SampleSql
from Fidaev.Create_bot import dp, bot


class FSM(StatesGroup):
    verification = State()
    ad = State()


# @dp.message_handler(Text(equals='admin', ignore_case=True), state="*")
# @dp.message_handler(commands=['admin'], state="*")
async def process_get_not_verification(message: types.Message):
    global result, not_confirm_user
    if message.from_user.id == Config_bot.admin_id:
        if await SampleSql.get_user_not_confirmation() is not None:
            result = (await SampleSql.get_user_not_confirmation())[1]
            not_confirm_user = (await SampleSql.get_user_not_confirmation())[0]
            await message.answer(f"Пользователь по имени {result}(ID:{not_confirm_user}) зарегистрирован но не "
                                 f"подтверждён."
                                 f"\nХотите подтвердить?", reply_markup=Keyboards.verification)
            await FSM.verification.set()
        else:
            await message.answer("все подтверждены")


# @dp.message_handler(state=FSM.verification)
async def process_get_site_id(message: types.Message, state: FSMContext):
    if message.text == 'YES':
        await SampleSql.for_admin_user_confirmation()
        await message.answer(f'Пользователь {result}(ID:{not_confirm_user}) подтверждён',
                             reply_markup=Keyboards.btnmenu)
        await bot.send_message(chat_id=not_confirm_user, text=f"Уважаемый {result} поздравляю, вас подтвердили!",
                               reply_markup=Keyboards.main_menu)
        await state.finish()
    else:
        await message.answer('Пользователь не подтверждён', reply_markup=Keyboards.btnmenu)


# @dp.message_handler(Text(equals='ad', ignore_case=True), state="*")
# @dp.message_handler(commands=['ad'], state="*")
async def process_ad(message: types.Message):
    # if message.from_user.id == "98908667":
    await message.answer('Отправим объявление!')
    await FSM.ad.set()


# @dp.message_handler(state=FSM.ad)
async def process_ad_msg(message: types.Message, state: FSMContext):
    users = [98908667, 51665305, 196120188, 138238312, 409102496, 427471753, 4518641, 761432533]
    # admin = [98908667]
    for Chat_id in users:
        try:
            await bot.send_message(chat_id=Chat_id, text=f"{message.text}")
            await bot.send_message(chat_id=98908667, text=f"{Config_bot.username(Chat_id)} получил!")
            await state.finish()
        except:
            await bot.send_message(chat_id=98908667, text=f"{Config_bot.username(Chat_id)} не получил!")


# @dp.message_handler(Text(equals='auto', ignore_case=True), state="*")
# @dp.message_handler(commands=['auto'], state="*")
async def process_autosend(message: types.Message, state: FSMContext):
    users = [98908667, 51665305, 196120188, 55226487, 138238312, 463272027, 173477426, 2224478, 409102496, 85569107,
             427471753]
    admin = [98908667]
    for Chat_id in admin:
        try:
            await SampleSql.get_Average_Subsystem_CPU_Usage(Chat_id)
            await bot.send_message(chat_id=98908667, text=f"{Config_bot.username(Chat_id)} получил!")
        except:
            await bot.send_message(chat_id=98908667, text=f"{Config_bot.username(Chat_id)} не получил!")


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(process_get_not_verification, Text(equals='admin', ignore_case=True), state="*")
    dp.register_message_handler(process_get_not_verification, commands=['admin'], state="*")
    dp.register_message_handler(process_get_site_id, state=FSM.verification)
    dp.register_message_handler(process_ad, Text(equals='ad', ignore_case=True), state="*")
    dp.register_message_handler(process_ad, commands=['ad'], state="*")
    dp.register_message_handler(process_ad_msg, state=FSM.ad)
    dp.register_message_handler(process_autosend, Text(equals='auto', ignore_case=True), state="*")
    dp.register_message_handler(process_autosend, commands=['auto'], state="*")
