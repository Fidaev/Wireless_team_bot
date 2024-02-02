import math
import os
import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from Fidaev import Config_bot
from Fidaev import Keyboards
from Fidaev import SampleSql
from Fidaev import Functions
from Fidaev.Create_bot import dp, bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from Fidaev.Project_Iskander.DATA.main_rnc import rnc_configuration
from Fidaev.Project_Iskander.bsc77725102023 import bsc_configuration


class FSM(StatesGroup):
    Site_id = State()
    Cell_id = State()
    GSM_cell_id = State()
    UMTS_cell_id = State()
    LTE_cell_id = State()
    Power_Calculator = State()
    Watt_to_dBm = State()
    dBm_to_Watt = State()
    Power_Information = State()
    location = State()
    power_change = State()
    power_change_technology = State()
    power_change_UMTS_cell = State()
    power_change_UMTS_ulocell = State()
    power_change_UMTS_watt = State()
    cell_deletion_technology = State()
    cell_deletion_UMTS_cell = State()
    cell_deletion_UMTS_nodeb = State()
    cell_deletion_UMTS_lac = State()
    cell_deletion_UMTS_ulocell = State()
    blk_brd = State()
    blk_brd_set = State()
    Site_ID_Converter = State()
    technology = State()
    USN = State()
    USN_set = State()
    USN_UMTS = State()
    USN_GSM = State()
    USN_UMTS_set = State()
    MML_RET_config = State()
    Performance = State()
    Performance_Wireless = State()
    Performance_rtwp = State()
    Performance_period = State()
    Performance_rtwp_cellid = State()
    Performance_rtwp_yesterday_cellid = State()
    Performance_Core = State()
    Performance_billing_reject = State()
    Performance_billing_reject_period = State()
    Performance_billing_reject_incoming = State()
    Performance_PRB = State()
    Performance_PRB_period = State()
    Performance_PRB_siteid = State()
    Performance_User_period = State()
    Performance_User_siteid = State()
    Performance_LTE_TA_period = State()
    Performance_LTE_TA_siteid = State()
    Performance_UMTS_PD_period = State()
    Performance_UMTS_PD_cellid = State()
    Performance_UMTS_Call_drop_period = State()
    Performance_UMTS_Call_drop_cellid = State()
    configuration = State()
    configuration_rf_plan = State()
    configuration_omch = State()
    configuration_umts_ip = State()
    configuration_mask = State()
    configuration_config = State()
    bsc_configuration_rf_plan = State()
    bsc_configuration_omch = State()
    bsc_configuration_gsm_ip = State()
    api = State()
    api_active_alarms = State()
    api_mml_list = State()
    api_mml_list_dsp_cell = State()
    api_mml_list_dsp_ulocell = State()
    api_dsp_mmctx = State()
    ringit_converter = State()


@dp.message_handler(Text(equals='Ringit Converter', ignore_case=True), state="*")
async def ringit_converter(message: types.Message, state: FSMContext):
    if await SampleSql.get_user_confirmation(message.from_user.id) == 'YES' and (await SampleSql.get_user_right(
            message.from_user.id) == 'Wireless' or await SampleSql.get_user_right(message.from_user.id) == 'API'):
        await message.answer("Напишите сколько Ringit хотите перевести в доллары или в суммы",
                             reply_markup=Keyboards.btnmenu)
        await FSM.ringit_converter.set()
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'YES' and await SampleSql.get_user_right(
            message.from_user.id) != 'Wireless':
        await message.answer("Вам сюда нельзя.")
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать For tests но у него нет прав")
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'NO':
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать Бот")
    #     await message.answer('Извините администратор Вас пока не подтвердил, ждите или свяжитесь с администраторм')
    # else:
    #     await message.answer('Вы не зарегистрированы.')


@dp.message_handler(state=FSM.ringit_converter)
async def ringit_converter(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    else:
        try:
            summa = int(message.text)
            ringit_to_dollars = round(summa / 4.6, 2)
            ringit_to_summ = round(ringit_to_dollars * 12300, 2)
            await message.answer(f'Ringit = {summa}\n'
                                 f'USD = {ringit_to_dollars}\n'
                                 f'SUM = {ringit_to_summ}', reply_markup=Keyboards.btnmenu)
            await bot.send_message(chat_id=Config_bot.admin_id,
                                   text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                        f"Перевёл {summa} Ringit")
        except:
            await message.answer("Напиши цифрами",
                                 reply_markup=Keyboards.btnmenu)


@dp.message_handler(commands=['For_tests'], state="*")
@dp.message_handler(Text(equals='For tests', ignore_case=True), state="*")
async def api_menu(message: types.Message, state: FSMContext):
    if await SampleSql.get_user_confirmation(message.from_user.id) == 'YES' and (await SampleSql.get_user_right(
            message.from_user.id) == 'Wireless' or await SampleSql.get_user_right(message.from_user.id) == 'API'):
        await message.answer("Выберите пункт", reply_markup=Keyboards.for_test_menu)
        await FSM.api.set()
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'YES' and await SampleSql.get_user_right(
            message.from_user.id) != 'Wireless':
        await message.answer("Вам сюда нельзя, тут админ проводит тесты.")
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать For tests но у него нет прав")
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'NO':
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать Бот (Site ID)")
    #     await message.answer('Извините администратор Вас пока не подтвердил, ждите или свяжитесь с администраторм')
    # else:
    #     await message.answer('Вы не зарегистрированы.')


@dp.message_handler(state=FSM.api)
async def api(message: types.Message, state: FSMContext):
    if message.text == 'Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == 'Active Alarms':
        await message.answer('Здесь вы можете проверить активные аварии БС или других элементов сети.'
                             '\n\nНапишите NE_Name \n\n(Например: ATC-241(1014) или UGW_TAS2)',
                             reply_markup=Keyboards.btnmenuand_back)
        await FSM.api_active_alarms.set()
    elif message.text == 'Get MML':
        await message.answer('Здесь вы можете отправить MML команды и получить результат'
                             '\n\nВыберите MML',
                             reply_markup=Keyboards.mml_menu)
        await FSM.api_mml_list.set()
    elif message.text == 'DSP MMCTX':
        await message.answer('Здесь вы можете узнать какая БС обслуживает абонента.'
                             '\n\nНапишите номер телефона \n\n(Например: 998991234567)',
                             reply_markup=Keyboards.btnmenuand_back)
        await FSM.api_dsp_mmctx.set()
    else:
        await message.answer('Выберите пункт')
        await FSM.api.set()


@dp.message_handler(state=FSM.api_dsp_mmctx)
async def api_dsp_mmctx(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer("Выберите пункт", reply_markup=Keyboards.for_test_menu)
        await FSM.api.set()
    else:
        try:
            if "LTE" in await Functions.mml_request_dsp_mmctx(message.text):
                a = f"{await Functions.mml_request_dsp_mmctx(message.text)}".replace("LTE", "")
                enodeb_id = int((a.replace("43408", ""))[:5], 16)
                cell_id = int((a.replace("43408", ""))[-2:], 16)
                await SampleSql.for_dsp_mmctx(message.from_user.id, enodeb_id, cell_id, a)
                await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                         f"(ID: {message.from_user.id}) "
                                                                         f"Конвертировал E-UTRAN cell global identity"
                                                                         f"\nID: {message.text}")
            elif "UMTS" in await Functions.mml_request_dsp_mmctx(message.text):
                c = await Functions.mml_request_dsp_mmctx(message.text)
                a = f"{c[0]}"
                rnc_id = f"{c[1]}"
                cell_id = int((a.replace("43408", ""))[-4:], 16)
                await SampleSql.for_dsp_mmctx_umts(message.from_user.id, cell_id, a, rnc_id)
                await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                         f"(ID: {message.from_user.id}) "
                                                                         f"Service area of user"
                                                                         f"\nID: {message.text}")
            elif "GSM" in await Functions.mml_request_dsp_mmctx(message.text):
                c = await Functions.mml_request_dsp_mmctx(message.text)
                a = f"{c[0]}"
                lac = f"{int(c[1][-6:-2], 16)}"
                cell_id = int((a.replace("0x", ""))[-4:], 16)
                await SampleSql.for_dsp_mmctx_gsm(message.from_user.id, cell_id, a, lac)
                await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                         f"(ID: {message.from_user.id}) "
                                                                         f"Конвертировал Cell Id"
                                                                         f"\nID: {message.text}")
        except:
            await message.answer(f'Неправильный ввод данных',
                                 reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                                 .add(KeyboardButton("🔙Back"))
                                 .add(KeyboardButton("🔝Main menu")))


@dp.callback_query_handler(state=FSM.api_dsp_mmctx)
async def process_Site_location(callback: types.CallbackQuery, state: FSMContext):
    await SampleSql.for_get_location(callback.from_user.id, callback.data)


