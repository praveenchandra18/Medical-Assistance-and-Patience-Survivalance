import datetime
import hashlib
from flask import Flask,render_template,request
import mysql.connector
maps_db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Pdnejoh@18",
  database="maps"
)
my_cursor= maps_db.cursor()

app=Flask(__name__)

def id_generator(code):
    if(code==0):
        my_cursor.execute("SELECT MAX(doctor_id) FROM doctors")
        result = my_cursor.fetchone()[0]
        if(result==None):
            return 100000000
        else:
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
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/patient_signup')
def new_patient():
    return render_template('patient_signup.html')

@app.route('/patient_login')
def patient_login():
    return render_template("patient_login.html")

@app.route('/patient_details',methods=['POST','GET'])
def patient_details():
    id=request.form['username']
    entered_password=request.form['password']
    query="""select * from patients where patient_id=%s"""
    data=[id]
    my_cursor.execute(query,data)
    lst=my_cursor.fetchall()
    if(lst[0][5]==password_encryption(entered_password) and lst[0][0]==20000000):
        return render_template('patient_portal.html',list=lst[0])
    elif(lst[0][5]==password_encryption(entered_password) and lst[0][0]!=20000000):
        return render_template('patient_portals.html',list=lst[0])
    else:
        return "<h2>pass not matched</h2>"

@app.route('/patient_added',methods=['POST'])
def patient_added():
    name = request.form['name']
    dob = request.form['dob']
    address = request.form['address']
    mobile=request.form['mobile']
    password=request.form['password']
    password=password_encryption(password)
    id=id_generator(1)
    my_data="""INSERT INTO patients (patient_id, patient_name, dob, address, mobile, password)
                VALUES (%s,%s,%s,%s,%s,%s);"""
    data=(id,name,dob,address,mobile,password)
    my_cursor.execute(my_data,data)
    maps_db.commit()
    display=""" <h2>New patient is added to the database<h2><br><br>
                <p>Please note your id number """+str(id)+"""</p>
                <p><a href="http://127.0.0.1:5000/patient_login">Go back to login page</a></p>"""
    return display

@app.route('/doctors_login')
def doctors_login():
    return render_template('doctors_login.html')

@app.route('/doctors_portal',methods=['POST'])
def doctors_portal():
    id=request.form['username']
    password=request.form['password']
    query="""select * from doctors where doctor_id=%s"""
    data=[id]
    my_cursor.execute(query,data)
    lst=my_cursor.fetchall()
    if len(lst)==0:
        return "<h2>No such user</h2>"
    elif(lst[0][6]==password_encryption(password)):
        return render_template('doctor_portal.html',list=lst[0])
    else:
        return "<h2>pass not matched</h2>"

@app.route('/docs_around_me')
def doctors_around_me():
    return render_template('docs_around_me.html')

@app.route('/docs_around_you',methods=['POST'])
def doctors_around_you():    
    city=request.form['city_name']
    specialist=request.form['specialist_type']
    query="select * from doctors where specialisation=%s and hospital_address=%s;"
    data=[specialist,city]
    my_cursor.execute(query,data)
    lst=my_cursor.fetchall()
    return render_template('docs_around_you.html',list=lst)

@app.route('/add_report_check')
def add_report_check():
    return render_template('add_report_check.html')

@app.route('/add_report',methods=['POST'])
def add_report():
    id=request.form['username']
    password=request.form['password']
    query="""select * from patients where patient_id=%s"""
    data=[id]
    my_cursor.execute(query,data)
    lst=my_cursor.fetchall()
    if(lst[0][5]==password_encryption(password)):
        return render_template('add_report.html')
    else:
        return "<h2>pass not matched</h2>"

@app.route('/medicine_remainder')
def medicine_remainder():
    "'This program is to suggest medicines for patients. Kind of self medication. Thinking to use ML algos'"
    return "<h2>This part of website is under construction</h2>"

@app.route('/food_suggestor')
def food_suggestor():
    return "<h2>This part of website is under construction</h2>"

# add_report()
if(__name__=='__main__'):
    app.run(debug=True)