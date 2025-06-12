#William Dunlap
#willdunlapb@gmail.com
#CNE370
#6/12/2025
# Connects to two MariaDB database shards through MaxScale and runs four queries on preloaded zipcode data.

from mysql.connector import connect

db = connect(host="127.0.0.1", port=4000, user="maxuser", password="maxpwd")
cursor = db.cursor()

print("Largest zipcode in zipcodes_one:")
cursor.execute("SELECT Zipcode FROM zipcodes_one.zipcodes_one ORDER BY Zipcode DESC LIMIT 1;")
print(cursor.fetchone())

print("\nZipcodes where state = KY:")
cursor.execute("SELECT Zipcode FROM zipcodes_one.zipcodes_one WHERE State = 'KY';")
print(cursor.fetchall())
cursor.execute("SELECT Zipcode FROM zipcodes_two.zipcodes_two WHERE State = 'KY';")
print(cursor.fetchall())

print("\nZipcodes between 40000 and 41000:")
cursor.execute("SELECT Zipcode FROM zipcodes_one.zipcodes_one WHERE Zipcode BETWEEN 40000 AND 41000;")
print(cursor.fetchall())
cursor.execute("SELECT Zipcode FROM zipcodes_two.zipcodes_two WHERE Zipcode BETWEEN 40000 AND 41000;")
print(cursor.fetchall())

total_wages = []

for schema in ["zipcodes_one", "zipcodes_two"]:
    cursor.execute(f"SELECT TotalWages FROM {schema}.{schema} WHERE State = 'PA';")
    for row in cursor.fetchall():
        if row[0]:  # Skip empty strings or None
            total_wages.append(row[0])

print("\nTotalWages where state = PA:")
for i in range(0, len(total_wages), 10):
    print(", ".join(total_wages[i:i+10]))
