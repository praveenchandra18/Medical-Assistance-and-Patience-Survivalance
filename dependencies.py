import hashlib
import mysql.connector
maps_db=mysql.connector.connect(
  host="localhost",
  user="root",
  password="Pdnejoh@18",
  database="maps"
)
my_cursor=maps_db.cursor()

def id_generator(code):
    if(code==0):
        my_cursor.execute("SELECT MAX(doctor_id) FROM doctors")
        result = my_cursor.fetchone()[0]
        return int(result)+1
    else:
        my_cursor.execute("SELECT MAX(patient_id) FROM patients")
        result = my_cursor.fetchone()[0]
        return int(result)+1

def password_encryption(password):
    password=str(password)
    hashed_password=hashlib.sha256(password.encode()).hexdigest()
    return hashed_password