@dp.message_handler(state=FSM.api_mml_list)
async def api_mml_list(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer("Выберите пункт", reply_markup=Keyboards.for_test_menu)
        await FSM.api.set()
    elif message.text == 'DSP CELL':
        await message.answer('Здесь вы можете проверить LTE CELL'
                             '\n\nНапишите Site ID \n\n(Например: 1014)',
                             reply_markup=Keyboards.btnmenuand_back)
        await FSM.api_mml_list_dsp_cell.set()
    elif message.text == 'DSP ULOCELL':
        await message.answer('Здесь вы можете проверить UMTS CELL'
                             '\n\nНапишите Site ID \n\n(Например: 1014)',
                             reply_markup=Keyboards.btnmenuand_back)
        await FSM.api_mml_list_dsp_ulocell.set()
    elif message.text == 'DSP LICRATE':
        volte_subs = await Functions.mml_request_dsp_licrate()
        await message.answer(f'{volte_subs}')
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"использовал DSP LICRATE")
    else:
        await message.answer('Выберите пункт')
        await FSM.api_mml_list.set()


@dp.message_handler(state=FSM.api_active_alarms)
async def api_active_alarms(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer("Выберите пункт", reply_markup=Keyboards.for_test_menu)
        await FSM.api.set()
    else:
        await Functions.fault_request(message.from_user.id, message.text)
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"проверил аварии NE: {message.text}")
        await Functions.fault_request(Config_bot.admin_id, message.text)


@dp.message_handler(state=FSM.api_mml_list_dsp_ulocell)
async def api_mml_list_dsp_ulocell(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Здесь вы можете отправить MML команды и получить результат'
                             '\n\nВыберите MML',
                             reply_markup=Keyboards.mml_menu)
        await FSM.api_mml_list.set()
    else:
        await Functions.mml_request_dsp_ulocell(message.from_user.id, message.text)
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"использовал DSP ULOCELL: {message.text}")
        # await Functions.mml_request(Config_bot.admin_id, message.text)


@dp.message_handler(state=FSM.api_mml_list_dsp_cell)
async def api_mml_list_dsp_cell(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Здесь вы можете отправить MML команды и получить результат'
                             '\n\nВыберите MML',
                             reply_markup=Keyboards.mml_menu)
        await FSM.api_mml_list.set()
    else:
        await Functions.mml_request_dsp_cell(message.from_user.id, message.text)
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"использовал DSP CELL: {message.text}")
        # await Functions.mml_request(Config_bot.admin_id, message.text)


@dp.message_handler(commands=['Configuration'], state="*")
@dp.message_handler(Text(equals='Configuration', ignore_case=True), state="*")
async def configuration(message: types.Message, state: FSMContext):
    if await SampleSql.get_user_confirmation(message.from_user.id) == 'YES' and await SampleSql.get_user_right(
            message.from_user.id) == 'Wireless':
        await message.answer("Выберите пункт", reply_markup=Keyboards.configuration)
        await FSM.configuration.set()
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'YES' and await SampleSql.get_user_right(
            message.from_user.id) != 'Wireless':
        await message.answer("У Вас нет прав")
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать Configuration но у него нет прав")
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'NO':
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать Бот (Site ID)")
    #     await message.answer('Извините администратор Вас пока не подтвердил, ждите или свяжитесь с администраторм')
    # else:
    #     await message.answer('Вы не зарегистрированы.')


@dp.message_handler(state=FSM.configuration)
async def config_rnc(message: types.Message, state: FSMContext):
    if message.text == 'Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == 'BSC':
        await message.answer('Отправьте РФ План', reply_markup=Keyboards.btnmenuand_back)
        await FSM.bsc_configuration_rf_plan.set()
    elif message.text == 'RNC':
        await message.answer('Отправьте РФ План', reply_markup=Keyboards.btnmenuand_back)
        await FSM.configuration_rf_plan.set()
    else:
        await message.answer('Выберите пункт', reply_markup=Keyboards.configuration)
        await FSM.configuration.set()


