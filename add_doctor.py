from dependencies import id_generator,password_encryption
from dependencies import my_cursor,maps_db
# import mysql.connector

name=input("Enter the name of the doctor ")
specialisation=input("Enter the specialisation of the doctor ")
education=input("Enter the education qualifications of the doctor ")
# address=input("Enter the address of the hospital ")
# mobile=input("Enter the mobile number of the doctor/ hospitals reception ")
password=input("Enter the password the doctor want to set for his account ")
hospital_id=int(input("Enter the hospital id "))
id=id_generator(0)
password=password_encryption(password)
data=[id,name,specialisation,education,password,hospital_id]
query="""insert into doctors(doctor_id,doctor_name,specialisation,education,password,hospital_id)
         values (%s,%s,%s,%s,%s,%s)"""
my_cursor.execute(query,data)
maps_db.commit()
print("Added doctor to the database")