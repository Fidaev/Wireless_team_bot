import datetime
import psycopg2
# import pypyodbc
import sqlite3
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
import Config_bot
import Keyboards
from Create_bot import bot
import matplotlib.pyplot as plt
import os

path = os.getcwd()


def sql_start():
    global base, cur
    base = sqlite3.connect(fr'{path}/BSC&RNC_bot.db')
    cur = base.cursor()
    if base:
        print('Data base connected')
    base.execute(
        'CREATE TABLE IF NOT EXISTS user_info(User_id TEXT PRIMARY KEY, User_name TEXT, Contact TEXT, Confirmation '
        'TEXT)')
    base.commit()


def postgresql_connection():
    global connection
    host1 = "localhost"
    pguser1 = "maintenance"
    password1 = "parolotdb"
    db_name1 = "maintenance"

    connection = psycopg2.connect(
        host=host1,
        user=pguser1,
        password=password1,
        database=db_name1
    )
    connection.autocommit = True


async def get_Average_Subsystem_CPU_Usage(chat_id):
    postgresql_connection()
    RNC_name = ["Tash_RNC1", "Tash_RNC2", "Nam_RNC1", "GUL_RNC1", "Fer_RNC1", "And_RNC1"]
    UUP_alarm = []
    UCP_alarm = []
    date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    for RNC in RNC_name:
        time_line = []
        UUP = []
        UCP = []
        with connection.cursor() as cursor:
            cursor.execute(f"""select "Result_Time", round((avg("Avg_Subsys_CPU_Usage"::numeric)),2)
                        from "Performance_RNC_Subsystem_CPU_Usage"
                        where ("Object_Name" like '{RNC}%=UUP') and "Result_Time" like '{date}%'
                        group by "Result_Time"
                        order by "Result_Time" """)
            for result in cursor.fetchall():
                time = str.format(result[0]).replace(f"2023-", f"")
                time_line.append(time)
                UUP.append(float(result[1]))
                if result[1] >= 50:
                    UUP_alarm.append(f"{RNC}")
            cursor.execute(f"""select "Result_Time", round((avg("Avg_Subsys_CPU_Usage"::numeric)),2)
                        from "Performance_RNC_Subsystem_CPU_Usage"
                        where ("Object_Name" like '{RNC}%=UCP') and "Result_Time" like '{date}%'
                        group by "Result_Time"
                        order by "Result_Time" """)
            for result in cursor.fetchall():
                UCP.append(float(result[1]))
                if result[1] >= 50:
                    UCP_alarm.append(f"{RNC}")
        if len(UUP):
            fig = plt.figure()
            fig.set_figheight(10)
            fig.set_figwidth(10)
            plt.title(f"KPI: Average Subsystem CPU Usage. \nDate: {date}.\nRNC name: {RNC}", color="black")
            plt.ylabel("Average Subsystem CPU Usage", color='black')
            plt.xticks(rotation=90)
            plt.plot(time_line, UUP, label="Subsystem Type=UUP", color='blue', linewidth=2, marker="o")
            plt.plot(time_line, UCP, label="Subsystem Type=UСP", color='red', linewidth=2, marker="o")
            plt.legend()
            plt.grid()
            ax = plt.gca()
            ax.set_facecolor('white')
            file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            plt.savefig(fr"{path}/Files/{RNC}_{file_name}.png")
            photo = InputFile(f"{path}/Files/{RNC}_{file_name}.png")
            await bot.send_photo(chat_id=chat_id, photo=photo)
            plt.close()
        else:
            await bot.send_message(chat_id=chat_id, text=f'Ошибка')
    if len(UUP_alarm) or len(UCP_alarm):
        str_UUP = str(list(set(UUP_alarm))).replace("['", "").replace("']", "").replace("', '", "\n") \
            .replace("[]", "Не зафиксирован")
        str_UCP = str(list(set(UCP_alarm))).replace("['", "").replace("']", "").replace("', '", "\n") \
            .replace("[]", "Не зафиксирован")
        alarms = f"***Subsystem Type=UUP зафиксирован более 50% на следующих контроллерах***" \
                 f"\n{str_UUP}" \
                 f"\n\n***Subsystem Type=UCP зафиксирован более 50% на следующих контроллерах***" \
                 f"\n{str_UCP}"
    else:
        alarms = f"На контроллерах Subsystem Type=UUP и Subsystem Type=UСP не зафиксирован более 50%"
    await bot.send_message(chat_id=chat_id, text=alarms)


async def get_Performance_UMTS_CS_Call_Drop(chat_id, cellid):
    postgresql_connection()
    x = []
    y = []
    date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT "Result_Time", "CS_RABs_Abnormally_Release", "CS_RABs_Normally_Release" 
        FROM "Performance_UMTS_CS_Call_Drop" 
        WHERE "Object_Name" like '%CellID={cellid}%' and "Result_Time" like '{date}%' 
        ORDER by "Result_Time" """)
        for result in cursor.fetchall():
            if int(result[2]) != 0:
                cs_call_drop = int(result[1]) / (int(result[1]) + int(result[2])) * 100
                x.append(round(cs_call_drop, 2))
            else:
                x.append(int(result[2]))
            a = str.format(result[0]).replace(f"{date} ", "")
            y.append(a)
    if len(x):
        fig = plt.figure(facecolor="white")
        plt.title(f"Cell ID: {cellid} \nDate: {date}", color="blue")
        plt.ylabel("CS Call Drop", color='blue')
        plt.xlabel("Time", color='blue')
        plt.xticks(rotation=90)
        plt.plot(y, x, label="CS Call Drop", color='blue', linewidth=2, marker="o")
        plt.legend()
        plt.grid()
        ax = plt.gca()
        ax.set_facecolor('white')
        fig.set_figheight(9)
        fig.set_figwidth(10)
        file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        plt.savefig(fr"{path}/Files/{file_name}.png")

        photo = InputFile(fr"{path}/Files/{file_name}.png")
        await bot.send_photo(chat_id=chat_id, photo=photo)
        plt.close()
    else:
        await bot.send_message(chat_id=chat_id, text=f'Такой селл нет в БД или ввели неправильный атрибут')


async def get_Performance_UMTS_Propagation_Delay(chat_id, cellid):
    postgresql_connection()
    date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    result = []
    TA = ["0-156m", "156-390m", "390-624m", "624-858m", "858-1092m", "1092-1326m", "1326-2262m",
          "2262-3666m", "3666-6006m", "6006-8349m", "8346-13026m", "13026m+"]
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT sum("VS_TP_UE_0"::numeric), sum("VS_TP_UE_1"::numeric), sum("VS_TP_UE_2"::numeric), 
        sum("VS_TP_UE_3"::numeric), sum("VS_TP_UE_4"::numeric), sum("VS_TP_UE_5"::numeric), 
        sum("VS_TP_UE_6_9"::numeric), sum("VS_TP_UE_10_15"::numeric), sum("VS_TP_UE_16_25"::numeric), 
        sum("VS_TP_UE_26_35"::numeric), sum("VS_TP_UE_36_55"::numeric), sum("VS_TP_UE_More55"::numeric) 
        FROM "Performance_UMTS_Propogation_delay" 
        WHERE "Object_Name" like '%CellID={cellid},%' and "Result_Time" like '{date}%'""")
        for result2 in cursor.fetchall():
            result.append(int(result2[0]))
            result.append(int(result2[1]))
            result.append(int(result2[2]))
            result.append(int(result2[3]))
            result.append(int(result2[4]))
            result.append(int(result2[5]))
            result.append(int(result2[6]))
            result.append(int(result2[7]))
            result.append(int(result2[8]))
            result.append(int(result2[9]))
            result.append(int(result2[10]))
            result.append(int(result2[11]))
    if len(result):
        fig = plt.figure(facecolor="white")
        plt.title(f"KPI: Propogation Delay in UMTS \nCell ID: {cellid}, \nDate: {date}", color="black")
        plt.ylabel("Number of RRC Connection Establishment Requests", color='black', fontsize=7)
        plt.xlabel("Meters", color='black', fontsize=7)
        plt.xticks(color='black', rotation=90)
        plt.yticks(color='black')
        plt.bar(TA, result, label="Propogation Delay in UMTS", color='red', width=0.5)
        plt.legend()
        plt.grid(color='grey', linewidth=1, axis='y')
        ax = plt.gca()
        ax.set_facecolor('white')
        plt.tick_params(pad=0, labelsize=7)
        fig.set_figheight(10)
        fig.set_figwidth(10)
        file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        plt.savefig(fr"{path}/Files/{cellid}_{file_name}.png")
        plt.close()
        photo = InputFile(fr"{path}/Files/{cellid}_{file_name}.png")
        await bot.send_photo(chat_id=chat_id, photo=photo)
    else:
        await bot.send_message(chat_id=chat_id, text=f'Такой сайт нет в БД или ввели неправильный атрибут')


