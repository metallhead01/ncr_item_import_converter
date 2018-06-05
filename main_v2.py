import pyodbc
import csv


dict_mssql = {}
list_csv_file = []

conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=WRURA185201-5ZJ;"
                      "Database=RusMerchant001;"
                      "Trusted_Connection=yes;")

cursor = conn.cursor()
cursor.execute('SELECT * FROM ItemMaster WHERE MerchantId = 600006')

for row in cursor:
    dict_mssql[row[1]] = row[8]
print(dict_mssql)


with open("import.csv", newline='') as f:
    reader = csv.DictReader(f, delimiter=',')
    for line in reader:
        list_csv_file.append(line["BARCODE"])

counter = 0
for i in dict_mssql:
    if dict_mssql.get(i) is not None and ("0" + dict_mssql.get(i)) in list_csv_file:
        cursor.execute("UPDATE ItemMaster SET BarCode = (?) WHERE ItemMasterId=(?)", ("0" + dict_mssql.get(i), i))
        counter += 1
conn.commit()
cursor.close()
print(counter)
