from flask import Flask,render_template, request, redirect, session, Blueprint
from dependencies import my_cursor,password_encryption,maps_db,id_generator

patient_bp=Blueprint('patient',__name__)

@patient_bp.route('/patient_interface')
def patient_login():
    return render_template('patient_interface.html')

@patient_bp.route('/patient_check',methods=['GET','POST'])
def patient_check():
    userid=request.form['username']
    entered_password=request.form['password']
    query="""select * from patients where patient_id=%s"""
    data=[userid]
    my_cursor.execute(query,data)
    lst=my_cursor.fetchall()
    if len(lst)==0:
        message="No such user.Please use sign up"
        return render_template('patient_interface.html',message=message)
        # return render_template('patient_login.html',message)
    elif(str(lst[0][0])==userid and lst[0][5]!=password_encryption(entered_password)):
        message="Wrong password. Try again!!"
        return render_template('patient_interface.html',message=message)
    elif (lst[0][5]==password_encryption(entered_password) and str(lst[0][0])==userid):
        session[userid]=lst[0]
        return redirect(f"/patient_interface/{userid}")
    
@patient_bp.route('/patient_interface/<userid>')
def patient_details(userid):
    data=session.get(userid)
    session.pop(userid)
    return render_template('patient_portal.html',list=data)

@patient_bp.route('/patient_interface/signup')
def patient_signup():
    return render_template('patient_signup.html')

@patient_bp.route('/patient_interface/signup_process',methods=['POST'])
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
    display=""" Your account is created
                Please note your id number """+str(id)
    return render_template('patient_signup.html',message=display)
    