async def get_LTE_TA_yesterday(chat_id, site_id):
    postgresql_connection()
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT "LocalCellID" FROM "RAN_Report_LTE_Cell" WHERE "LTENEName" like '%({site_id})' 
            ORDER BY "LocalCellID" """)
        for result in cursor.fetchall():
            lc = result[0]
            date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            result = []
            TA = ["0-156m", "156-234m", "234-546m", "546-1014m", "1014-1950m", "1950-3510m", "3510-6630m",
                  "6630-14430m", "14430-30030m", "30030-53430m", "53430-76830m", "76830m+"]
            with connection.cursor() as cursor2:
                cursor2.execute(f"""SELECT sum("L_RA_TA_UE_Index0"::numeric) as Index0,
                sum("L_RA_TA_UE_Index1"::numeric) as Index1, 
                sum("L_RA_TA_UE_Index2"::numeric) as Index2, 
                sum("L_RA_TA_UE_Index3"::numeric) as Index3, 
                sum("L_RA_TA_UE_Index4"::numeric) as Index4, 
                sum("L_RA_TA_UE_Index5"::numeric) as Index5, 
                sum("L_RA_TA_UE_Index6"::numeric) as Index6, 
                sum("L_RA_TA_UE_Index7"::numeric) as Index7, 
                sum("L_RA_TA_UE_Index8"::numeric) as Index8, 
                sum("L_RA_TA_UE_Index9"::numeric) as Index9, 
                sum("L_RA_TA_UE_Index10"::numeric) as Index10, 
                sum("L_RA_TA_UE_Index11"::numeric) as Index11
                FROM "Performance_LTE_TA" 
                WHERE "Object_Name" like '%{site_id})%Local Cell ID={lc}%' and "Result_Time" like '{date}%' 
                """)
                for result2 in cursor2.fetchall():
                    result.append(int(result2[0]))
                    result.append(int(result2[1]))
                    result.append(int(result2[2]))
                    result.append(int(result2[3]))
                    result.append(int(result2[4]))
                    result.append(int(result2[5]))
                    result.append(int(result2[6]))
                    result.append(int(result2[7]))
                    result.append(int(result2[8]))
                    result.append(int(result2[9]))
                    result.append(int(result2[10]))
                    result.append(int(result2[11]))
            if len(result):
                fig = plt.figure(facecolor="white")
                plt.title(f"KPI: Timing Advance in LTE \nSite Name: {lc} \nSite ID: {site_id} \nLocal "
                          f"Cell ID: {lc}", color="black")
                plt.ylabel("initiated random access procedure", color='black', fontsize=7)
                plt.xlabel("Meters", color='black', fontsize=7)
                plt.xticks(color='black', rotation=90)
                plt.yticks(color='black')
                plt.bar(TA, result, label="Timing Advance in LTE", color='red', width=0.5)
                plt.legend()
                plt.grid(color='grey', linewidth=1, axis='y')
                ax = plt.gca()
                ax.set_facecolor('white')
                plt.tick_params(pad=0, labelsize=7)
                fig.set_figheight(10)
                fig.set_figwidth(10)
                file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                plt.savefig(fr"{path}/Files/{site_id}_{lc}_{file_name}.png")
                plt.close()
                photo = InputFile(fr"{path}/Files/{site_id}_{lc}_{file_name}.png")
                await bot.send_photo(chat_id=chat_id, photo=photo)
            else:
                await bot.send_message(chat_id=chat_id, text=f'Такой сайт нет в БД или ввели неправильный атрибут')


async def get_LTE_User_yesterday(chat_id, site_id):
    postgresql_connection()
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT "LocalCellID" FROM "RAN_Report_LTE_Cell" WHERE "LTENEName" like '%({site_id})' 
        ORDER BY "LocalCellID" """)
        for result in cursor.fetchall():
            lc = result[0]
            date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            x = []
            time = []
            z = []
            with connection.cursor() as cursor2:
                cursor2.execute(f"""SELECT "Result_Time", "Avg_user_cell", "Max_user_cell" 
                FROM "Performance_LTE_number_of_users_in_a_cell" 
                WHERE "Object_Name" like '%{site_id})%Local Cell ID={lc},%' AND "Result_Time" like '{date}%' 
                ORDER by "Result_Time" 
                """)
                for result2 in cursor2.fetchall():
                    a = str.format(result2[0]).replace(f"2023-", "")
                    time.append(a)
                    x.append(result2[1])
                    z.append(result2[2])
            if len(x):
                fig = plt.figure()
                fig.set_figheight(10)
                fig.set_figwidth(10)
                plt.title(f"KPI: Number of users in a cell \nSite Name: {lc} \nSite ID: {site_id} \nLocal "
                          f"Cell ID: {lc}", color="black")
                plt.ylabel("Number of users in a cell", color='black')
                plt.xticks(rotation=90)
                plt.plot(time, x, label="Average number of users in a cell", color='blue', linewidth=2, marker="o")
                plt.plot(time, z, label="Maximum number of users in a cell", color='red', linewidth=2, marker="o")
                plt.legend()
                plt.grid()
                ax = plt.gca()
                ax.set_facecolor('white')
                file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                plt.savefig(fr"{path}/Files/{site_id}_{lc}_{file_name}.png")
                plt.close()
                photo = InputFile(fr"{path}/Files/{site_id}_{lc}_{file_name}.png")
                await bot.send_photo(chat_id=chat_id, photo=photo)
            else:
                await bot.send_message(chat_id=chat_id, text=f'Такой сайт нет в БД или ввели неправильный атрибут')


