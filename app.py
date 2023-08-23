from flask import Flask,render_template, request, redirect, session
app=Flask(__name__)
app.secret_key="jnaskjnakgnjaslgnaskjsnfgkjangkjdfgnkj"

import mysql.connector
maps_db=mysql.connector.connect(
  host="localhost",
  user="root",
  password="Pdnejoh@18",
  database="maps"
)
my_cursor=maps_db.cursor()

import hashlib
import datetime

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

@app.route('/')
@app.route('/maps')
def home():
    return render_template('index.html')

@app.route('/maps/patient_login')
def patient_login():
    return render_template('patient_login.html')

@app.route('/patient_check',methods=['GET','POST'])
def patient_check():
    userid=request.form['username']
    entered_password=request.form['password']

    query="""select * from patients where patient_id=%s"""
    data=[userid]
    my_cursor.execute(query,data)
    lst=my_cursor.fetchall()
    if len(lst)==0:
        message="No such user.Please use sign up"
        return render_template('patient_login.html',message=message)
        # return render_template('patient_login.html',message)
    elif(str(lst[0][0])==userid and lst[0][5]!=password_encryption(entered_password)):
        message="Wrong password. Try again!!"
        return render_template('patient_login.html',message=message)
    elif (lst[0][5]==password_encryption(entered_password) and str(lst[0][0])==userid):
        session[userid]=lst[0]
        return redirect(f"/maps/{userid}")
    
@app.route('/maps/<userid>')
def patient_details(userid):
    data=session.get(userid)
    session.pop(userid)
    return render_template('patient_portal.html',list=data)
    
if __name__=='__main__':
    app.run(debug=True)