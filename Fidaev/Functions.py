from Create_bot import bot
import requests
import json
import psycopg2
import re


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


def get_token():
    url = "https://10.15.8.5:31127/api/rest/securityManagement/v1/oauth/token"

    payload = json.dumps({
        "grantType": "password",
        "userName": "test_api",
        "value": "qwerty@1"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

    data = response.text

    data_dict = json.loads(data)

    token = data_dict["accessSession"]

    # print(token)

    return token


async def MML_RET_Configuration(chatid, input_text):
    split = input_text.replace("\t", " ").replace("\n", " ").replace("  ", " ").split(" ")
    calc = 0
    calc2 = 1
    final_result = []
    for a in split:
        try:
            subrack = int(split[calc])
        except:
            break
        sn = split[calc2]
        sn2 = sn[-2:]
        sector1 = [60, 70, 73, 80, 83, 90, 93, 100]
        sector2 = [61, 71, 74, 81, 84, 91, 94, 101]
        sector3 = [62, 72, 75, 82, 85, 92, 95, 102]
        f900 = ["0r", "yC"]
        f1800 = ["bR", "yR", "0b"]
        f2100 = ["bL", "yL"]
        f700_900R = ["r2"]
        f700_900L = ["r1"]
        f1800_2100R = ["y1"]
        f1800_2100L = ["y3"]
        if sn2 in f900 and subrack in sector1:
            DEVICENAME = "Sector1_900"
            MMLScript = f"""ADD RET:DEVICENO=0,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f900 and subrack in sector2:
            DEVICENAME = "Sector2_900"
            MMLScript = f"""ADD RET:DEVICENO=1,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f900 and subrack in sector3:
            DEVICENAME = "Sector3_900"
            MMLScript = f"""ADD RET:DEVICENO=2,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)

        elif sn2 in f1800 and subrack in sector1:
            DEVICENAME = "Sector1_1800"
            MMLScript = f"""ADD RET:DEVICENO=3,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f1800 and subrack in sector2:
            DEVICENAME = "Sector2_1800"
            MMLScript = f"""ADD RET:DEVICENO=4,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f1800 and subrack in sector3:
            DEVICENAME = "Sector3_1800"
            MMLScript = f"""ADD RET:DEVICENO=5,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)

        elif sn2 in f2100 and subrack in sector1:
            DEVICENAME = "Sector1_2100"
            MMLScript = f"""ADD RET:DEVICENO=6,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f2100 and subrack in sector2:
            DEVICENAME = "Sector2_2100"
            MMLScript = f"""ADD RET:DEVICENO=7,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f2100 and subrack in sector3:
            DEVICENAME = "Sector3_2100"
            MMLScript = f"""ADD RET:DEVICENO=8,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)

        elif sn2 in f700_900R and subrack in sector1:
            DEVICENAME = "Sector1_700/900(R)"
            MMLScript = f"""ADD RET:DEVICENO=9,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f700_900L and subrack in sector1:
            DEVICENAME = "Sector1_700/900(L)"
            MMLScript = f"""ADD RET:DEVICENO=10,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f700_900R and subrack in sector2:
            DEVICENAME = "Sector2_700/900(R)"
            MMLScript = f"""ADD RET:DEVICENO=11,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f700_900L and subrack in sector2:
            DEVICENAME = "Sector2_700/900(L)"
            MMLScript = f"""ADD RET:DEVICENO=12,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f700_900R and subrack in sector3:
            DEVICENAME = "Sector3_700/900(R)"
            MMLScript = f"""ADD RET:DEVICENO=13,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f700_900L and subrack in sector3:
            DEVICENAME = "Sector3_700/900(L)"
            MMLScript = f"""ADD RET:DEVICENO=14,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)

        elif sn2 in f1800_2100R and subrack in sector1:
            DEVICENAME = "Sector1_1800/2100(R)"
            MMLScript = f"""ADD RET:DEVICENO=15,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f1800_2100L and subrack in sector1:
            DEVICENAME = "Sector1_1800/2100(L)"
            MMLScript = f"""ADD RET:DEVICENO=16,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f1800_2100R and subrack in sector2:
            DEVICENAME = "Sector2_1800/2100(R)"
            MMLScript = f"""ADD RET:DEVICENO=17,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f1800_2100L and subrack in sector2:
            DEVICENAME = "Sector2_1800/2100(L)"
            MMLScript = f"""ADD RET:DEVICENO=18,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f1800_2100R and subrack in sector3:
            DEVICENAME = "Sector3_1800/2100(R)"
            MMLScript = f"""ADD RET:DEVICENO=19,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        elif sn2 in f1800_2100L and subrack in sector3:
            DEVICENAME = "Sector3_1800/2100(L)"
            MMLScript = f"""ADD RET:DEVICENO=20,DEVICENAME="{DEVICENAME}",CTRLCN=0,CTRLSRN={subrack},CTRLSN=0,""" \
                        f"""RETTYPE=SINGLE_RET,SCENARIO=DAISY_CHAIN,VENDORCODE="HW",SERIALNO="{sn}";"""
            final_result.append(MMLScript)
        else:
            final_result.append("")
        calc2 += 2
        calc += 2
    to_return = str(final_result).replace("['", "").replace("', '", "\n\n").replace("']", "")
    await bot.send_message(chat_id=chatid, text=f'{to_return}')


async def fault_request(chatid, site_id):
    postgresql_connection()
    ne_name = ''
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT "Ne_Name"
        FROM "RAN_Ne_Report"
        where "Ne_Name" like '%({site_id})%';""")
        for result in cursor.fetchall():
            ne_name = result[0]
    if ne_name == "":
        await bot.send_message(chat_id=chatid, text=f'Такой сайт не существует.')
    else:
        url = (f"https://10.15.8.5:31127/api/rest/faultSupervisonManagement/v1/alarms?dataType=CURRENT&alarmAckState="
               f"ALL_ACTIVE_ALARMS&baseObjectInstance={ne_name}")
        token = get_token()

        payload = ""
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': f'{token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        data = response.text

        # print(data)

        data_dict = json.loads(data)
        # print(data_dict)

        alarm_name = data_dict["alarmInformationList"]
        alarms = []
        text_for_send = f"На данный момент на этом элементе({ne_name}) есть следующие аварии:\n\n"
        for i in alarm_name:
            alarms.append(i["alarmName"])
            text_for_send += f"""{i["meName"]} - {i["alarmName"]}\n"""

        if len(alarms):
            pass
        else:
            text_for_send = f"На данный момент на этом элементе({ne_name}) нет аварий"

        await bot.send_message(chat_id=chatid, text=f'{text_for_send}')


async def mml_request_dsp_cell(chatid, site_id):
    postgresql_connection()
    ne_name = ''
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT "Ne_Name"
            FROM "RAN_Ne_Report"
            where "Ne_Name" like '%({site_id})%';""")
        for result in cursor.fetchall():
            ne_name = result[0]
    if ne_name == "":
        await bot.send_message(chat_id=chatid, text=f'Такой сайт не существует.')
    else:
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT "LocalCellID"
            FROM "RAN_Report_LTE_Cell"
            where "LTENEName" like '%({site_id})%'
            order by "LocalCellID";""")
            for result in cursor.fetchall():
                url = "https://10.15.8.5:31127/api/rest/mmlManagement/v1/command"
                token = get_token()

                payload = json.dumps({
                    "command": f'DSP CELL:LOCALCELLID={result[0]};',
                    "neNames": [
                        f"{ne_name}"
                    ]
                })
                headers = {
                    'Content-Type': 'application/json',
                    'X-Auth-Token': f'{token}'
                }

                response = requests.request("POST", url, headers=headers, data=payload, verify=False)

                data = response.text
                data_dict = json.loads(data)
                text_for_message = data_dict['results'][0]["report"].split('(Number of results =')[0]

                await bot.send_message(chat_id=chatid, text=f'{text_for_message}')
    connection.close()


async def mml_request_dsp_ulocell(chatid, site_id):
    postgresql_connection()
    ne_name = ''
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT "Ne_Name"
            FROM "RAN_Ne_Report"
            where "Ne_Name" like '%({site_id})%';""")
        for result in cursor.fetchall():
            ne_name = result[0]
    if ne_name == "":
        await bot.send_message(chat_id=chatid, text=f'Такой сайт не существует.')
    else:
        url = "https://10.15.8.5:31127/api/rest/mmlManagement/v1/command"
        token = get_token()

        payload = json.dumps({
            "command": 'DSP ULOCELL:;',
            "neNames": [
                "ATC-241(1014)"
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': f'{token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        data = response.text
        # print(data)
        data_dict = json.loads(data.replace(r"\r\n(Number of results = 18)\r\n\r\n\r\n---    END\r\n\r\n", ""))
        text = data_dict['results'][0]["report"]
        local_cell_ids = re.findall(r'Local Cell ID\s+=\s+(\d+)', text)
        local_cell_statuses = re.findall(r'Local Cell Status\s+=\s+(.*?)Local Cell Administration Status', text,
                                         re.DOTALL)
        local_cell_administrative_statuses = re.findall(r'Local Cell Administration Status\s+=\s+(.*?)Cell ID', text,
                                                        re.DOTALL)

        local_cell_cell_ids = re.findall(r'Cell ID\s+=\s+(.*?)Cell Transmit Diversity Status', text, re.DOTALL)
        cell_ids = []
        for ci in local_cell_cell_ids:
            cell_id = re.findall(r'Cell ID\s+=\s+(.*?)Cell Operation Status', ci, re.DOTALL)
            for a in cell_id:
                cell_ids.append(a)

        local_cell_ul_freq = re.findall(r'UL Frequency Channel Number\s+=\s+(.*?)DL Frequency Channel Number', text,
                                        re.DOTALL)
        local_cell_dl_freq = re.findall(r'DL Frequency Channel Number\s+=\s+(.*?)UL 16QAM Capability', text, re.DOTALL)
        local_cell_64_qam = re.findall(r'UL 16QAM Capability\s+=\s+(.*?)UL L2 Enhanced Capability', text, re.DOTALL)
        local_cell_normal_beam = re.findall(r'Normal Beam Capability\s+=\s+(.*?)Massive Beam 4T4R Capability', text,
                                            re.DOTALL)
        local_cell_4t4r_beam = re.findall(r'Massive Beam 4T4R Capability\s+=\s+(.*?)Massive Beam 8T8R Capability', text,
                                          re.DOTALL)
        local_cell_8t8r_beam = re.findall(
            r'Massive Beam 8T8R Capability\s+=\s+(.*?)UMTS and LTE Spectrum Sharing Capability', text, re.DOTALL)
        for shag in range(0, len(local_cell_ids)):
            text = fr"""Local Cell ID = {local_cell_ids[shag]}
Local Cell Status = {local_cell_statuses[shag].strip()}
Local Cell Administration Status = {local_cell_administrative_statuses[shag].strip()}
Cell ID = {cell_ids[shag].strip()}
UL Frequency Channel Number = {local_cell_ul_freq[shag].strip()}
DL Frequency Channel Number = {local_cell_dl_freq[shag].strip()}
DL 64QAM Capability = {local_cell_64_qam[shag].strip()}
Normal Beam Capability = {local_cell_normal_beam[shag].strip()}
Massive Beam 4T4R Capability = {local_cell_4t4r_beam[shag].strip()}
Massive Beam 8T8R Capability = {local_cell_8t8r_beam[shag].strip()}
"""
            await bot.send_message(chat_id=chatid, text=f'{text}')
    connection.close()


async def mml_request_dsp_mmctx(number):
    global cell_id
    url = "https://10.15.8.5:31127/api/rest/mmlManagement/v1/command"
    token = get_token()

    payload = json.dumps({
        "command": f'DSP MMCTX:QUERYOPT=BYMSISDN,MSISDN="{number}";',
        "neNames": [
            "241_AMF", "244 AMF",
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': f'{token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    data = response.text
    data_dict = json.loads(data)
    texts = data_dict['results']
    service_area_of_user = []
    gsm_cell_id = []
    for text in texts:
        if "Record does not exist" not in text["report"]:
            eutran_global_identity = re.findall(r'E-UTRAN cell global identity\s+=\s+(.*?)Global eNodeB ID',
                                                text["report"], re.DOTALL)
            try:
                service_area_of_user.append(re.findall(r'Service area of user\s+=\s+(.*?)RNC ID',
                                                       text["report"], re.DOTALL)[0].strip())
                service_area_of_user.append(re.findall(r'RNC ID\s+=\s+(.*?)UMTS Encryption algorithm',
                                                       text["report"], re.DOTALL)[0].strip())
            except:
                pass
            try:
                gsm_cell_id.append(re.findall(r'Cell Id\s+=\s+(.*?)GERAN Encryption algorithm',
                                              text["report"], re.DOTALL)[0].strip())
                gsm_cell_id.append(re.findall(r'RAI\s+=\s+(.*?)Cell Id', text["report"], re.DOTALL)[0].strip())
            except:
                pass
            try:
                return "LTE" + eutran_global_identity[0].strip()
            except:
                try:
                    if len(service_area_of_user):
                        service_area_of_user.append("UMTS")
                        return service_area_of_user
                    else:
                        try:
                            if len(gsm_cell_id):
                                gsm_cell_id.append("GSM")
                                return gsm_cell_id
                        except:
                            pass
                except:
                    pass
        else:
            pass


async def mml_request_dsp_licrate():
    global volte_subs, volte_active_subs
    url = "https://10.15.8.5:31127/api/rest/mmlManagement/v1/command"
    token = get_token()

    payload = json.dumps({
        "command": 'DSP LICRATE:;',
        "neNames": [
            "ATS241_UDMBE01_USCDBUDM"
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': f'{token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    data = response.text
    data_dict = json.loads(data)
    texts = data_dict['results']
    for text in texts:
        if "Record does not exist" not in text["report"]:
            subs = re.findall(
                fr'HSS BE basic SW,Number of HSS BE Subscriptions,Per Subs\s+ \s+(.*?)HSS9860  HSS Data Compression',
                text["report"], re.DOTALL)[0].split(' ')
            volte_subs = subs[0]

    payload = json.dumps({
        "command": 'DSP GURN:;',
        "neNames": [
            "ATS244_ATS01"
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Token': f'{token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    data = response.text
    data_dict = json.loads(data)
    texts = data_dict['results']
    for text in texts:
        if "Record does not exist" not in text["report"]:
            subs = re.findall(r'Number of total registered users\s+=\s+(.*?)Number of total registered Multi-Device users',
                              text["report"], re.DOTALL)[0].strip()
            volte_active_subs = subs

    return str(f"""Количество абонентов VOLTE  - {volte_subs}
Количество активных абонентов VOLTE-{volte_active_subs}""")
