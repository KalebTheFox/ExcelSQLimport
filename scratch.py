import mysql.connector
from mysql.connector import errorcode
import pandas
import time

excel_file = input("Pfad zur datei angeben mit /: ")
df = pandas.read_excel(excel_file, usecols='A:D')

# Verbindung zu SQL server aufbauen
connec = mysql.connector.connect(
    user='root',
    password='Pwd.08/15',
    host='127.0.0.1',
    database='aufgabe'
)
try:
    cursor = connec.cursor()
    cursor.execute("SHOW TABLES")
    tabels = []
    for table_name in cursor:
        tabels.append(str(table_name).replace("('", "").replace("',)", ""))
        print(table_name)
    select = input("select carefully!: ")
    # Display
    for table_name in tabels:
        print(str(table_name) + " == " + select + ": " + str(str(table_name) == select))
        if table_name == select:
            query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
            cursor.execute(query)
            column_names = [row[0] for row in cursor.fetchall()]
            print(column_names)
            columns = str(column_names).replace("[", "").replace( "]", "").replace("'", "")
            for _, row in df.iterrows():
                sql = f"INSERT INTO {select} ({columns}) VALUES (%s, %s, %s, %s)"
                values = [row[column_names[0]], row[column_names[1]], row[column_names[2]], row[column_names[3]]]
                print(sql)
                print(values)
                cursor.execute(sql, values)
                connec.commit()
                print("Datein eingefühlt")
    connec.close()

except mysql.connector.Error as err:
    print(err)
    print("fck")
