from maps import id_generator,password_encryption 
import mysql.connector
maps_db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Pdnejoh@18",
  database="maps"
)
my_cursor= maps_db.cursor()

name=input("Enter the name of the doctor ")
specialisation=input("Enter the specialisation of the doctor ")
education=input("Enter the education qualifications of the doctor ")
address=input("Enter the address of the hospital ")
mobile=input("Enter the mobile number of the doctor/ hospitals reception ")
password=input("Enter the password the doctor want to set for his account ")
id=id_generator(0)
password=password_encryption(password)
data=[id,name,specialisation,education,address,mobile,password]
query="""insert into doctors(doctor_id,doctor_name,specialisation,education,hospital_address,mobile,password)
         values (%s,%s,%s,%s,%s,%s,%s)"""
my_cursor.execute(query,data)
maps_db.commit()