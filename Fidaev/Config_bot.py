bot_token = "1803232589:AAFSJ_sF1mZKrC_77r4BjmC55H-MR-LcN7I"
admin_id = 98908667

host = "129.20.0.199"
pguser = "postgres"
password = "wireles"
db_name = "wireless"

Userlist = {
    '98908667': 'Jaloliddin Fidaev',
    '51665305': 'Farrux Abdullaev',
    '196120188': 'Aziz Turdiev',
    '55226487': 'Elyor Abdukadirov',
    '138238312': 'Davron Mirzaev',
    '463272027': 'Azizxon Fatkhullakhudjaev',
    '173477426': 'Abduxakim Abdazov',
    '2224478': 'Aziz Kadirov',
    '409102496': 'Iskander Kadiraliev',
    '85569107': 'Zafar Mansurov',
    '427471753': 'Vadim Krivov',
}

users = [98908667, 51665305, 196120188, 55226487,
         138238312, 463272027, 173477426, 2224478, 409102496,
         85569107, 427471753]


def username(userid):
    return f"User id: {userid}" \
           f"\nUser name: {(Userlist.get(f'{userid}'))}"


Test_ID = 2116163519
Farrux_Abdullaev = 51665305
Aziz_Turdiev = 196120188
Elyor_Abdukadirov = 55226487
Davron_Mirzaev = 138238312
Azizxon_Fatkhullakhudjaev = 463272027
Abduxakim_Abdazov = 173477426
Aziz_Kadirov = 2224478
Iskander_Kadiraliev = 409102496
Zafar_Mansurov = 85569107
Vadim_Krivov = 427471753