async def get_PRB_Utill_yesterday(chat_id, site_id):
    postgresql_connection()
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT "LocalCellID" FROM "RAN_Report_LTE_Cell" WHERE "LTENEName" like '%({site_id})' 
        ORDER BY "LocalCellID" """)
        for result in cursor.fetchall():
            lc = result[0]
            date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            x = []
            y = []
            z = []
            with connection.cursor() as cursor2:
                cursor2.execute(f"""SELECT "Result_Time", 
                round(("Average_number_of_used_PDSCH_PRBs"/"Number_of_available_downlink_PRBs"*100)::numeric, 2) 
                as "DL PRB Utilization", 
                round(("Average_number_of_used_uplink_PRBs"/"Number_of_available_uplink_PRBs"*100)::numeric, 2) 
                as "UL PRB Utilization" 
                FROM "Performance_LTE_PRB_Utilization" 
                WHERE "Object_Name" like '%({site_id})%Local Cell ID={lc},%' AND "Result_Time" like '{date}%' 
                ORDER by "Result_Time" """)
                for result2 in cursor2.fetchall():
                    a = str.format(result2[0]).replace(f"2023-", "")
                    y.append(a)
                    x.append(result2[1])
                    z.append(result2[2])
            if len(x):
                fig = plt.figure()
                fig.set_figheight(10)
                fig.set_figwidth(10)
                plt.title(f"KPI: PRB Utilization Rate \nSite ID: {site_id} \nLocal Cell ID: {lc}", color="black")
                plt.ylabel("PRB Utilization Rate", color='black')
                plt.xticks(rotation=90)
                plt.plot(y, x, label="DL PRB Utilization Rate", color='blue', linewidth=2, marker="o")
                plt.plot(y, z, label="UL PRB Utilization Rate", color='red', linewidth=2, marker="o")
                plt.legend()
                plt.grid()
                ax = plt.gca()
                ax.set_facecolor('white')
                file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                plt.savefig(fr"{path}/Files/{site_id}_{lc}_{file_name}.png")
                plt.close()
                photo = InputFile(fr"{path}/Files/{site_id}_{lc}_{file_name}.png")
                await bot.send_photo(chat_id=chat_id, photo=photo)
            else:
                await bot.send_message(chat_id=chat_id, text=f'Такой сайт нет в БД или ввели неправильный атрибут')
    connection.close()


async def get_rtwp_3days(chat_id, Cellid):
    postgresql_connection()
    x = []
    y = []
    date = datetime.date.today().strftime('%Y-%m-%d')
    date2 = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    date3 = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT replace((replace((replace("Result_Time", ':15', ':00')),':30',':00')), ':45', ':00') 
        as Time, ROUND((AVG("MeanRTWP"::numeric)),2)
        FROM "Performance_UMTS_RTWP" 
        WHERE "Object_Name" like '%CellID={Cellid}%' AND ("Result_Time" like '{date}%' or "Result_Time" like 
        '{date2}%' or "Result_Time" like '{date3}%') 
        GROUP by Time""")
        for result in cursor.fetchall():
            a = str.format(result[0]).replace(f"2023-", "")
            y.append(a)
            x.append(result[1])
    if len(x):
        fig = plt.figure()
        fig.set_figheight(10)
        fig.set_figwidth(10)
        plt.title(f"Cell ID: {Cellid} \nLast 3 days", color="black")
        plt.ylabel("RTWP", color='black')
        plt.xticks(rotation=90)
        plt.plot(y, x, label="MEAN RTWP", color='blue', linewidth=2, marker="o")
        plt.legend()
        plt.grid()
        ax = plt.gca()
        ax.set_facecolor('white')
        file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        plt.savefig(fr"{path}/Files/{file_name}.png")

        photo = InputFile(fr"{path}/Files/{file_name}.png")
        await bot.send_photo(chat_id=chat_id, photo=photo)
        plt.close()
        plt.show()
    else:
        await bot.send_message(chat_id=chat_id, text=f'Такой селл нет в БД или ввели неправильный атрибут')


async def get_core_Billing_reject_3days(SRV, chat_id):
    postgresql_connection()
    try:
        time_line1 = []
        time_line2 = []
        Fer_MSX = []
        Tash_MSX = []
        date = datetime.date.today().strftime('%Y-%m-%d')
        date2 = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        date3 = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
        key = SRV
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT replace((replace((replace("Result_Time", ':15', ':00')),':30',':00')), ':45',
            ':00') as Time, "Object_Name", sum("Billing_rejects"::integer) FROM "Performance_Core_Billing_Reject" WHERE 
            "Object_Name" like '%SRVKEY={SRV}' AND ("Result_Time" like '{date}%' or "Result_Time" like '{date2}%' or 
            "Result_Time" like '{date3}%') GROUP by Time, "Object_Name" Order by Time""")
            for result in cursor.fetchall():
                if f"Fer_MSX_H/ServiceKey:SRVKEY={SRV}" in result[1]:
                    time = str.format(result[0]).replace(f"2023-", f"")
                    time_line1.append(time)
                    Fer_MSX.append(int(result[2]))

                elif f"Tas_MSX_H/ServiceKey:SRVKEY={SRV}" in result[1]:
                    time = str.format(result[0]).replace(f"2022-", f"")
                    time_line2.append(time)
                    Tash_MSX.append(int(result[2]))

            if key == "101":
                if len(time_line1):
                    fig = plt.figure()
                    fig.set_figheight(10)
                    fig.set_figwidth(10)

                    plt.subplot(3, 1, 1)
                    plt.title(f"Отказы от биллинга за 3 дня: Исходящий Tas_MSX_H", color="black")
                    plt.ylabel("times", color='black')
                    plt.xticks(rotation=90)
                    plt.plot(time_line2, Tash_MSX, label="Исходящий Отказы: Tas_MSX_H", color='red', linewidth=2,
                             marker="o")
                    plt.grid()
                    ax = plt.gca()
                    ax.set_facecolor('white')

                    plt.subplot(2, 1, 2)
                    plt.title(f"Отказы от биллинга за 3 дня: Исходящий Fer_MSX_H", color="black")
                    plt.ylabel("times", color='black')
                    plt.xticks(rotation=90)
                    plt.plot(time_line1, Fer_MSX, label="Исходящий Отказы: Fer_MSX_H", color='blue', linewidth=2,
                             marker="o")
                    plt.grid()
                    ax = plt.gca()
                    ax.set_facecolor('white')
                    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                    plt.savefig(f"Files/{file_name}.png")
                    plt.close()
                    photo = InputFile(f"Files/{file_name}.png")
                    await bot.send_photo(chat_id=chat_id, photo=photo)

                else:
                    await bot.send_message(chat_id=chat_id, text=f'Такой селл нет в БД или ввели неправильный атрибут')
            else:
                if len(time_line1):
                    fig = plt.figure()
                    fig.set_figheight(10)
                    fig.set_figwidth(10)

                    plt.subplot(3, 1, 1)
                    plt.title(f"Отказы от биллинга за 3 дня: Входящий Tas_MSX_H", color="black")
                    plt.ylabel("times", color='black')
                    plt.xticks(rotation=90)
                    plt.plot(time_line2, Tash_MSX, label="Входящий Отказы: Tas_MSX_H", color='red', linewidth=2,
                             marker="o")
                    plt.grid()
                    ax = plt.gca()
                    ax.set_facecolor('white')

                    plt.subplot(2, 1, 2)
                    plt.title(f"Отказы от биллинга за 3 дня: Входящий Fer_MSX_H", color="black")
                    plt.ylabel("times", color='black')
                    plt.xticks(rotation=90)
                    plt.plot(time_line1, Fer_MSX, label="Входящий Отказы: Fer_MSX_H", color='blue', linewidth=2,
                             marker="o")
                    plt.grid()
                    ax = plt.gca()
                    ax.set_facecolor('white')
                    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                    plt.savefig(fr"{path}/Files/{file_name}.png")
                    plt.close()
                    photo = InputFile(fr"{path}/Files/{file_name}.png")
                    await bot.send_photo(chat_id=chat_id, photo=photo)
                else:
                    await bot.send_message(chat_id=chat_id, text=f'Такой селл нет в БД или ввели неправильный атрибут')
    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if connection:
            connection.close()


async def get_core_incoming_today(chat_id):
    postgresql_connection()
    try:
        time_line1 = []
        time_line2 = []
        Fer_MSX = []
        Tash_MSX = []
        date = datetime.date.today().strftime('%Y-%m-%d')
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT replace((replace((replace("Result_Time", ':15', ':00')),':30',':00')), ':45',
            ':00') as Time, "Object_Name", sum("Billing_rejects"::integer) FROM "Performance_Core_Billing_Reject" WHERE 
            "Object_Name" like '%102' and "Result_Time" like '{date}%' GROUP by Time, "Object_Name" 
            Order by Time""")
            for result in cursor.fetchall():
                if "Fer_MSX_H/ServiceKey:SRVKEY=102" in result[1]:
                    time = str.format(result[0]).replace(f"{date} ", "")
                    time_line1.append(time)
                    Fer_MSX.append(int(result[2]))

                elif "Tas_MSX_H/ServiceKey:SRVKEY=102" in result[1]:
                    time = str.format(result[0]).replace(f"{date} ", "")
                    time_line2.append(time)
                    Tash_MSX.append(int(result[2]))
            if len(time_line1):
                plt.subplot(3, 1, 1)
                plt.title(f"Отказы от биллинга: Входящий Tas_MSX_H", color="black")
                plt.ylabel("times", color='black')
                plt.xticks(rotation=45)
                plt.plot(time_line2, Tash_MSX, label="Входящий Отказы: Tas_MSX_H", color='red', linewidth=2, marker="o")
                plt.grid()
                ax = plt.gca()
                ax.set_facecolor('white')

                plt.subplot(2, 1, 2)
                plt.title(f"Отказы от биллинга: Входящий Fer_MSX_H", color="black")
                plt.ylabel("times", color='black')
                plt.xticks(rotation=45)
                plt.plot(time_line1, Fer_MSX, label="Входящий Отказы: Fer_MSX_H", color='blue', linewidth=2, marker="o")
                plt.grid()
                ax = plt.gca()
                ax.set_facecolor('white')
                file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                plt.savefig(fr"{path}/Files/{file_name}.png")
                plt.close()
                photo = InputFile(fr"{path}/Files/{file_name}.png")
                await bot.send_photo(chat_id=chat_id, photo=photo)
            else:
                await bot.send_message(chat_id=chat_id, text=f'Такой селл нет в БД или ввели неправильный атрибут')
    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if connection:
            connection.close()


