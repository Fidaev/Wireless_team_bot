bot_token = "token"
admin_id = "admin_id"

host = "111.222.333.444"
pguser = "postgres"
password = "wireles"
db_name = "wireless"

Userlist = {
    '111': 'Jaloliddin Fidaev',
    '222': 'Farrux Abdullaev',
    '333': 'Aziz Turdiev',
    '444': 'Elyor Abdukadirov',
    '555': 'Davron Mirzaev',
    '666': 'Azizxon Fatkhullakhudjaev',
    '777': 'Abduxakim Abdazov',
    '888': 'Aziz Kadirov',
    '999': 'Iskander Kadiraliev',
    '000': 'Zafar Mansurov',
    '123': 'Vadim Krivov',
}

users = [111, 222, 333, 444,
         555, 666, 777, 888, 999,
         000, 1232]


def username(userid):
    return f"User id: {userid}" \
           f"\nUser name: {(Userlist.get(f'{userid}'))}"


Test_ID = 111
Farrux_Abdullaev = 222
Aziz_Turdiev = 333
Elyor_Abdukadirov = 444
Davron_Mirzaev = 555
Azizxon_Fatkhullakhudjaev = 666
Abduxakim_Abdazov = 777
Aziz_Kadirov = 888
Iskander_Kadiraliev = 999
Zafar_Mansurov = 000
Vadim_Krivov = 123
