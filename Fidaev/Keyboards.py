from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = types.ReplyKeyboardRemove(selective=False)
registration = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(KeyboardButton("Регистрация")) \
    .add(KeyboardButton("Main menu"))

configuration = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(KeyboardButton("BSC"),
                                                                                       KeyboardButton("RNC")) \
    .add(KeyboardButton("Main menu"))

for_test_menu = (ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
                 .add(KeyboardButton("DSP MMCTX"), KeyboardButton("Active Alarms"))
                 .add(KeyboardButton("Get MML"))
                 .add(KeyboardButton("🔝Main menu")))

mml_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(KeyboardButton("DSP ULOCELL"),
                                                                                  KeyboardButton("DSP CELL")) \
    .add(KeyboardButton("DSP LICRATE")) \
    .add(KeyboardButton("🔝Main menu"), KeyboardButton("🔙Back"))

send_contact = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(KeyboardButton("Отправить контакт"
                                                                                                     ,
                                                                                                     request_contact=True))
main_menu = (ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
             .add(KeyboardButton("Site ID"),
                  KeyboardButton("Performance"))
             .add(KeyboardButton("Cell Converter"),
                  KeyboardButton("Send location"))
             .add(KeyboardButton("MML Command"),
                  KeyboardButton("Power calculator"))
             .add(KeyboardButton("Configuration"),
                  KeyboardButton("For tests"))
             .add(KeyboardButton("Ringit Converter")))
verification = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(KeyboardButton("YES"),
                                                                                      KeyboardButton("NO"))
scripts = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(KeyboardButton("Power change"),
                                                                                 KeyboardButton("Cell deletion")) \
    .add(KeyboardButton("Block Board"),
         KeyboardButton("Ret Configuration")) \
    .add(KeyboardButton("🔝Main menu"))
power_change_technology = (ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(KeyboardButton("GSM"),
                                                                                                  KeyboardButton(
                                                                                                      "UMTS"),
                                                                                                  KeyboardButton("LTE")) \
                           .add(KeyboardButton("🔝Main menu"))
                           .add(KeyboardButton("🔙Back")))

btnmenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(KeyboardButton("🔝Main menu"))
btnmenuand_back = (ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(KeyboardButton("🔝Main menu"))
                   .add(KeyboardButton("🔙Back")))
btnsend_location = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(
    KeyboardButton("Send location", request_location=True)).add(KeyboardButton("🔝Main menu"))

btnSiteID = KeyboardButton("SiteID")
btnCellID = KeyboardButton("CellID")
btn_Power_calculator = KeyboardButton('Power calculator')
btnsendlocation = KeyboardButton("Send location", request_location=True)
btn_Power_information = KeyboardButton("Power Information")
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btnSiteID, btnCellID).add(
    btn_Power_calculator, btn_Power_information).add(btnsendlocation)

btnGSMCellID = KeyboardButton("GSM_Cell")
btnUMTSCellID = KeyboardButton("UMTS_Cell")
btnLTECellID = KeyboardButton("LTE_Cell")
btnBack = KeyboardButton("Back")
cell_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btnGSMCellID, btnUMTSCellID,
                                                                                 btnLTECellID).add(
    KeyboardButton("🔝Main menu"))

Button_back = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btnBack)

# btnsendcontact = KeyboardButton("Send Contact", request_contact=True)


sendlocation = ReplyKeyboardMarkup(resize_keyboard=True, selective=False).add(btnsendlocation, btnBack)

btn_Watt_to_dBm = KeyboardButton("Watt to dBm")
btn_dBm_to_Watt = KeyboardButton("dBm to Watt")
btn_Power_calculator = KeyboardButton('Power calculator')
Keyboard_Watt_to_dBm_to_Watt = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btn_Watt_to_dBm,
                                                                                                      btn_dBm_to_Watt).add(
    KeyboardButton("🔝Main menu"))