async def get_core_outgoing_today(chat_id):
    postgresql_connection()
    try:
        time_line1 = []
        time_line2 = []
        Fer_MSX = []
        Tash_MSX = []
        date = datetime.date.today().strftime('%Y-%m-%d')
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT replace((replace((replace("Result_Time", ':15', ':00')),':30',':00')), ':45',
            ':00') as Time, "Object_Name", sum("Billing_rejects"::integer) FROM "Performance_Core_Billing_Reject" WHERE 
            "Object_Name" like '%101' and "Result_Time" like '{date}%' GROUP by Time, "Object_Name" 
            Order by Time""")
            for result in cursor.fetchall():
                if "Fer_MSX_H/ServiceKey:SRVKEY=101" in result[1]:
                    time = str.format(result[0]).replace(f"{date} ", "")
                    time_line1.append(time)
                    Fer_MSX.append(int(result[2]))

                elif "Tas_MSX_H/ServiceKey:SRVKEY=101" in result[1]:
                    time = str.format(result[0]).replace(f"{date} ", "")
                    time_line2.append(time)
                    Tash_MSX.append(int(result[2]))

            if len(time_line1):
                plt.subplot(3, 1, 1)
                plt.title(f"Отказы от биллинга: Исходящий Tas_MSX_H", color="black")
                plt.ylabel("times", color='black')
                plt.xticks(rotation=45)
                plt.plot(time_line2, Tash_MSX, label="Исходящий Отказы: Tas_MSX_H", color='red', linewidth=2,
                         marker="o")
                plt.grid()
                ax = plt.gca()
                ax.set_facecolor('white')

                plt.subplot(2, 1, 2)
                plt.title(f"Отказы от биллинга: Исходящий Fer_MSX_H", color="black")
                plt.ylabel("times", color='black')
                plt.xticks(rotation=45)
                plt.plot(time_line1, Fer_MSX, label="Исходящий Отказы: Fer_MSX_H", color='blue', linewidth=2,
                         marker="o")
                plt.grid()
                ax = plt.gca()
                ax.set_facecolor('white')
                file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                plt.savefig(fr"{path}/Files/{file_name}.png")
                plt.close()
                photo = InputFile(fr"{path}/Files/{file_name}.png")
                await bot.send_photo(chat_id=chat_id, photo=photo)

            else:
                await bot.send_message(chat_id=chat_id, text=f'Такой селл нет в БД или ввели неправильный атрибут')
    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if connection:
            connection.close()


async def get_rtwp_today_img(chat_id, cellid):
    postgresql_connection()
    x = []
    y = []
    date = datetime.date.today().strftime('%Y-%m-%d')
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT "Result_Time", "Period", "Object_Name", ROUND("MeanRTWP"::numeric,2)
        FROM "Performance_UMTS_RTWP" 
        WHERE "Object_Name" like '%CellID={cellid},%' and "Result_Time" like '{date}%'
        Order by "Result_Time" """)
        for result in cursor.fetchall():
            a = str.format(result[0]).replace(f"{date} ", "")
            y.append(a)
            x.append(result[3])
    if len(x):
        plt.title(f"Cell ID: {cellid} \nDate: {date}", color="blue")
        plt.ylabel("RTWP", color='blue')
        plt.xlabel("Time", color='blue')
        plt.xticks(rotation=45)
        plt.plot(y, x, label="MEAN RTWP", color='blue', linewidth=2, marker="o")
        plt.legend()
        plt.grid()
        ax = plt.gca()
        ax.set_facecolor('white')
        file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        plt.savefig(fr"{path}/Files/{file_name}.png")

        photo = InputFile(fr"{path}/Files/{file_name}.png")
        await bot.send_photo(chat_id=chat_id, photo=photo)
        plt.close()
    else:
        await bot.send_message(chat_id=chat_id, text=f'Такой селл нет в БД или ввели неправильный атрибут')


