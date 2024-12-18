import happybase

# Connect to HBase
connection = happybase.Connection('hbase-master')
connection.open()

# Define the table name
table_name = 'wikipedia'

# Get the table object
table = connection.table(table_name)

# Retrieve the row with the row key 'United States'
row_key = 'Anarchism'
row = table.row(row_key.encode('utf-8'))

# Print the row data
# In dữ liệu từng cột trên từng dòng
if row:
    print(f"Row with key '{row_key}':")
    for column, value in row.items():
        print(f"Column: {column.decode('utf-8')}, Value: {value.decode('utf-8')}")
else:
    print(f"No row found with key '{row_key}'")

# Close the connection
connection.close()