@dp.message_handler(state=FSM.configuration_rf_plan)
@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=FSM.configuration_rf_plan)
async def load_document(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer("Выберите пункт", reply_markup=Keyboards.configuration)
        await FSM.configuration.set()
    else:
        # try:
        path = os.getcwd()
        today = datetime.date.today().strftime('%Y-%m-%d')
        try:
            os.mkdir(f"{path}/Input_files/{today}/documents")
        except:
            pass
        files = os.listdir(fr"{path}/Input_files/{today}/documents")
        for fayl in files:
            os.remove(fr"{path}/Input_files/{today}/documents/{fayl}")
        files_for_output = os.listdir(fr"{path}/Output_files")
        for fayl in files_for_output:
            os.remove(fr"{path}/Output_files/{fayl}")
        await message.document.download(destination_dir=fr"{path}/Input_files/{today}")
        await message.answer(text="Введите IP-адрес OM - канала. Например 10.65.0.15 :",
                             reply_markup=Keyboards.btnmenuand_back)
        await FSM.configuration_omch.set()
    # except:
    #     await message.answer('Отправьте РФ План', reply_markup=Keyboards.btnmenuand_back)
    #     await FSM.configuration_rf_plan.set()


@dp.message_handler(state=FSM.configuration_omch)
async def configuration_get_omch(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Отправьте РФ План', reply_markup=Keyboards.btnmenuand_back)
        await FSM.configuration_rf_plan.set()
    else:
        async with state.proxy() as data:
            data['omch_ip'] = message.text
        await message.answer('Введите IP-адрес UMTS сервиса. Например 10.75.0.15 :',
                             reply_markup=Keyboards.btnmenuand_back)
        await FSM.configuration_umts_ip.set()
        print(data)


@dp.message_handler(state=FSM.configuration_umts_ip)
async def configuration_gsm_ip(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer(text="Введите IP-адрес OM - канала. Например 10.65.0.15 :",
                             reply_markup=Keyboards.btnmenuand_back)
        await FSM.configuration_omch.set()
    else:
        async with state.proxy() as data:
            data['umts_ip'] = message.text
        await message.answer('Введите маску IP-адреса. Например 255.255.255.224 :',
                             reply_markup=Keyboards.btnmenuand_back)
        await FSM.configuration_mask.set()
        print(data)


@dp.message_handler(state=FSM.configuration_mask)
async def configuration_mask(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Введите IP-адрес UMTS сервиса. Например 10.75.0.15 :',
                             reply_markup=Keyboards.btnmenuand_back)
        await FSM.configuration_umts_ip.set()
    else:
        async with state.proxy() as data:
            data['mask'] = message.text
        await message.answer("""Выберите необходимую конфигурацию: 

Если  UMTS2100 3/3/3 нажмите = 1
Если  UMTS900  1/1/1 нажмите = 2
Если  UMTS2100 3/3/3 и UMTS900 1/1/1 нажмите = 3
Если  UMTS2100 2/2/2 EasyMacro 2.0 нажмите = 4

Если  UMTS2100 2/2/2 Massive MIMO нажмите = 5
Если  UMTS2100 2/2/2 Massive MIMO и UMTS900 1/1/1  нажмите = 6
Если  UMTS2100 6/6/6 6-секторная нажмите = 7
Если  UMTS2100 6/6/6 6-секторная и UMTS900 1/1/1  нажмите = 8

Если  UMTS2100 2// BTS3902E нажмите = 9

Если  UMTS2100 2// BTS3900 Lampsite нажмите = 10
Если  UMTS2100 2/2/ BTS3900 Lampsite нажмите = 11
Если  UMTS2100 2/2/2 BTS3900 Lampsite нажмите = 12
Если  UMTS2100 2/2/2/2 BTS3900 Lampsite нажмите = 13
Если  UMTS2100 2/2/2/2/2 BTS3900 Lampsite нажмите = 14

Если  UMTS2100 3// BTS5900 Lampsite нажмите = 15
Если  UMTS2100 3/3/ BTS5900 Lampsite нажмите = 16
Если  UMTS2100 3/3/3 BTS5900 Lampsite нажмите = 17
Если  UMTS2100 3/3/3/3 BTS5900 Lampsite нажмите = 18
Если  UMTS2100 3/3/3/3/3 BTS5900 Lampsite нажмите = 19

Если  UMTS2100 1/1/1 BTS5900 Lampsite для MobiUZ нажмите = 20
Если  UMTS2100 1/1/1 BTS5900 Lampsite для Beeline нажмите = 21
Если  UMTS2100 1/1/1 BTS5900 Lampsite для Ucell нажмите = 22""", reply_markup=Keyboards.btnmenuand_back)
        await FSM.configuration_config.set()
        print(data)


@dp.message_handler(state=FSM.configuration_config)
async def configuration_config(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Введите маску IP-адреса. Например 255.255.255.224 :',
                             reply_markup=Keyboards.btnmenuand_back)
        await FSM.configuration_mask.set()
    else:
        async with state.proxy() as data:
            data['config'] = message.text
        await message.answer("""Генерация конфигурации...""", reply_markup=Keyboards.btnmenu)
        await rnc_configuration(message.from_user.id, data["omch_ip"], data["umts_ip"], data["mask"], data["config"])
        await message.answer("""Готово!""", reply_markup=Keyboards.btnmenu)
        await state.finish()
        print(data)


@dp.message_handler(state=FSM.bsc_configuration_rf_plan)
@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=FSM.bsc_configuration_rf_plan)
async def bsc_load_document(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer("Выберите пункт", reply_markup=Keyboards.configuration)
        await FSM.configuration.set()
    else:
        # try:
        path = os.getcwd()
        today = datetime.date.today().strftime('%Y-%m-%d')
        try:
            os.mkdir(f"{path}/Input_files/{today}/documents")
        except:
            pass
        files = os.listdir(fr"{path}/Input_files/{today}/documents")
        for fayl in files:
            os.remove(fr"{path}/Input_files/{today}/documents/{fayl}")
        files_for_output = os.listdir(fr"{path}/Output_files")
        for fayl in files_for_output:
            os.remove(fr"{path}/Output_files/{fayl}")
        await message.document.download(destination_dir=fr"{path}/Input_files/{today}")
        await message.answer(text="Введите IP-адрес OM - канала. Например 10.65.0.15 :",
                             reply_markup=Keyboards.btnmenuand_back)
        await FSM.bsc_configuration_omch.set()


@dp.message_handler(state=FSM.bsc_configuration_omch)
async def bsc_configuration_get_omch(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Отправьте РФ План', reply_markup=Keyboards.btnmenuand_back)
        await FSM.bsc_configuration_rf_plan.set()
    else:
        async with state.proxy() as data:
            data['omch_ip'] = message.text
        await message.answer('Введите IP-адрес GSM сервиса. Например 10.70.0.15 :',
                             reply_markup=Keyboards.btnmenuand_back)
        await FSM.bsc_configuration_gsm_ip.set()
        print(data)


@dp.message_handler(state=FSM.bsc_configuration_gsm_ip)
async def bsc_configuration_gsm_ip(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer(text="Введите IP-адрес OM - канала. Например 10.65.0.15 :",
                             reply_markup=Keyboards.btnmenuand_back)
        await FSM.bsc_configuration_omch.set()
    else:
        async with state.proxy() as data:
            data['gsm_ip'] = message.text
        await message.answer("""Генерация конфигурации...""", reply_markup=Keyboards.btnmenu)
        await bsc_configuration(message.from_user.id, data["omch_ip"], data["gsm_ip"])
        await message.answer("""Готово!""", reply_markup=Keyboards.btnmenu)
        await state.finish()
        print(data)


# @dp.message_handler(commands=['siteid'], state="*")
# @dp.message_handler(Text(equals='Site id', ignore_case=True), state="*")
async def process_site_id(message: types.Message, state: FSMContext):
    if await SampleSql.get_user_confirmation(message.from_user.id) == 'YES':
        await message.answer("Введите Site ID"
                             "\n\nНапример: 1000", reply_markup=Keyboards.btnmenu)
        await FSM.Site_id.set()
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'NO':
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать Бот (Site ID)")
    #     await message.answer('Извините администратор Вас пока не подтвердил, ждите или свяжитесь с администраторм')
    # else:
    #     await message.answer('Вы не зарегистрированы.')


# @dp.message_handler(state=FSM.Site_id)
async def process_get_site_id(message: types.Message, state: FSMContext):
    if message.text == 'Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    else:
        try:
            async with state.proxy() as site:
                site['site'] = int(message.text)
            int(message.text)
            await SampleSql.for_get_site_information(message.from_user.id, message.text)
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"ищет сайт: {message.text}")
        except:
            await message.answer(text="Такой базы нет в БД или ввели неправильный атрибут",
                                 disable_web_page_preview=True,
                                 reply_markup=Keyboards.btnmenu)
            await bot.send_message(chat_id=Config_bot.admin_id,
                                   text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                        f"ищет сайт, но он ввёл неправильный атрибут: {message.text}")


@dp.callback_query_handler(state=FSM.Site_id)
async def process_Site_location(callback: types.CallbackQuery, state: FSMContext):
    await SampleSql.for_get_location(callback.from_user.id, callback.data)


# @dp.message_handler(commands=['Performance'], state="*")
# @dp.message_handler(Text(equals='Performance', ignore_case=True), state="*")
async def Performance(message: types.Message, state: FSMContext):
    if await SampleSql.get_user_confirmation(message.from_user.id) == 'YES':
        await message.answer("Выберите пункт", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                selective=False)
                             .add(KeyboardButton("Core"),
                                  KeyboardButton("Wireless"))
                             .add(KeyboardButton("🔝Main menu")))
        await FSM.Performance.set()
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'NO':
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать Бот (Performance)")
    #     await message.answer('Извините администратор Вас пока не подтвердил, ждите или свяжитесь с администраторм')
    # else:
    #     await message.answer('Вы не зарегистрированы.')


# @dp.message_handler(state=FSM.Performance)
async def Performance_dep(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == 'Wireless':
        await message.answer('Выберите технологию', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                     selective=False)
                             .add(KeyboardButton("UMTS"),
                                  KeyboardButton("LTE"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_Wireless.set()
    elif message.text == 'Core':
        await message.answer('Выберите статистику', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                     selective=False)
                             .add(KeyboardButton("Отказы от биллинга"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_Core.set()


# @dp.message_handler(state=FSM.Performance_Core)
async def Performance_Core(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer("Выберите пункт", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                selective=False)
                             .add(KeyboardButton("Core"),
                                  KeyboardButton("Wireless"))
                             .add(KeyboardButton("🔝Main menu")))
        await FSM.Performance.set()
    elif message.text == 'Отказы от биллинга':
        await message.answer('Выберите пункт', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                selective=False)
                             .add(KeyboardButton("Исходящий"),
                                  KeyboardButton("Входящий"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_billing_reject.set()


# @dp.message_handler(state=FSM.Performance_billing_reject)
async def Performance_billing_reject(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите статистику', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                     selective=False)
                             .add(KeyboardButton("Отказы от биллинга"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_Core.set()
    elif message.text == 'Исходящий':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Today"))
                             .add(KeyboardButton("Last 3 days"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_billing_reject_period.set()
    elif message.text == 'Входящий':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Today"))
                             .add(KeyboardButton("Last 3 days"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_billing_reject_incoming.set()


# @dp.message_handler(state=FSM.Performance_billing_reject_incoming)
async def Performance_billing_reject_incoming(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите пункт', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                selective=False)
                             .add(KeyboardButton("Исходящий"),
                                  KeyboardButton("Входящий"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_billing_reject.set()
    elif message.text == 'Today':
        await SampleSql.get_core_incoming_today(message.from_user.id)
        await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                 f"(ID: {message.from_user.id}) "
                                                                 f"Получил статистику отказы от "
                                                                 f"биллинга: {message.text}")
    elif message.text == 'Last 3 days':
        await SampleSql.get_core_Billing_reject_3days("102", message.from_user.id)
        await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                 f"(ID: {message.from_user.id}) "
                                                                 f"Получил статистику отказы от "
                                                                 f"биллинга: {message.text}")


# @dp.message_handler(state=FSM.Performance_billing_reject_period)
async def Performance_billing_reject_period(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите пункт', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                selective=False)
                             .add(KeyboardButton("Исходящий"),
                                  KeyboardButton("Входящий"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_billing_reject.set()
    elif message.text == 'Today':
        await SampleSql.get_core_outgoing_today(message.from_user.id)
        await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                 f"(ID: {message.from_user.id}) "
                                                                 f"Получил статистику отказы от "
                                                                 f"биллинга: {message.text}")
    elif message.text == 'Last 3 days':
        await SampleSql.get_core_Billing_reject_3days("101", message.from_user.id)
        await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                 f"(ID: {message.from_user.id}) "
                                                                 f"Получил статистику отказы от "
                                                                 f"биллинга: {message.text}")


# @dp.message_handler(state=FSM.Performance_Wireless)
async def Performance_Wireless(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer("Выберите пункт", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                selective=False)
                             .add(KeyboardButton("Core"),
                                  KeyboardButton("Wireless"))
                             .add(KeyboardButton("🔝Main menu")))
        await FSM.Performance.set()
    elif message.text == 'UMTS':
        await message.answer('Выберите статистику', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                     selective=False)
                             .add(KeyboardButton("CS Service Call Drop Rate"))
                             .add(KeyboardButton("Mean RTWP"))
                             .add(KeyboardButton("Propogation Delay"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_rtwp.set()
    elif message.text == 'LTE':
        await message.answer('Выберите статистику', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                     selective=False)
                             .add(KeyboardButton("PRB Utilization"))
                             .add(KeyboardButton("Number of users in a cell"))
                             .add(KeyboardButton("Timing Advance in LTE"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_PRB.set()


# @dp.message_handler(state=FSM.Performance_PRB)
async def Performance_PRB(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите технологию', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                     selective=False)
                             .add(KeyboardButton("UMTS"),
                                  KeyboardButton("LTE"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_Wireless.set()
    elif message.text == 'PRB Utilization':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Yesterday"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_PRB_period.set()
    elif message.text == 'Number of users in a cell':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Yesterday"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_User_period.set()
    elif message.text == 'Timing Advance in LTE':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Yesterday"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_LTE_TA_period.set()


# @dp.message_handler(state=FSM.Performance_LTE_TA_period)
async def Performance_LTE_TA_period(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите статистику', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                     selective=False)
                             .add(KeyboardButton("PRB Utilization"))
                             .add(KeyboardButton("Number of users in a cell"))
                             .add(KeyboardButton("Timing Advance in LTE"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_PRB.set()
    elif message.text == 'Yesterday':
        await message.answer('Введите Site ID'
                             '\nНапример: 1014', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                  selective=False)
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_LTE_TA_siteid.set()


# @dp.message_handler(state=FSM.Performance_LTE_TA_siteid)
async def Performance_LTE_TA_siteid(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Yesterday"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_LTE_TA_period.set()
    else:
        try:
            int(message.text)
            await SampleSql.get_LTE_TA_yesterday(message.from_user.id, message.text)
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"Получил Performance : Timing Advance in "
                                                                     f"LTE: {message.text}")
        except:
            await message.answer('Неправильный ввод', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                       selective=False)
                                 .add(KeyboardButton("🔙Back"),
                                      KeyboardButton("🔝Main menu")))
            await bot.send_message(chat_id=Config_bot.admin_id,
                                   text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                        f"хочет получить Performance Timing Advance in LTE, но он ввёл неправильный"
                                        f" атрибут: {message.text}")


# @dp.message_handler(state=FSM.Performance_User_period)
async def Performance_User_period(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите статистику', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                     selective=False)
                             .add(KeyboardButton("PRB Utilization"))
                             .add(KeyboardButton("Number of users in a cell"))
                             .add(KeyboardButton("Timing Advance in LTE"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_PRB.set()
    elif message.text == 'Yesterday':
        await message.answer('Введите Site ID', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_User_siteid.set()


# @dp.message_handler(state=FSM.Performance_User_siteid)
async def Performance_User_siteid(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Yesterday"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_User_period.set()
    else:
        try:
            int(message.text)
            await SampleSql.get_LTE_User_yesterday(message.from_user.id, message.text)
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"Получил Performance Number of users in a "
                                                                     f"cell: {message.text}")
        except:
            await message.answer('Неправильный ввод', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                       selective=False)
                                 .add(KeyboardButton("🔙Back"),
                                      KeyboardButton("🔝Main menu")))
            await bot.send_message(chat_id=Config_bot.admin_id,
                                   text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                        f"хочет получить Performance Number of users in a cell, но он ввёл неправильный"
                                        f" атрибут: {message.text}")


# @dp.message_handler(state=FSM.Performance_PRB_period)
async def Performance_PRB_period(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите статистику', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                     selective=False)
                             .add(KeyboardButton("PRB Utilization"))
                             .add(KeyboardButton("Number of users in a cell"))
                             .add(KeyboardButton("Timing Advance in LTE"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_PRB.set()
        await FSM.Performance_PRB.set()
    elif message.text == 'Yesterday':
        await message.answer('Введите Site ID', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_PRB_siteid.set()


# @dp.message_handler(state=FSM.Performance_PRB_siteid)
async def Performance_PRB_siteid(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Yesterday"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_PRB_period.set()
    else:
        try:
            int(message.text)
            await SampleSql.get_PRB_Utill_yesterday(message.from_user.id, message.text)
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"Получил PRB Performance: {message.text}")
        except:
            await message.answer('Неправильный ввод', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                       selective=False)
                                 .add(KeyboardButton("🔙Back"),
                                      KeyboardButton("🔝Main menu")))
            await bot.send_message(chat_id=Config_bot.admin_id,
                                   text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                        f"хочет получить PRB Performance, но он ввёл неправильный "
                                        f"атрибут: {message.text}")


# @dp.message_handler(state=FSM.Performance_rtwp)
async def Performance_rtwp(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите технологию', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                     selective=False)
                             .add(KeyboardButton("UMTS"),
                                  KeyboardButton("LTE"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_Wireless.set()
    elif message.text == 'Mean RTWP':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Today"))
                             .add(KeyboardButton("Last 3 days"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_period.set()
    elif message.text == 'Propogation Delay':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Yesterday"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_UMTS_PD_period.set()
    elif message.text == 'CS Service Call Drop Rate':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Yesterday"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_UMTS_Call_drop_period.set()


# @dp.message_handler(state=FSM.Performance_UMTS_Call_drop_period)
async def Performance_UMTS_Call_drop_period(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите статистику', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                     selective=False)
                             .add(KeyboardButton("CS Service Call Drop Rate"))
                             .add(KeyboardButton("Mean RTWP"))
                             .add(KeyboardButton("Propogation Delay"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_rtwp.set()
    elif message.text == 'Yesterday':
        await message.answer('Введите Cell ID'
                             '\nНапример: 10141', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                   selective=False)
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_UMTS_Call_drop_cellid.set()


# @dp.message_handler(state=FSM.Performance_UMTS_Call_drop_cellid)
async def Performance_UMTS_Call_drop_cellid(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Yesterday"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_UMTS_Call_drop_period.set()
    else:
        # try:
        int(message.text)
        await SampleSql.get_Performance_UMTS_CS_Call_Drop(message.from_user.id, message.text)
        await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                 f"(ID: {message.from_user.id}) "
                                                                 f"Получил Performance UMTS Call Drop Rate"
                                                                 f": {message.text}")
    # except:
    #     await message.answer('Неправильный ввод', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
    #                                                                                selective=False)
    #                          .add(KeyboardButton("🔙Back"),
    #                               KeyboardButton("🔝Main menu")))
    #     await bot.send_message(chat_id=Config_bot.admin_id,
    #                            text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
    #                                 f"хочет получить Performance UMTS Call Drop Rate, но он ввёл неправильный"
    #                                 f" атрибут: {message.text}")


# @dp.message_handler(state=FSM.Performance_UMTS_PD_period)
async def Performance_UMTS_PD_period(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите статистику', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                     selective=False)
                             .add(KeyboardButton("CS Service Call Drop Rate"))
                             .add(KeyboardButton("Mean RTWP"))
                             .add(KeyboardButton("Propogation Delay"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_rtwp.set()
    elif message.text == 'Yesterday':
        await message.answer('Введите Cell ID'
                             '\nНапример: 10141', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                   selective=False)
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_UMTS_PD_cellid.set()


# @dp.message_handler(state=FSM.Performance_UMTS_PD_cellid)
async def Performance_UMTS_PD_cellid(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Yesterday"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_UMTS_PD_period.set()
    else:
        # try:
        int(message.text)
        await SampleSql.get_Performance_UMTS_Propagation_Delay(message.from_user.id, message.text)
        await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                 f"(ID: {message.from_user.id}) "
                                                                 f"Получил Performance Propogation Delay in UMTS"
                                                                 f": {message.text}")
    # except:
    #     await message.answer('Неправильный ввод', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
    #                                                                                selective=False)
    #                          .add(KeyboardButton("🔙Back"),
    #                               KeyboardButton("🔝Main menu")))
    #     await bot.send_message(chat_id=Config_bot.admin_id,
    #                            text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
    #                                 f"хочет получить Performance Propogation Delay in UMTS, но он ввёл неправильный"
    #                                 f" атрибут: {message.text}")


# @dp.message_handler(state=FSM.Performance_period)
async def Performance_period(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите статистику', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                     selective=False)
                             .add(KeyboardButton("CS Service Call Drop Rate"))
                             .add(KeyboardButton("Mean RTWP"))
                             .add(KeyboardButton("Propogation Delay"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_rtwp.set()
    elif message.text == 'Today':
        await message.answer('Введите Cell ID', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_rtwp_cellid.set()
    elif message.text == 'Last 3 days':
        await message.answer('Введите Cell ID', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_rtwp_yesterday_cellid.set()


# @dp.message_handler(state=FSM.Performance_rtwp_yesterday_cellid)
async def Performance_rtwp_yesterday_cellid(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Today"))
                             .add(KeyboardButton("Last 3 days"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_period.set()
    else:
        try:
            int(message.text)
            await SampleSql.get_rtwp_3days(message.from_user.id, message.text)
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"Получил RTWP Performance: {message.text}")
        except:
            await message.answer('Неправильный ввод', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                       selective=False)
                                 .add(KeyboardButton("🔙Back"),
                                      KeyboardButton("🔝Main menu")))
            await bot.send_message(chat_id=Config_bot.admin_id,
                                   text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                        f"хочет получить RTWP Performance, но он ввёл неправильный "
                                        f"атрибут: {message.text}")


# @dp.message_handler(state=FSM.Performance_rtwp_cellid)
async def Performance_rtwp_cellid(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer('Выберите период', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                 selective=False)
                             .add(KeyboardButton("Today"))
                             .add(KeyboardButton("Last 3 days"))
                             .add(KeyboardButton("🔙Back"),
                                  KeyboardButton("🔝Main menu")))
        await FSM.Performance_period.set()
    else:
        try:
            int(message.text)
            await SampleSql.get_rtwp_today_img(message.from_user.id, message.text)
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"Получил RTWP Performance: {message.text}")
        except:
            await message.answer('Неправильный ввод', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                       selective=False)
                                 .add(KeyboardButton("🔙Back"),
                                      KeyboardButton("🔝Main menu")))
            await bot.send_message(chat_id=Config_bot.admin_id,
                                   text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                        f"хочет получить RTWP Performance, но он ввёл неправильный "
                                        f"атрибут: {message.text}")


# @dp.message_handler(commands=['cellid'], state="*")
# @dp.message_handler(Text(equals='Cell ID', ignore_case=True), state="*")
async def process_cell_id(message: types.Message, state: FSMContext):
    if await SampleSql.get_user_confirmation(message.from_user.id) == 'YES':
        await message.answer("Выберите технологию", reply_markup=Keyboards.cell_kb)
        await FSM.Cell_id.set()
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'NO':
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать Бот (cell id)")
    #     await message.answer('Извините администратор Вас пока не подтвердил, ждите или свяжитесь с администраторм')
    # else:
    #     await message.answer('Вы не зарегистрированы.')


# @dp.message_handler(state=FSM.Cell_id)
async def process_get_cell_id(message: types.Message, state: FSMContext):
    if message.text == 'Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == 'GSM_Cell' or message.text == '/gsmcell':
        await message.answer("Введите GSM Cell ID\nНапример: 10001", reply_markup=Keyboards.btnmenuand_back)
        await FSM.GSM_cell_id.set()
    elif message.text == 'UMTS_Cell' or message.text == '/umtscell':
        await message.answer("Введите UMTS Cell ID\nНапример: 10001", reply_markup=Keyboards.btnmenuand_back)
        await FSM.UMTS_cell_id.set()
    elif message.text == 'LTE_Cell' or message.text == '/ltecell':
        await message.answer("Coming Soon", reply_markup=Keyboards.btnmenuand_back)
        await FSM.LTE_cell_id.set()


# @dp.message_handler(state=FSM.GSM_cell_id)
async def process_get_gsmcell_id(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer("Выберите технологию", reply_markup=Keyboards.cell_kb)
        await FSM.Cell_id.set()
    else:
        try:
            int(message.text)
            await message.answer(text=SampleSql.SampleSQL.get_raw_data_for_GSMCell(message.text),
                                 reply_markup=Keyboards.btnmenu)
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"ищет GSM Cell: {message.text}")
        except:
            await message.answer(text="Ввели неправильный атрибут", disable_web_page_preview=True,
                                 reply_markup=Keyboards.btnmenu)
            await bot.send_message(chat_id=Config_bot.admin_id,
                                   text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                        f"ищет GSM Cell, но он ввёл неправильный атрибут: {message.text}")


# @dp.message_handler(state=FSM.UMTS_cell_id)
async def process_get_umtscell_id(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer("Выберите технологию", reply_markup=Keyboards.cell_kb)
        await FSM.Cell_id.set()
    else:
        try:
            int(message.text)
            await message.answer(text=SampleSql.SampleSQL.get_raw_data_for_UMTSCell(message.text),
                                 reply_markup=Keyboards.btnmenu)
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"ищет UMTS Cell: {message.text}")
        except:
            await message.answer(text="Ввели неправильный атрибут", disable_web_page_preview=True,
                                 reply_markup=Keyboards.btnmenu)
            await bot.send_message(chat_id=Config_bot.admin_id,
                                   text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                        f"ищет UMTS Cell, но он ввёл неправильный атрибут: {message.text}")


# @dp.message_handler(state=FSM.LTE_cell_id)
async def process_get_ltecell_id(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == '🔙Back':
        await message.answer("Выберите технологию", reply_markup=Keyboards.cell_kb)
        await FSM.Cell_id.set()


# @dp.message_handler(commands=['pwr_calc'], state="*")
# @dp.message_handler(Text(equals='Power calculator', ignore_case=True), state="*")
async def process_power_calculator(message: types.Message, state: FSMContext):
    if await SampleSql.get_user_confirmation(message.from_user.id) == 'YES':
        await message.answer("Выберите действие.", reply_markup=Keyboards.Keyboard_Watt_to_dBm_to_Watt)
        await FSM.Power_Calculator.set()
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'NO':
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать Бот (Power Calculator)")
    #     await message.answer('Извините администратор Вас пока не подтвердил, ждите или свяжитесь с администраторм')
    # else:
    #     await message.answer('Вы не зарегистрированы.')


# @dp.message_handler(state=FSM.Power_Calculator)
async def process_get_Power_calculator(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    elif message.text == 'Watt to dBm':
        await message.answer("Введите число", reply_markup=Keyboards.btnmenuand_back)
        await FSM.Watt_to_dBm.set()
    elif message.text == 'dBm to Watt':
        await message.answer("Введите число", reply_markup=Keyboards.btnmenuand_back)
        await FSM.dBm_to_Watt.set()


# @dp.message_handler(state=FSM.Watt_to_dBm)
async def process_get_watt_to_dbm(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    if message.text == '🔙Back':
        await message.answer("Выберите действие.", reply_markup=Keyboards.Keyboard_Watt_to_dBm_to_Watt)
        await FSM.Power_Calculator.set()
    else:
        try:
            float(message.text)
            await message.reply(f'{message.text} Watt = {10 * math.log10(float(message.text) * 1000)} dBm')
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"перевёл {message.text} Watt на dBm")
        except:
            await message.answer("Неправильное число")


# @dp.message_handler(state=FSM.dBm_to_Watt)
async def process_get_dBm_to_watt(message: types.Message, state: FSMContext):
    if message.text == '🔝Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    if message.text == '🔙Back':
        await message.answer("Выберите действие.", reply_markup=Keyboards.Keyboard_Watt_to_dBm_to_Watt)
        await FSM.Power_Calculator.set()
    else:
        try:
            float(message.text)
            await message.reply(f'{message.text} dBm = {(math.pow(10, float(message.text) / 10)) / 1000} Watt')
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"перевёл {message.text} dBm на Watt")
        except:
            await message.answer("Неправильное число")


# @dp.message_handler(commands=['pwr_inf'], state="*")
# @dp.message_handler(Text(equals='Power Information', ignore_case=True), state="*")
async def process_power_information(message: types.Message, state: FSMContext):
    if await SampleSql.get_user_confirmation(message.from_user.id) == 'YES':
        await message.answer("Введите Site Id", reply_markup=Keyboards.btnmenu)
        await FSM.Power_Information.set()
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'NO':
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать Бот (Power Information)")
    #     await message.answer('Извините администратор Вас пока не подтвердил, ждите или свяжитесь с администраторм')
    # else:
    #     await message.answer('Вы не зарегистрированы.')


# @dp.message_handler(state=FSM.Power_Information)
async def process_get_power_information(message: types.Message, state: FSMContext):
    if message.text == 'Main menu':
        await message.answer('Выберите пункт', reply_markup=Keyboards.main_menu)
        await state.finish()
    else:
        await message.answer(text=SampleSql.SampleSQL.get_power_information(message.text),
                             disable_web_page_preview=True)
        await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                 f"(ID: {message.from_user.id}) "
                                                                 f"ищет  {message.text} dBm на Watt")


# @dp.message_handler(commands=['location'], state="*")
# @dp.message_handler(Text(equals='Send location', ignore_case=True), state="*")
async def process_location(message: types.Message, state: FSMContext):
    if await SampleSql.get_user_confirmation(message.from_user.id) == 'YES':
        await message.answer("Отправьте мне локацию и я вам отправлю ближайщие сайты.",
                             reply_markup=Keyboards.btnsend_location)
        await FSM.location.set()
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'NO':
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать Бот (Send Location)")
    #     await message.answer('Извините администратор Вас пока не подтвердил, ждите или свяжитесь с администраторм')
    # else:
    #     await message.answer('Вы не зарегистрированы.')


# @dp.message_handler(state=FSM.location, content_types=["location"])
async def process_get_location(message):
    b = 'https://yandex.uz/maps/10335/tashkent/?ll={message.location.longitude}%2C{message.location.latitude}&mode=' \
        'search&sll={message.location.longitude}%2C{message.location.latitude}&text={message.location.latitude}%2C{' \
        'message.location.longitude}&z=17.16"'
    tex_for_admin = f'''Пользователь {message.from_user.username}(ID: {message.from_user.id}) отправил локацию: <a href
    ='{b}'>Location</a>'''
    if message.location is not None:
        longitude = message.location.longitude
        latitude = message.location.latitude
        await message.answer(text=SampleSql.SampleSQL.get_nearest(longitude, latitude), disable_web_page_preview=True)
        await message.answer(text="***Топ 5 ближайших сайтов***")
        await message.answer(text=SampleSql.SampleSQL.get_top1_data(longitude, latitude), disable_web_page_preview=True)
        await message.answer(text=SampleSql.SampleSQL.get_top2_data(longitude, latitude), disable_web_page_preview=True)
        await message.answer(text=SampleSql.SampleSQL.get_top3_data(longitude, latitude), disable_web_page_preview=True)
        await message.answer(text=SampleSql.SampleSQL.get_top4_data(longitude, latitude), disable_web_page_preview=True)
        await message.answer(text=SampleSql.SampleSQL.get_top5_data(longitude, latitude), disable_web_page_preview=True)
        await bot.send_message(chat_id=Config_bot.admin_id, text=tex_for_admin, disable_web_page_preview=True)


# @dp.message_handler(commands=['mml_command'], state="*")
# @dp.message_handler(Text(equals='MML_Command', ignore_case=True), state="*")
async def process_mml_command(message: types.Message, state: FSMContext):
    if await SampleSql.get_user_confirmation(message.from_user.id) == 'YES':
        await message.answer('Здесь вы можете получить готовые MML скрипты для U2020'
                             '\n\nВыберите пункт', reply_markup=Keyboards.scripts)
        await FSM.power_change.set()
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'NO':
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать Бот (MML Command)")
    #     await message.answer('Извините администратор Вас пока не подтвердил, ждите или свяжитесь с администраторм')
    # else:
    #     await message.answer('Вы не зарегистрированы.')


# @dp.message_handler(state=FSM.power_change)
async def process_power_change(message: types.Message, state: FSMContext):
    if message.text == 'Power change':
        await message.answer('Здесь вы можете получить готовые MML скрипты для увеличения мощности.'
                             '\n\nВыберите технологию.', reply_markup=Keyboards.power_change_technology)
        await FSM.next()
    elif message.text == 'Cell deletion':
        await message.answer('Здесь вы можете получить готовые MML скрипты для удаления селлов.'
                             '\n\nВыберите технологию.', reply_markup=Keyboards.power_change_technology)
        await FSM.cell_deletion_technology.set()
    elif message.text == 'Block Board':
        await message.answer('Здесь вы можете получить готовые MML скрипты для блокировки RRU'
                             '\n\nНапишите Site ID'
                             '\nНапример: 1000', reply_markup=Keyboards.btnmenuand_back)
        await FSM.blk_brd.set()
    elif message.text == 'Ret Configuration':
        await message.answer('Здесь вы можете получить готовые MML скрипты для конфигурации RET моторов.'
                             '\n\nПожалуйста отправьте "Control Port Subrack No." и "Serial No."'
                             '\nВам необходимо собрать нужные поля в excell и скопировать сюда.'
                             '\n\nПример:'
                             '\n60  M1667G502AR49300r'
                             '\n60  M1667G502AS6538bL'
                             '\n60  M1667G502AT755bbR'
                             '\n61  M1667G402E3710bbR'
                             '\n61  M1667G402E29056bL'
                             '\n61  M1667G402E100090r'
                             '\n62  M1667G405K9660bbR'
                             '\n62  M1667G405K793580r'
                             '\n62  M1667G405K84235bL', reply_markup=Keyboards.btnmenuand_back)
        await FSM.MML_RET_config.set()
    else:
        await message.answer('Выберите пункт')


# @dp.message_handler(state=FSM.MML_RET_config)
async def MML_RET_config(message: types.Message, state: FSMContext):
    if message.text == "🔙Back":
        await message.answer('Здесь вы можете получить готовые MML скрипты для U2020'
                             '\n\nВыберите пункт', reply_markup=Keyboards.scripts)
        await FSM.power_change.set()
    else:
        try:
            await Functions.MML_RET_Configuration(message.from_user.id, message.text)
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"получил скрипт для конфигурации RET"
                                                                     f"{message.text}")
        except:
            await message.answer(f'Fail')


# @dp.message_handler(state=FSM.power_change_technology)
async def process_power_change_tech(message: types.Message, state: FSMContext):
    if message.text == 'GSM':
        await message.answer('Coming soon')
    elif message.text == 'UMTS':
        await message.answer('Для увеличения мощности необходимы следующие параметры:'
                             '\n\n-UMTS Cell ID'
                             '\n-UMTS ULOCELL'
                             '\n\nВведите UMTS Cell ID \nНапример: 10001', reply_markup=Keyboards.btnmenuand_back)
        await FSM.next()
    elif message.text == 'LTE':
        await message.answer('Coming soon')
    elif message.text == '🔙Back':
        await message.answer('Здесь вы можете получить готовые MML скрипты для U2020'
                             '\n\nВыберите пункт', reply_markup=Keyboards.scripts)
        await FSM.power_change.set()


# @dp.message_handler(state=FSM.power_change_UMTS_cell)
async def process_power_change_umts_ulocell(message: types.Message, state: FSMContext):
    if message.text == "🔙Back":
        await message.answer('Здесь вы можете получить готовые MML скрипты для увеличения мощности.'
                             '\n\nВыберите технологию.', reply_markup=Keyboards.power_change_technology)
        await FSM.power_change_technology.set()
    else:
        try:
            async with state.proxy() as data:
                data['UMTS_cell'] = int(message.text)
            await message.answer('Введите UMTS ULOCELL')
            await FSM.next()
        except:
            await message.answer('Ввели неправильный атрибут')


# @dp.message_handler(state=FSM.power_change_UMTS_ulocell)
async def process_power_change_umts(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['UMTS_ulocell'] = int(message.text)
        await message.answer("Введите сколько Watt \n\nПримечание: Единица измерения должно быть Watt")
        await FSM.next()
    except:
        await message.answer('Ввели неправильный атрибут')


# @dp.message_handler(state=FSM.power_change_UMTS_watt)
async def process_power_change_umts_watt(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['watt'] = float(message.text)
        watt = float(data['watt'])
        max_transmit_pwr = int(10 * math.log10(watt * 1000) * 10)
        pilot_pwr = int(10 * math.log10((watt / 10) * 1000) * 10)
        await message.answer(f'*****For RNC*****')
        await message.answer(f"MOD UPCPICHPWR:CELLID={data['UMTS_cell']},MAXPCPICHPOWER={(pilot_pwr + 80)},"
                             f'MINPCPICHPOWER={(pilot_pwr - 60)};'
                             f"\n\nMOD UCELL:CELLID={data['UMTS_cell']},MAXTXPOWER={max_transmit_pwr},PCPICHPOWER={pilot_pwr},"
                             f'DSSSMALLCOVMAXTXPOWER={max_transmit_pwr};'
                             f"\n\nMOD UPCPICHPWR:CELLID={data['UMTS_cell']},MAXPCPICHPOWER={(pilot_pwr + 10)},"
                             f'MINPCPICHPOWER={(pilot_pwr - 10)};')
        await message.answer(f'*****For NodeB*****')
        await message.answer(
            f"MOD ULOCELL: ULOCELLID={data['UMTS_ulocell']}, LOCELLTYPE=NORMAL_CELL,MAXPWR={max_transmit_pwr};")
        await message.answer(f'*****For NodeB LAMPSITE pRRU*****')
        await message.answer(f"MOD ULOCELL: ULOCELLID={data['UMTS_ulocell']}, LOCELLTYPE=MIXED_MULTIRRU_CELL, "
                             f'MAXPWR={max_transmit_pwr};')
        await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                 f"(ID: {message.from_user.id}) "
                                                                 f"получил скрипт для изменения мощности селла "
                                                                 f"ID: {data['UMTS_cell']} на {data['watt']} watt")
        await state.finish()
    except:
        await message.answer('Ввели неправильный атрибут')


# @dp.message_handler(state=FSM.cell_deletion_technology)
async def process_cell_deletion_technology(message: types.Message, state: FSMContext):
    if message.text == 'GSM':
        await message.answer('Coming soon')
    elif message.text == 'UMTS':
        await message.answer('Для удаления UMTS селла необходимы следующие параметры:'
                             '\n\n-UMTS Cell ID'
                             '\n-UMTS NodeB ID'
                             '\n-UMTS LAC'
                             '\n-UMTS ULOCELL'
                             '\n\nВведите UMTS Cell ID \nНапример: 10001', reply_markup=Keyboards.btnmenuand_back)
        await FSM.next()
    elif message.text == 'LTE':
        await message.answer('Coming soon')
    elif message.text == '🔙Back':
        await message.answer('Здесь вы можете получить готовые MML скрипты для U2020'
                             '\n\nВыберите пункт', reply_markup=Keyboards.scripts)
        await FSM.power_change.set()


# @dp.message_handler(state=FSM.cell_deletion_UMTS_cell)
async def process_cell_deletion_UMTS_cell(message: types.Message, state: FSMContext):
    if message.text == '🔙Back':
        await message.answer('Здесь вы можете получить готовые MML скрипты для удаления селлов.'
                             '\n\nВыберите технологию.', reply_markup=Keyboards.power_change_technology)
        await FSM.cell_deletion_technology.set()
    else:
        try:
            async with state.proxy() as data:
                data['UMTS_cell'] = int(message.text)
            await message.answer('Введите UMTS NodeB ID')
            await FSM.next()
        except:
            await message.answer('Ввели неправильный атрибут')


# @dp.message_handler(state=FSM.cell_deletion_UMTS_nodeb)
async def process_cell_deletion_UMTS_nodeb(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['UMTS_nodeb'] = int(message.text)
        await message.answer('Введите UMTS LAC')
        await FSM.next()
    except:
        await message.answer('Ввели неправильный атрибут')


# @dp.message_handler(state=FSM.cell_deletion_UMTS_lac)
async def process_cell_deletion_UMTS_lac(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['UMTS_lac'] = int(message.text)
        await message.answer('Введите UMTS Local cell')
        await FSM.next()
    except:
        await message.answer('Ввели неправильный атрибут')


# @dp.message_handler(state=FSM.cell_deletion_UMTS_ulocell)
async def process_cell_deletion_UMTS_locell(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['UMTS_locell'] = int(message.text)
        await message.answer(f'*****For RNC*****')
        await message.answer(f"RMV UCELL:CELLID={data['UMTS_cell']};"
                             f"\n\nRMV ULOCELL:IDTYPE=BYID,NODEBID={data['UMTS_nodeb']},LOCELL={data['UMTS_locell']};"
                             f"\n\nRMV USAC:CNOPINDEX=0,LAC={data['UMTS_lac']},SAC={data['UMTS_cell']};")
        await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                 f"(ID: {message.from_user.id}) "
                                                                 f"получил скрипт для удаления селла "
                                                                 f"ID: {data['UMTS_cell']}")
        await state.finish()
    except:
        await message.answer('Ввели неправильный атрибут')


# @dp.message_handler(state=FSM.power_change_technology)
async def process_blk_brd(message: types.Message, state: FSMContext):
    if message.text == '🔙Back':
        await message.answer('Здесь вы можете получить готовые MML скрипты для U2020'
                             '\n\nВыберите пункт', reply_markup=Keyboards.scripts)
        await FSM.power_change.set()
    else:
        await message.answer(f'Site ID: {message.text}')
        await SampleSql.get_blk_brd(message.from_user.id, message.text)
        await SampleSql.get_ubl_brd(message.from_user.id, message.text)
        await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                 f"(ID: {message.from_user.id}) "
                                                                 f"получил скрипт для блокировки RRU"
                                                                 f"\nID: {message.text}")
        await FSM.blk_brd.set()


# @dp.message_handler(commands=['Converter'], state="*")
# @dp.message_handler(Text(equals='Converter', ignore_case=True), state="*")
async def process_Converter(message: types.Message, state: FSMContext):
    if await SampleSql.get_user_confirmation(message.from_user.id) == 'YES':
        await message.answer('Здесь вы можете конвертировать формат Cell Id коммутатора.'
                             '\n\nВыберите источник',
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                             .add(KeyboardButton("USN(DSP MMCTX)"),
                                  KeyboardButton("SDR"))
                             .add(KeyboardButton("🔝Main menu")))
        await FSM.Site_ID_Converter.set()
    elif await SampleSql.get_user_confirmation(message.from_user.id) == 'NO':
        await bot.send_message(chat_id=Config_bot.admin_id,
                               text=f"Пользователь {message.from_user.username}(ID: {message.from_user.id}) "
                                    f"Пытается использовать Бот (Converter)")
    #     await message.answer('Извините администратор Вас пока не подтвердил, ждите или свяжитесь с администраторм')
    # else:
    #     await message.answer('Вы не зарегистрированы.')


# @dp.message_handler(state=FSM.Site_ID_Converter)
async def process_Site_ID_Converter(message: types.Message, state: FSMContext):
    if message.text == "USN(DSP MMCTX)":
        await message.answer(f'Выберите Технологию'
                             f'\n\nЕсли абонент сидит на LTE в результате MML будет поле "E-UTRAN cell global identity"'
                             f'\n\nЕсли абонент сидит на UMTS в результате MML будет поле "Service area of user"'
                             f'\n\nЕсли абонент сидит на GSM в результате MML будет поле "Cell Id"',
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                             .add(KeyboardButton("LTE"),
                                  KeyboardButton("UMTS"),
                                  KeyboardButton("GSM"))
                             .add(KeyboardButton("🔙Back"))
                             .add(KeyboardButton("🔝Main menu")))
        await FSM.technology.set()
    elif message.text == "SDR":
        await message.answer(f'Coming Soon',
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                             .add(KeyboardButton("🔝Main menu")))
        await state.finish()
    else:
        await message.answer(f'Выберите пункт')


# @dp.message_handler(state=FSM.technology)
async def process_technology(message: types.Message, state: FSMContext):
    if message.text == '🔙Back':
        await message.answer('Здесь вы можете конвертировать формат Cell Id коммутатора.'
                             '\n\nВыберите источник',
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                             .add(KeyboardButton("USN(DSP MMCTX)"),
                                  KeyboardButton("SDR"))
                             .add(KeyboardButton("🔝Main menu")))
        await FSM.Site_ID_Converter.set()
    elif message.text == "LTE":
        await message.answer(f'Напишите "E-UTRAN cell global identity"',
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                             .add(KeyboardButton("🔙Back"))
                             .add(KeyboardButton("🔝Main menu")))
        await FSM.USN.set()
    elif message.text == "UMTS":
        await message.answer(f'Напишите "Service area of user"',
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                             .add(KeyboardButton("🔙Back"))
                             .add(KeyboardButton("🔝Main menu")))
        await FSM.USN_UMTS.set()
    elif message.text == "GSM":
        await message.answer(f'Напишите "Cell Id"',
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                             .add(KeyboardButton("🔙Back"))
                             .add(KeyboardButton("🔝Main menu")))
        await FSM.USN_GSM.set()
    else:
        await message.answer(f'Выберите пункт')


# @dp.message_handler(state=FSM.USN_GSM)
async def process_USN_GSM(message: types.Message, state: FSMContext):
    if message.text == '🔙Back':
        await message.answer(f'Выберите Технологию'
                             f'\n\nЕсли абонент сидит на LTE в результате MML будет поле "E-UTRAN cell global identity"'
                             f'\n\nЕсли абонент сидит на UMTS в результате MML будет поле "Service area of user"'
                             f'\n\nЕсли абонент сидит на GSM в результате MML будет поле "Cell Id"',
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                             .add(KeyboardButton("LTE"),
                                  KeyboardButton("UMTS"),
                                  KeyboardButton("GSM"))
                             .add(KeyboardButton("🔙Back"))
                             .add(KeyboardButton("🔝Main menu")))
        await FSM.technology.set()
    else:
        try:
            a = f"{message.text}"
            Cell_Id = int((a.replace("0x", ""))[-4:], 16)
            await SampleSql.for_dsp_mmctx_gsm(message.from_user.id, Cell_Id, a)
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"Конвертировал Cell Id"
                                                                     f"\nID: {message.text}")
            await FSM.USN_GSM.set()
        except:
            await message.answer(f'Неправильный ввод данных',
                                 reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                                 .add(KeyboardButton("🔙Back"))
                                 .add(KeyboardButton("🔝Main menu")))
            await FSM.USN_UMTS.set()


# @dp.message_handler(state=FSM.USN_UMTS)
async def process_USN_UMTS(message: types.Message, state: FSMContext):
    if message.text == '🔙Back':
        await message.answer(f'Выберите Технологию'
                             f'\n\nЕсли абонент сидит на LTE в результате MML будет поле "E-UTRAN cell global identity"'
                             f'\n\nЕсли абонент сидит на UMTS в результате MML будет поле "Service area of user"'
                             f'\n\nЕсли абонент сидит на GSM в результате MML будет поле "Cell Id"',
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                             .add(KeyboardButton("LTE"),
                                  KeyboardButton("UMTS"),
                                  KeyboardButton("GSM"))
                             .add(KeyboardButton("🔙Back"))
                             .add(KeyboardButton("🔝Main menu")))
        await FSM.technology.set()
    else:
        try:
            a = f"{message.text}"
            Cell_Id = int((a.replace("43408", ""))[-4:], 16)
            await SampleSql.for_dsp_mmctx_umts(message.from_user.id, Cell_Id, a)
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"Service area of user"
                                                                     f"\nID: {message.text}")
            await FSM.USN_UMTS.set()
        except:
            await message.answer(f'Неправильный ввод данных',
                                 reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                                 .add(KeyboardButton("🔙Back"))
                                 .add(KeyboardButton("🔝Main menu")))
            await FSM.USN_UMTS.set()


# @dp.message_handler(state=FSM.USN)
async def process_USN_LTE(message: types.Message, state: FSMContext):
    if message.text == '🔙Back':
        await message.answer(f'Выберите Технологию'
                             f'\n\nЕсли абонент сидит на LTE в результате MML будет поле "E-UTRAN cell global identity"'
                             f'\n\nЕсли абонент сидит на UMTS в результате MML будет поле "Service area of user"'
                             f'\n\nЕсли абонент сидит на GSM в результате MML будет поле "Cell Id"',
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                             .add(KeyboardButton("LTE"),
                                  KeyboardButton("UMTS"),
                                  KeyboardButton("GSM"))
                             .add(KeyboardButton("🔙Back"))
                             .add(KeyboardButton("🔝Main menu")))
        await FSM.technology.set()
    else:
        try:
            a = f"{message.text}"
            EnodeB_ID = int((a.replace("43408", ""))[:5], 16)
            Cell_ID = int((a.replace("43408", ""))[-2:], 16)
            await SampleSql.for_dsp_mmctx(message.from_user.id, EnodeB_ID, Cell_ID, a)
            await bot.send_message(chat_id=Config_bot.admin_id, text=f"Пользователь {message.from_user.username}"
                                                                     f"(ID: {message.from_user.id}) "
                                                                     f"Конвертировал E-UTRAN cell global identity"
                                                                     f"\nID: {message.text}")
            await FSM.USN.set()
        except:
            await message.answer(f'Неправильный ввод данных',
                                 reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                                 .add(KeyboardButton("🔙Back"))
                                 .add(KeyboardButton("🔝Main menu")))
            await FSM.USN_UMTS.set()


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(process_site_id, commands=['siteid'], state="*")
    dp.register_message_handler(process_site_id, Text(equals='Site id', ignore_case=True), state="*")
    dp.register_message_handler(process_get_site_id, state=FSM.Site_id)
    dp.register_message_handler(process_cell_id, commands=['cellid'], state="*")
    dp.register_message_handler(process_cell_id, Text(equals='Cell ID', ignore_case=True), state="*")
    dp.register_message_handler(process_get_cell_id, state=FSM.Cell_id)
    dp.register_message_handler(process_get_gsmcell_id, state=FSM.GSM_cell_id)
    dp.register_message_handler(process_get_umtscell_id, state=FSM.UMTS_cell_id)
    dp.register_message_handler(process_get_ltecell_id, state=FSM.LTE_cell_id)
    dp.register_message_handler(process_power_calculator, commands=['pwr_calc'], state="*")
    dp.register_message_handler(process_power_calculator, Text(equals='Power calculator', ignore_case=True), state="*")
    dp.register_message_handler(process_get_location, state=FSM.location, content_types=["location"])
    dp.register_message_handler(process_get_Power_calculator, state=FSM.Power_Calculator)
    dp.register_message_handler(process_get_watt_to_dbm, state=FSM.Watt_to_dBm)
    dp.register_message_handler(process_get_dBm_to_watt, state=FSM.dBm_to_Watt)
    dp.register_message_handler(process_power_information, commands=['pwr_inf'], state="*")
    dp.register_message_handler(process_power_information, Text(equals='Power Information', ignore_case=True),
                                state="*")
    dp.register_message_handler(process_get_power_information, state=FSM.Power_Information)
    dp.register_message_handler(process_location, commands=['location'], state="*")
    dp.register_message_handler(process_location, Text(equals='Send location', ignore_case=True), state="*")
    dp.register_message_handler(process_get_location, state=FSM.Power_Information, content_types=["location"])
    dp.register_message_handler(process_mml_command, commands=['mml_command'], state="*")
    dp.register_message_handler(process_mml_command, Text(equals='MML Command', ignore_case=True), state="*")
    dp.register_message_handler(process_power_change, state=FSM.power_change)
    dp.register_message_handler(process_power_change_tech, state=FSM.power_change_technology)
    dp.register_message_handler(process_power_change_umts_ulocell, state=FSM.power_change_UMTS_cell)
    dp.register_message_handler(process_power_change_umts, state=FSM.power_change_UMTS_ulocell)
    dp.register_message_handler(process_power_change_umts_watt, state=FSM.power_change_UMTS_watt)
    dp.register_message_handler(process_cell_deletion_technology, state=FSM.cell_deletion_technology)
    dp.register_message_handler(process_cell_deletion_UMTS_cell, state=FSM.cell_deletion_UMTS_cell)
    dp.register_message_handler(process_cell_deletion_UMTS_nodeb, state=FSM.cell_deletion_UMTS_nodeb)
    dp.register_message_handler(process_cell_deletion_UMTS_lac, state=FSM.cell_deletion_UMTS_lac)
    dp.register_message_handler(process_cell_deletion_UMTS_locell, state=FSM.cell_deletion_UMTS_ulocell)
    dp.register_message_handler(process_blk_brd, state=FSM.blk_brd)
    dp.register_message_handler(process_Converter, commands=['Cell Converter'], state="*")
    dp.register_message_handler(process_Converter, Text(equals='Cell Converter', ignore_case=True), state="*")
    dp.register_message_handler(process_Site_ID_Converter, state=FSM.Site_ID_Converter)
    dp.register_message_handler(process_technology, state=FSM.technology)
    dp.register_message_handler(process_USN_LTE, state=FSM.USN)
    dp.register_message_handler(process_USN_UMTS, state=FSM.USN_UMTS)
    dp.register_message_handler(process_USN_GSM, state=FSM.USN_GSM)
    dp.register_message_handler(MML_RET_config, state=FSM.MML_RET_config)
    dp.register_message_handler(Performance, commands=['Performance'], state="*")
    dp.register_message_handler(Performance, Text(equals='Performance', ignore_case=True), state="*")
    dp.register_message_handler(Performance_dep, state=FSM.Performance)
    dp.register_message_handler(Performance_Wireless, state=FSM.Performance_Wireless)
    dp.register_message_handler(Performance_rtwp, state=FSM.Performance_rtwp)
    dp.register_message_handler(Performance_period, state=FSM.Performance_period)
    dp.register_message_handler(Performance_rtwp_cellid, state=FSM.Performance_rtwp_cellid)
    dp.register_message_handler(Performance_rtwp_yesterday_cellid, state=FSM.Performance_rtwp_yesterday_cellid)
    dp.register_message_handler(Performance_Core, state=FSM.Performance_Core)
    dp.register_message_handler(Performance_billing_reject, state=FSM.Performance_billing_reject)
    dp.register_message_handler(Performance_billing_reject_period, state=FSM.Performance_billing_reject_period)
    dp.register_message_handler(Performance_billing_reject_incoming, state=FSM.Performance_billing_reject_incoming)
    dp.register_message_handler(Performance_PRB, state=FSM.Performance_PRB)
    dp.register_message_handler(Performance_PRB_period, state=FSM.Performance_PRB_period)
    dp.register_message_handler(Performance_PRB_siteid, state=FSM.Performance_PRB_siteid)
    dp.register_message_handler(Performance_User_period, state=FSM.Performance_User_period)
    dp.register_message_handler(Performance_User_siteid, state=FSM.Performance_User_siteid)
    dp.register_message_handler(Performance_LTE_TA_period, state=FSM.Performance_LTE_TA_period)
    dp.register_message_handler(Performance_LTE_TA_siteid, state=FSM.Performance_LTE_TA_siteid)
    dp.register_message_handler(Performance_UMTS_PD_period, state=FSM.Performance_UMTS_PD_period)
    dp.register_message_handler(Performance_UMTS_PD_cellid, state=FSM.Performance_UMTS_PD_cellid)
    dp.register_message_handler(Performance_UMTS_Call_drop_period, state=FSM.Performance_UMTS_Call_drop_period)
    dp.register_message_handler(Performance_UMTS_Call_drop_cellid, state=FSM.Performance_UMTS_Call_drop_cellid)