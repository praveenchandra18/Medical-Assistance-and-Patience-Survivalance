from dependencies import id_generator,password_encryption
from dependencies import my_cursor,maps_db

hospital_name=input("Enter the name of the hospital")
location=input("Enter the location of the hospital")
contact=input("Enter the contact number of the hospital")
address=input("Enter the hospital address")
password=input("Enter the password you would like to use it for the hospital login")
password=password_encryption(password)
data=[hospital_name,location,contact,address,password]
query="""insert into hospitals(hospital_name,location,contact_number,address,password)
         values (%s,%s,%s,%s,%s)"""
my_cursor.execute(query,data)
maps_db.commit()
print("Added hospital to the server")
lastrowid=my_cursor.lastrowid
print(lastrowid)