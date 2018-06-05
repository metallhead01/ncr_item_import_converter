import sqlite3


string_list = []
string_list_for_comparing = []
counter_2 = 1

db = sqlite3.connect("mydatabase.db")
cur = db.cursor()
cur.execute("""DROP TABLE IF EXISTS import""")
cur.execute("""CREATE TABLE import (ID INTEGER PRIMARY KEY AUTOINCREMENT, Item_Name text)""")
db.commit()
cur.close()

with open("Book5.csv") as book:
    counter = 1
    for line in book:
        insert = counter, line  # создаем кортеж из двух элементов - первый счетчик, второй строка из файла
        string_list.append(tuple(insert))  # делаем кортеж внутри кортежа
        counter += 1
        string_list_for_comparing.append(line)


db = sqlite3.connect("mydatabase.db")
cur = db.cursor()
cur.executemany("""INSERT INTO import VALUES(?,?)""", string_list)
db.commit()
cur.close()

db = sqlite3.connect("mydatabase.db")
cur = db.cursor()
for i in set(string_list_for_comparing):
    cur.execute("SELECT * FROM import WHERE Item_Name LIKE (?)", (i,))
    result = cur.fetchall()
    if len(result) > 1:
        counter_1 = "1"
        for j in result:
            #print(j)
            if len(j[1]) < 20:
                pass
            else:
                split_list = list(j[1])
                split_list[19] = str(counter_1)
                new_element = ''.join(split_list)
                #print(new_element)
                counter_1 = int(counter_1) + 1
                cur.execute("UPDATE import SET Item_Name = (?) WHERE ID = ?", (new_element, j[0]))
    else:
        pass

db.commit()

with open("export.csv", "w") as export:
    while counter_2 <= len(string_list_for_comparing):
        cur.execute("SELECT * FROM import WHERE ID LIKE (?)", (counter_2,))
        export_to_file_string = cur.fetchall()
        print(export_to_file_string)
        if export_to_file_string[0][1][-1] != "\n": # делаем проверку - если последний символ в строке имени товара
            #  не символ перевода строки ("\n" Python читает как один символ, то добавляем его сложением строк)
            export.write(export_to_file_string[0][1]+"\n")
        else:
            export.write(export_to_file_string[0][1])
        counter_2 += 1

cur.close()