async def sql_user_registration(state):
    async with state.proxy() as data:
        postgresql_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO user_info VALUES('{data['User_ID']}','{data['Name']}','{data['contact']}',"
                               f"'{data['Verification']}')")
        except Exception as ex:
            print("[INFO] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()


async def get_user_confirmation(message):
    postgresql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT Confirmation FROM user_info WHERE User_id = '{message}'")
            for result in cursor.fetchall():
                return result[0]
    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if connection:
            connection.close()


async def get_user_right(message):
    postgresql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT "right" FROM user_info WHERE User_id = '{message}'""")
            for result in cursor.fetchall():
                return result[0]
    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if connection:
            connection.close()


async def get_user_not_confirmation():
    postgresql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM user_info WHERE Confirmation = 'NO'")
            for result in cursor.fetchall():
                return result
    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if connection:
            connection.close()

    # for confirm in cur.execute(f"SELECT User_name FROM user_info WHERE Confirmation = 'NO'").fetchall():
    #     return confirm[0]
    # base.commit()


async def for_admin_user_confirmation():
    postgresql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE user_info SET Confirmation = 'YES' WHERE Confirmation = 'NO'")
    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if connection:
            connection.close()

    # cur.execute(f"UPDATE user_info SET Confirmation = 'YES' WHERE Confirmation = 'NO'")
    # base.commit()


async def DEA_LTE_SHOS(user_id, bts_id):
    result = []
    for confirm in cur.execute(f"SELECT DEACELLFORMML FROM Block_LTE WHERE Site_Name like '%{bts_id})'").fetchall():
        result.append(confirm)
    x = f"{result}"
    a = x.replace("[", "").replace("'", "").replace("]", "").replace(", ", "\n").replace("(", "").replace(",)", "")
    await bot.send_message(user_id, f'{a}')


async def ACT_LTE_SHOS(user_id, bts_id):
    result = []
    for confirm in cur.execute(f"SELECT ACTCELLFORMML FROM Block_LTE WHERE Site_Name like '%{bts_id})'").fetchall():
        result.append(confirm)
    x = f"{result}"
    a = x.replace("[", "").replace("'", "").replace("]", "").replace(", ", "\n").replace("(", "").replace(",)", "")
    await bot.send_message(user_id, f'{a}')


async def blk_UMTS_CS_PS_SHOS(user_id, bts_id):
    result = []
    for confirm in cur.execute(f"SELECT DEAUnodeBforMML FROM Block_UMTS WHERE NEName like '%{bts_id})'").fetchall():
        result.append(confirm)
    x = f"{result}"
    a = x.replace("[", "").replace("'", "").replace("]", "").replace(", ", "\n").replace("(", "").replace(",)", "")
    await bot.send_message(user_id, f'{a}')


async def ubl_UMTS_CS_PS_SHOS(user_id, bts_id):
    result = []
    for confirm in cur.execute(f"SELECT ACTUnodeBforMML FROM Block_UMTS WHERE NEName like '%{bts_id})'").fetchall():
        result.append(confirm)
    x = f"{result}"
    a = x.replace("[", "").replace("'", "").replace("]", "").replace(", ", "\n").replace("(", "").replace(",)", "")
    await bot.send_message(user_id, f'{a}')


async def blk_UMTS_PS_SHOS(user_id, bts_id):
    result = []
    for confirm in cur.execute(f"SELECT UMTSPSOFFFORMML FROM Block_UMTS_PS WHERE NodeBName like '%{bts_id})'") \
            .fetchall():
        result.append(confirm)
    x = f"{result}"
    a = x.replace("[", "").replace("'", "").replace("]", "").replace(", ", "\n").replace("(", "").replace(",)", "")
    await bot.send_message(user_id, f'{a}')


async def ubl_UMTS_PS_SHOS(user_id, bts_id):
    result = []
    for confirm in cur.execute(f"SELECT UMTSPSONFORMML FROM Block_UMTS_PS WHERE NodeBName like '%{bts_id})'") \
            .fetchall():
        result.append(confirm)
    x = f"{result}"
    a = x.replace("[", "").replace("'", "").replace("]", "").replace(", ", "\n").replace("(", "").replace(",)", "")
    await bot.send_message(user_id, f'{a}')


async def blk_UMTS_CS_SHOS(user_id, bts_id):
    result = []
    for confirm in cur.execute(f"SELECT UMTSCSOFFFORMML FROM SHOS_Block_UMTS_CS WHERE NodeBName like '%{bts_id})'") \
            .fetchall():
        result.append(confirm)
    x = f"{result}"
    a = x.replace("[", "").replace("'", "").replace("]", "").replace(", ", "\n").replace("(", "").replace(",)", "")
    await bot.send_message(user_id, f'{a}')


async def ubl_UMTS_CS_SHOS(user_id, bts_id):
    result = []
    for confirm in cur.execute(f"SELECT UMTSCSONFORMML FROM SHOS_Block_UMTS_CS WHERE NodeBName like '%{bts_id})'") \
            .fetchall():
        result.append(confirm)
    x = f"{result}"
    a = x.replace("[", "").replace("'", "").replace("]", "").replace(", ", "\n").replace("(", "").replace(",)", "")
    await bot.send_message(user_id, f'{a}')


async def blk_RRU_SHOS(user_id, bts_id):
    result = []
    for confirm in cur.execute(f"SELECT BLKRRUFORMML FROM Block_RRU WHERE NEName like '%{bts_id})'").fetchall():
        result.append(confirm)
    x = f"{result}"
    a = x.replace("[", "").replace("'", "").replace("]", "").replace(", ", "\n").replace("(", "").replace(",)", "")
    await bot.send_message(user_id, f'{a}')


async def ubl_RRU_SHOS(user_id, bts_id):
    result = []
    for confirm in cur.execute(f"SELECT UBLRRUFORMML FROM Block_RRU WHERE NEName like '%{bts_id})'").fetchall():
        result.append(confirm)
    x = f"{result}"
    a = x.replace("[", "").replace("'", "").replace("]", "").replace(", ", "\n").replace("(", "").replace(",)", "")
    await bot.send_message(user_id, f'{a}')


async def get_blk_brd(user_id, bts_id):
    result = []
    for confirm in cur.execute(f"SELECT InventoryUnitID FROM Inventory_Subrack_20220505_114140 WHERE FrameType = 'RRU' "
                               f"and NEName like '%{bts_id})'").fetchall():
        subrack = f'BLK BRD:CN=0,SRN={confirm[0]},SN=0,BLKTP=IMMEDIATE;'
        result.append(subrack)
    x = f"{result}"
    a = x.replace("[", "").replace("'", "").replace("]", "").replace(", ", "\n")
    await bot.send_message(user_id, f'{a}')


async def get_ubl_brd(user_id, bts_id):
    result = []
    for confirm in cur.execute(f"SELECT InventoryUnitID FROM Inventory_Subrack_20220505_114140 WHERE FrameType = 'RRU' "
                               f"and NEName like '%{bts_id})'").fetchall():
        subrack = f'UBL BRD:CN = 0,SRN = {confirm[0]},SN = 0;'
        result.append(subrack)
    x = f"{result}"
    a = x.replace("[", "").replace("'", "").replace("]", "").replace(", ", "\n")
    await bot.send_message(user_id, f'{a}')


async def for_dsp_mmctx(user_id, enodeb_id, cell_id, cgi):
    postgresql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT "LTENEName", "CellID", replace(replace("FrequencyBand"::text,'3', 'LTE1800'),
            '28', 'LTE700') as BAND, (regexp_matches("LTENEName", '\((\d+)\)'))[1]
            FROM "RAN_Report_LTE_Cell" 
            WHERE "eNodeBID" = '{enodeb_id}' AND "CellID" = '{cell_id}'""")
            for result in cursor.fetchall():
                site_name = result[0]
                ci = result[1]
                band = result[2]
                site_id = result[3]
            try:
                cursor.execute(f"""SELECT replace(replace(replace(replace(replace(replace("NeName", 'Tash_RNC1_H', 
                'Tashkent city'), 'Tash_RNC2_H', 'Tashkent region'), 'And_RNC1_H', 'Andijan region'), 'Fer_RNC1_H', 
                'Fergana region'), 'Nam_RNC1_H', 'Namangan region'), 'GUL_RNC1_H', 'Sirdarya region'), 
                "Longitude", "Latitude", "District", "Address"
                FROM "RF_Plan_UMTS"
                where "Site_Name" like '%({site_id})'
                group by "NeName", "Longitude", "Latitude", "District", "Address";""")
                for result in cursor.fetchall():
                    if len(result):
                        region = result[0]
                        longitude = result[1]
                        latitude = result[2]
                        district = result[3]
                        address = result[4]
                    else:
                        region = ""

                cell_information = str.format(f"\nE-UTRAN cell global identity - {cgi}"
                                              f"\nEnodeB ID - {enodeb_id}"
                                              f"\nSite Name - {site_name}"
                                              f"\nSite ID - {site_id}"
                                              f"\nCell ID - {ci}"
                                              f"\nBand - {band}"
                                              f"\nRegion - {region}"
                                              f"\nDistrict - {district}"
                                              f"\nAddress - {address}"
                                              f"\nLongitude - {longitude}"
                                              f"\nLatitude - {latitude}"
                                              f'''\n<a href='https://yandex.uz/maps/10335/tashkent/?ll={longitude}%2C{latitude}&mode=searc
                               h&sll={longitude}%2C{latitude}&text={latitude}%2C{longitude}&z=17.16'>Location</a>''')
                await bot.send_message(user_id, f'{cell_information}',
                                       reply_markup=InlineKeyboardMarkup(row_width=1)
                                       .add(InlineKeyboardButton(text='Location', callback_data=f'{site_id}')),
                                       disable_web_page_preview=True)
            except:
                cell_information = str.format(f"\nE-UTRAN cell global identity - {cgi}"
                                              f"\nEnodeB ID - {enodeb_id}"
                                              f"\nSite Name - {site_name}"
                                              f"\nSite ID - {site_id}"
                                              f"\nCell ID - {ci}"
                                              f"\nBand - {band}")
                await bot.send_message(user_id, f'{cell_information}',
                                       reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                                       .add(KeyboardButton("🔙Back"))
                                       .add(KeyboardButton("🔝Main menu")))
    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if connection:
            connection.close()


