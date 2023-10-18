import mysql.connector
from mysql.connector import errorcode
import pandas

excel_file = input("Path to File write with / instead of\ : ")
#Set the columns of the Excel file to use
df = pandas.read_excel(excel_file, usecols='A:D')

# Connect to SQL server
connec = mysql.connector.connect(
    user='%user%',
    password='%password%',
    host='%hostaddres%',
    database='%database'
)
try:
    cursor = connec.cursor()
    cursor.execute("SHOW TABLES")
    tabels = []
    for table_name in cursor:
        tabels.append(str(table_name).replace("('", "").replace("',)", ""))
        print(table_name)
    select = input("select carefully!: ")
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
                print("Things Inserted!")
    connec.close()

except mysql.connector.Error as err:
    print(err)
    print("Errored Out!")
