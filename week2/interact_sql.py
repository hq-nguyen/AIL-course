# pip install pymysql
import pyodbc
import pandas as pd
# information for connect
# server = r'DESKTOP-U3ICBLI\HQUAN'
# database = 'AdventureWorks2019'
# username = 'sa'
# password = '303'

import os

server = os.getenv('DB_SERVER', 'localhost')
database = os.getenv('DB_NAME', 'AdventureWorks2019')
username = os.getenv('DB_USER', 'sa')
password = os.getenv('DB_PASSWORD', '303')


# connect to database
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # connect to sql server
    conn = pyodbc.connect(conn_str)
    print('Connected')

    # create cursor
    cursor = conn.cursor()

    # execute query
    query = 'SELECT top(20) [AddressLine1], [City] ,[ModifiedDate] FROM [AdventureWorks2019].[Person].[Address]'
    cursor.execute(query)

    # get all customers
    rows = cursor.fetchall()

    # to DataFrame
    columns = [column[0] for column in cursor.description]
    df = pd.DataFrame.from_records(rows, columns=columns)

    # show data
    print(df)
    
    # Lưu DataFrame thành file CSV
    output_folder = r'....'
    output_file = os.path.join(output_folder, 'Person_Address.csv')

    # Xem xét thư mục lưu data có chưa, nếu chưa thì tạo mới
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Lưu file CSV
    df.to_csv(output_file, index=False)
    print(f"File CSV đã được lưu tại: {output_file}")

except pyodbc.Error as e:
    print(f"Lỗi kết nối hoặc không query được data: {e}")

finally:
    # Đóng kết nối
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