async def for_dsp_mmctx_umts(user_id, cell_id, cgi, rnc_id):
    postgresql_connection()
    rnc_ids = {'1': 'Tash_RNC1_H', '712': 'Tash_RNC2_H', '741': 'And_RNC1_H', '731': 'Fer_RNC1_H', '671': 'GUL_RNC1_H',
               '691': 'Nam_RNC1_H'}
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT "NeName", "NodeBId", "Site_Name", 
            replace(SPLIT_PART("Site_Name", '(', 2), ')', '') AS "Site_ID", "Cell_Id", "Cell_Name", 
            replace(replace(replace(replace("DL_Freq", '10787', 'U2100'), '10812', 'U2100'), '10837', 'U2100'), 
            '3058', 'U900') as "Band", "LAC", 
            "District", "Address", "Longitude", "Latitude"
            FROM "RF_Plan_UMTS"
            where "Cell_Id" = '{cell_id}' and "NeName" = '{rnc_ids[f'{rnc_id}']}';""")
            for result in cursor.fetchall():
                ne_name = result[0]
                nodeb_id = result[1]
                site_name = result[2]
                site_id = result[3]
                ci = result[4]
                cell_name = result[5]
                band = result[6]
                lac = result[7]
                district = result[8]
                address = result[9]
                longitude = result[10]
                latitude = result[11]

                cell_information = str.format(f"\nService area of user - {cgi}"
                                              f"\nRNC_Name - {ne_name}"
                                              f"\nNodeb ID - {nodeb_id}"
                                              f"\nSite Name - {site_name}"
                                              f"\nSite ID - {site_id}"
                                              f"\nCell ID - {ci}"
                                              f"\nCell Name - {cell_name}"
                                              f"\nBand - {band}"
                                              f"\nLAC - {lac}"
                                              f"\nDistrict - {district}"
                                              f"\nAddress - {address}"
                                              f"\nLongitude - {longitude}"
                                              f"\nLatitude - {latitude}"
                                              f'''\n<a href='https://yandex.uz/maps/10335/tashkent/?ll={longitude}%2C{latitude}&mode=searc
                               h&sll={longitude}%2C{latitude}&text={latitude}%2C{longitude}&z=17.16'>Location</a>''')
                await bot.send_message(user_id, f'{cell_information}',
                                       reply_markup=InlineKeyboardMarkup(row_width=1)
                                       .add(InlineKeyboardButton(text='Location', callback_data=f'{site_id}')),
                                       disable_web_page_preview=True)
    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if connection:
            connection.close()


async def for_dsp_mmctx_gsm(user_id, cell_id, cgi, lac):
    postgresql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT "NEName", "SiteIndex", "CI", "CellName", "FreqSeg", "LAC", 
            replace(SPLIT_PART(SPLIT_PART("SiteName", '@', 1), '(', 2), ')', '') AS "Site_ID",
            replace(SPLIT_PART("SiteName", '@', 1), '_2G', '') AS "Site_Name"
            FROM "RAN_Report_GSM_Cell"
            where "CI" = '{cell_id}' and "LAC" = '{lac}';""")
            for result in cursor.fetchall():
                ne_name = result[0]
                site_index = result[1]
                ci = result[2]
                cell_name = result[3]
                band = result[4]
                lac = result[5]
                site_id = result[6]
                site_name = result[7]
            try:
                cursor.execute(f"""SELECT replace(replace(replace(replace(replace(replace("NeName", 'Tash_RNC1_H', 
                'Tashkent city'), 'Tash_RNC2_H', 'Tashkent region'), 'And_RNC1_H', 'Andijan region'), 'Fer_RNC1_H', 
                'Fergana region'), 'Nam_RNC1_H', 'Namangan region'), 'GUL_RNC1_H', 'Sirdarya region'), 
                "Longitude", "Latitude", "District", "Address"
                FROM "RF_Plan_UMTS"
                where "Site_Name" like '%({site_id})'
                group by "Site_Name", "NeName", "Longitude", "Latitude", "District", "Address";""")
                for result in cursor.fetchall():
                    region = result[0]
                    longitude = result[1]
                    latitude = result[2]
                    district = result[3]
                    address = result[4]

                cell_information = str.format(f"\nService area of user - {cgi}"
                                              f"\nBSC Name - {ne_name}"
                                              f"\nSite Index - {site_index}"
                                              f"\nSite Name - {site_name}"
                                              f"\nSite ID - {site_id}"
                                              f"\nCell ID - {ci}"
                                              f"\nCell Name - {cell_name}"
                                              f"\nBand - {band}"
                                              f"\nLAC - {lac}"
                                              f"\nRegion - {region}"
                                              f"\nDistrict - {district}"
                                              f"\nAddress - {address}"
                                              f"\nLongitude - {longitude}"
                                              f"\nLatitude - {latitude}"
                                              f'''\n<a href='https://yandex.uz/maps/10335/tashkent/?ll={longitude}%2C{latitude}&mode=search&sll={longitude}%2C{latitude}&text={latitude}%2C{longitude}&z=17.16'>Location</a>'''
                                              )
                await bot.send_message(user_id, f'{cell_information}',
                                       reply_markup=InlineKeyboardMarkup(row_width=1)
                                       .add(InlineKeyboardButton(text='Location', callback_data=f'{site_id}')),
                                       disable_web_page_preview=True)
            except:
                cell_information = str.format(f"\nService area of user - {cgi}"
                                              f"\nBSC Name - {ne_name}"
                                              f"\nSite Index - {site_index}"
                                              f"\nSite Name - {site_name}"
                                              f"\nSite ID - {site_id}"
                                              f"\nCell ID - {ci}"
                                              f"\nCell Name - {cell_name}"
                                              f"\nBand - {band}"
                                              f"\nLAC - {lac}")
                await bot.send_message(user_id, f'{cell_information}',
                                       reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
                                       .add(KeyboardButton("🔙Back"))
                                       .add(KeyboardButton("🔝Main menu")))
    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if connection:
            connection.close()


async def for_get_site_information(user_id, site_id):
    postgresql_connection()
    try:
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""Select * From "For_Database_Site_information" where "SiteID" = '{site_id}'""")
                for result in cursor.fetchall():
                    site_id = result[0]
                    site_name = result[1]
                    region = result[2]
                    longitude = result[3]
                    latitude = result[4]
                    address = result[5]
                    ne_type = result[6]
                    date_of_lunch = result[7]
                site_information = str.format(f"\nSite ID - {site_id}"
                                              f"\nSite Name - {site_name}"
                                              f"\nRegion - {region}"
                                              f"\nLongitude - {longitude}"
                                              f"\nLatitude - {latitude}"
                                              f"\nAddress - {address}"
                                              f"\nNe Type - {ne_type}"
                                              f"\nDate of launch - {date_of_lunch}"
                                              f'''\n<a href='https://yandex.uz/maps/10335/tashkent/?ll={longitude}%2C{latitude}&mode=searc
                               h&sll={longitude}%2C{latitude}&text={latitude}%2C{longitude}&z=17.16'>Location</a>''')
            except:
                site_information = ""
            try:
                cursor.execute(f"""SELECT "SiteIndex" FROM "RAN_Report_GSM_Cell" WHERE "SiteName" like '%({site_id})' 
                and "ActivityStatus" = 'ACTIVATED' GROUP by "SiteIndex" """)
                for result in cursor.fetchall():
                    site_id = result[0]
                site_index = str.format(f"Site index - {site_id}")
            except:
                site_index = ""
    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if connection:
            connection.close()
    await bot.send_message(user_id, f'{site_information}'
                                    f'\n\n{site_index}', reply_markup=InlineKeyboardMarkup(row_width=1)
                           .add(InlineKeyboardButton(text='Location', callback_data=f'{site_id}')),
                           disable_web_page_preview=True)


async def for_get_location(user_id, site_id):
    postgresql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT "Longitude", "Latitude"
            FROM "RF_Plan_UMTS"
            where "Site_Name" like '%({site_id})'
            group by "Longitude", "Latitude";""")
            for result in cursor.fetchall():
                longitude = result[0]
                latitude = result[1]
    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if connection:
            connection.close()
    await bot.send_location(user_id, latitude=latitude, longitude=longitude)


