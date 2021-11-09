import sqlite3

dbpath = 'wwwardrobe.sqlite' # DB's path
connection = sqlite3.connect(dbpath)
cursor = connection.cursor()

tables = ['users', 'wardrobes', 'history_own', 'history_wear', 'weather_today']

for i in tables:
    cursor.execute("SELECT * FROM {};".format(i))
    rows = cursor.fetchall()
    print(i + ' ------------------------------------------------------')
    for j in rows:
        j_list = list(j)
        for k in range(len(j_list)):
            if type(j_list[k]) is int:
                j_list[k] = str(j_list[k])
            elif j_list[k] is None:
                j_list[k] = ""
            elif type(j_list[k]) is float:
                j_list[k] = str(j_list[k])
        print(','.join(list(j_list)))