class SampleSQL:
    # def get_raw_data(btsid) -> str:
    #     _sql_server = "DESKTOP-F17DSNU\SQLEXPRESS"
    #     _database = "For_Telegram_bot"
    #     connection = pypyodbc.connect('Driver={SQL Server};'
    #                                   'Server=' + _sql_server + ';'
    #                                                             'Database=' + _database + ';')
    #     cursor = connection.cursor()
    #     mySQLQuery = (f"""
    #     Select [Site ID], [Site Name], Region, Longitude, Latitude, Address, Ne_type, Description
    #     From Site$
    #     where [Site ID] = {btsid}
    #     Group by [Site ID], [Site Name], Region, Longitude, Latitude, Address, Ne_type, Description
    #     """)
    #
    #     cursor.execute(mySQLQuery)
    #     results = cursor.fetchall()
    #     try:
    #         for row in results:
    #             Site_id = int(row[0])
    #             site_name = row[1]
    #             region = row[2]
    #             long = row[3]
    #             lat = row[4]
    #             Address = row[5]
    #             NE_Type = row[6]
    #             Description = row[7]
    #
    #         return str.format(f"Site ID - {Site_id}"
    #                           f"\nSite Name - {site_name}"
    #                           f"\nRegion - {region}"
    #                           f"\nLongitude - {long}"
    #                           f"\nLatitude - {lat}"
    #                           f"\nAddress - {Address}"
    #                           f"\nNe_Type - {NE_Type}"
    #                           f"\nDescription - {Description}"
    #                           f'''\n<a href='https://yandex.uz/maps/10335/tashkent/?ll={long}%2C{lat}&mode=search&sll={long}%2C{lat}&text={lat}%2C{long}&z=17.16'>Location</a>''')
    #     except:
    #         return str.format("The site does not exist in the database")
    #
    #     connection.close()

    # def get_raw_data_for_GSMCell(CellID) -> str:
    #     _sql_server = "DESKTOP-F17DSNU\SQLEXPRESS"
    #     _database = "For_Telegram_bot"
    #     connection = pypyodbc.connect('Driver={SQL Server};'
    #                                   'Server=' + _sql_server + ';'
    #                                                             'Database=' + _database + ';')
    #     cursor = connection.cursor()
    #     mySQLQuery = (f"""
    #         Select [NE Name], [Site Name], [Site Index], [Cell Index], [Cell Name], CI, FreqSeg as Technology, LAC, BCCHNO as BCCH
    #         From RAN_Report_GSM_Cell
    #         Where CI like '{CellID}'
    #         Order by CI
    #         """)
    #
    #     cursor.execute(mySQLQuery)
    #     results = cursor.fetchall()
    #     try:
    #         for row in results:
    #             NE_Name = row[0]
    #             Site_Name = row[1]
    #             Site_Index = int(row[2])
    #             Cell_Index = int(row[3])
    #             Cell_Name = int(row[4])
    #             CI = int(row[5])
    #             Technology = row[6]
    #             LAC = int(row[7])
    #             BCCH = int(row[8])
    #             return (f"NE Name - {NE_Name}"
    #                     f"\nSite Name - {Site_Name}"
    #                     f"\nSite Index - {Site_Index}"
    #                     f"\nCell Index - {Cell_Index}"
    #                     f"\nCell Name - {Cell_Name}"
    #                     f"\nCI - {CI}"
    #                     f"\nTechnology - {Technology}"
    #                     f"\nLAC - {LAC}"
    #                     f"\nBCCH - {BCCH}"
    #                     f"\n")
    #
    #     except:
    #         return str.format("The cell does not exist in the database")
    #
    #     connection.close()

    # def get_raw_data_for_UMTSCell(CellID) -> str:
    #     _sql_server = "DESKTOP-F17DSNU\SQLEXPRESS"
    #     _database = "For_Telegram_bot"
    #     connection = pypyodbc.connect('Driver={SQL Server};'
    #                                   'Server=' + _sql_server + ';'
    #                                                             'Database=' + _database + ';')
    #     cursor = connection.cursor()
    #     mySQLQuery = (f"""
    #         Select [BSC Name], [NodeB Name], [Cell ID], [Cell Name], [Band Indicator], [Downlink UARFCN],
    #         [DL Primary Scrambling Code], [Location Area Code], [Routing Area Code], [Max Transmit Power of Cell],
    #         [PCPICH Transmit Power]
    #         From CELL$
    #         Where [Cell ID] like '{CellID}'
    #         Order by [Cell ID]
    #         """)
    #
    #     cursor.execute(mySQLQuery)
    #     results = cursor.fetchall()
    #     try:
    #         for row in results:
    #             NE_Name = row[0]
    #             NodeB_Name = row[1]
    #             Cell_ID = int(row[2])
    #             Cell_Name = int(row[3])
    #             Band_Indicator = row[4]
    #             DL_UARFCN = int(row[5])
    #             Scrambling_Code = int(row[6])
    #             LAC = int(row[7])
    #             RAC = int(row[8])
    #             Max_Transmit_Power = int(row[9])
    #             PCPICH_Transmit_Power = int(row[10])
    #             return (f"NE Name - {NE_Name}"
    #                     f"\nNodeB Name - {NodeB_Name}"
    #                     f"\nCell ID - {Cell_ID}"
    #                     f"\nCell Name - {Cell_Name}"
    #                     f"\nBand Indicator - {Band_Indicator}"
    #                     f"\nDL UARFCN - {DL_UARFCN}"
    #                     f"\nScrambling Code - {Scrambling_Code}"
    #                     f"\nLAC - {LAC}"
    #                     f"\nRAC - {RAC}"
    #                     f"\nMax Transmit Power - {Max_Transmit_Power}"
    #                     f"\nPCPICH Transmit Power - {PCPICH_Transmit_Power}"
    #                     f"\n")
    #
    #     except:
    #         return str.format("The cell does not exist in the database")
    #
    #     connection.close()

    def get_nearest(longitude, latitude) -> str:
        postgresql_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'select "SiteName", "Latitude", "Longitude", Round((6371*(acos(cos(radians(90-"Latitude"))*'
                    f'cos(radians(90-{latitude}))+sin(radians(90-"Latitude"))*sin(radians(90-{latitude}))*cos(radians'
                    f'("Longitude"-{longitude}))))*1000)::numeric,2) as "Distance" from '
                    f'"For_Database_Site_information" group by "SiteName", "Latitude", "Longitude" order by '
                    f'"Distance" limit 1')
                for result in cursor.fetchall():
                    BTS_Name = result[0]
                    Latitude = result[1]
                    Longitude = result[2]
                    distance = result[3]
                return str.format(f"***Самый ближайший сайт***"
                                  f"\nBTS Name - {BTS_Name}"
                                  f"\nLongitude - {Longitude}"
                                  f"\nLatitude - {Latitude}"
                                  f"\nDistance - {distance}м"
                                  f'''\n<a href='https://yandex.uz/maps/10335/tashkent/?ll={Longitude}%2C{Latitude}&
                                  mode=search&sll={Longitude}%2C{Latitude}&text={Latitude}%2C{Longitude}&z=17.16'
                                  >Location</a>''')
        except Exception as ex:
            print("[INFO] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()

    def get_top1_data(longitude, latitude) -> str:
        postgresql_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'select "SiteName", "Latitude", "Longitude", Round((6371*(acos(cos(radians(90-"Latitude"))*'
                    f'cos(radians(90-{latitude}))+sin(radians(90-"Latitude"))*sin(radians(90-{latitude}))*cos(radians'
                    f'("Longitude"-{longitude}))))*1000)::numeric,2) as "Distance" from '
                    f'"For_Database_Site_information" group by "SiteName", "Latitude", "Longitude" order by '
                    f'"Distance" limit 2')
                for result in cursor.fetchall():
                    BTS_Name = result[0]
                    Latitude = result[1]
                    Longitude = result[2]
                    distance = result[3]
                return str.format(f"\nBTS Name - {BTS_Name}"
                                  f"\nLongitude - {Longitude}"
                                  f"\nLatitude - {Latitude}"
                                  f"\nDistance - {distance}м"
                                  f'''\n<a href='https://yandex.uz/maps/10335/tashkent/?ll={Longitude}%2C{Latitude}&
                                          mode=search&sll={Longitude}%2C{Latitude}&text={Latitude}%2C{Longitude}&z=17.16'
                                          >Location</a>''')
        except Exception as ex:
            print("[INFO] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()

    def get_top2_data(longitude, latitude) -> str:
        postgresql_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'select "SiteName", "Latitude", "Longitude", Round((6371*(acos(cos(radians(90-"Latitude"))*'
                    f'cos(radians(90-{latitude}))+sin(radians(90-"Latitude"))*sin(radians(90-{latitude}))*cos(radians'
                    f'("Longitude"-{longitude}))))*1000)::numeric,2) as "Distance" from '
                    f'"For_Database_Site_information" group by "SiteName", "Latitude", "Longitude" order by '
                    f'"Distance" limit 3')
                for result in cursor.fetchall():
                    BTS_Name = result[0]
                    Latitude = result[1]
                    Longitude = result[2]
                    distance = result[3]
                return str.format(f"\nBTS Name - {BTS_Name}"
                                  f"\nLongitude - {Longitude}"
                                  f"\nLatitude - {Latitude}"
                                  f"\nDistance - {distance}м"
                                  f'''\n<a href='https://yandex.uz/maps/10335/tashkent/?ll={Longitude}%2C{Latitude}&
                                                  mode=search&sll={Longitude}%2C{Latitude}&text={Latitude}%2C{Longitude}&z=17.16'
                                                  >Location</a>''')
        except Exception as ex:
            print("[INFO] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()

    def get_top3_data(longitude, latitude) -> str:
        postgresql_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'select "SiteName", "Latitude", "Longitude", Round((6371*(acos(cos(radians(90-"Latitude"))*'
                    f'cos(radians(90-{latitude}))+sin(radians(90-"Latitude"))*sin(radians(90-{latitude}))*cos(radians'
                    f'("Longitude"-{longitude}))))*1000)::numeric,2) as "Distance" from '
                    f'"For_Database_Site_information" group by "SiteName", "Latitude", "Longitude" order by '
                    f'"Distance" limit 4')
                for result in cursor.fetchall():
                    BTS_Name = result[0]
                    Latitude = result[1]
                    Longitude = result[2]
                    distance = result[3]
                return str.format(f"\nBTS Name - {BTS_Name}"
                                  f"\nLongitude - {Longitude}"
                                  f"\nLatitude - {Latitude}"
                                  f"\nDistance - {distance}м"
                                  f'''\n<a href='https://yandex.uz/maps/10335/tashkent/?ll={Longitude}%2C{Latitude}&
                                                  mode=search&sll={Longitude}%2C{Latitude}&text={Latitude}%2C{Longitude}&z=17.16'
                                                  >Location</a>''')
        except Exception as ex:
            print("[INFO] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()

    def get_top4_data(longitude, latitude) -> str:
        postgresql_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'select "SiteName", "Latitude", "Longitude", Round((6371*(acos(cos(radians(90-"Latitude"))*'
                    f'cos(radians(90-{latitude}))+sin(radians(90-"Latitude"))*sin(radians(90-{latitude}))*cos(radians'
                    f'("Longitude"-{longitude}))))*1000)::numeric,2) as "Distance" from '
                    f'"For_Database_Site_information" group by "SiteName", "Latitude", "Longitude" order by '
                    f'"Distance" limit 5')
                for result in cursor.fetchall():
                    BTS_Name = result[0]
                    Latitude = result[1]
                    Longitude = result[2]
                    distance = result[3]
                return str.format(f"\nBTS Name - {BTS_Name}"
                                  f"\nLongitude - {Longitude}"
                                  f"\nLatitude - {Latitude}"
                                  f"\nDistance - {distance}м"
                                  f'''\n<a href='https://yandex.uz/maps/10335/tashkent/?ll={Longitude}%2C{Latitude}&
                                                  mode=search&sll={Longitude}%2C{Latitude}&text={Latitude}%2C{Longitude}&z=17.16'
                                                  >Location</a>''')
        except Exception as ex:
            print("[INFO] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()

    def get_top5_data(longitude, latitude) -> str:
        postgresql_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'select "SiteName", "Latitude", "Longitude", Round((6371*(acos(cos(radians(90-"Latitude"))*'
                    f'cos(radians(90-{latitude}))+sin(radians(90-"Latitude"))*sin(radians(90-{latitude}))*cos(radians'
                    f'("Longitude"-{longitude}))))*1000)::numeric,2) as "Distance" from '
                    f'"For_Database_Site_information" group by "SiteName", "Latitude", "Longitude" order by '
                    f'"Distance" limit 6')
                for result in cursor.fetchall():
                    BTS_Name = result[0]
                    Latitude = result[1]
                    Longitude = result[2]
                    distance = result[3]
                return str.format(f"\nBTS Name - {BTS_Name}"
                                  f"\nLongitude - {Longitude}"
                                  f"\nLatitude - {Latitude}"
                                  f"\nDistance - {distance}м"
                                  f'''\n<a href='https://yandex.uz/maps/10335/tashkent/?ll={Longitude}%2C{Latitude}&
                                                  mode=search&sll={Longitude}%2C{Latitude}&text={Latitude}%2C{Longitude}&z=17.16'
                                                  >Location</a>''')
        except Exception as ex:
            print("[INFO] Error while working with PostgreSQL", ex)
        finally:
            if connection:
                connection.close()

    def get_top_final(self):

        return str.format(f"{SampleSQL.get_nearest()} "
                          f"\n ***Топ 5 ближайших сайтов***"
                          f"\n {SampleSQL.get_top1_data()}"
                          f"\n {SampleSQL.get_top2_data()}"
                          f"\n {SampleSQL.get_top3_data()}"
                          f"\n {SampleSQL.get_top4_data()}"
                          f"\n {SampleSQL.get_top5_data()}")

    # def get_power_information(BTS_id) -> str:
    #     _sql_server = "DESKTOP-F17DSNU\SQLEXPRESS"
    #     _database = "For_Telegram_bot"
    #     connection = pypyodbc.connect('Driver={SQL Server};'
    #                                   'Server=' + _sql_server + ';'
    #                                                             'Database=' + _database + ';')
    #     cursor = connection.cursor()
    #     mySQLQuery = (f"""
    #         Select NEName, [ID ], Configuration, Comments
    #         from ['RRU CONFIGURATION$']
    #         Where [ID ] = {BTS_id}
    #         group by NEName, [ID ], Configuration, Comments
    #         """)
    #
    #     cursor.execute(mySQLQuery)
    #     results = cursor.fetchall()
    #     try:
    #         for row in results:
    #             NE_Name = row[0]
    #             Site_ID = int(row[1])
    #             Configuration = row[2]
    #             Description = row[3]
    #
    #             return (f"Site name - {NE_Name}"
    #                     f"\nSite_ID - {Site_ID}"
    #                     f"\n\nConfiguration - {Configuration}"
    #                     f"\n\nDescription - {Description}")
    #
    #     except:
    #         return str.format("The site does not exist in the database")
    #
    #     connection.close()
