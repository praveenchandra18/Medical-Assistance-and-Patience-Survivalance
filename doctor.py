from flask import Blueprint, render_template,request,session,redirect,url_for
from dependencies import my_cursor,maps_db,password_encryption
from datetime import datetime

doctor_bp=Blueprint('doctor',__name__)

@doctor_bp.route('/doctors_interface')
def doctor_interface():
    cookie=request.cookies.get('doc_data')
    if(cookie):
        docid=session['doc_data'][0]
        return redirect(f"dashboard/{docid}")
    return render_template("doctors_interface.html")

@doctor_bp.route('/doctor_check',methods=['GET','POST'])
def doctor_check():
    docid=request.form['username']
    password=request.form['password']
    query="""select * from doctors where doctor_id=%s"""
    data=[docid]
    my_cursor.execute(query,data)
    lst=my_cursor.fetchall()
    print(lst)
    if len(lst)==0:
        message="User not found!!"
        # return redirect(url_for('doctor_interface'),message=message)
        return render_template('doctors_interface.html',message=message)
    elif(lst[0][4]==password_encryption(password)):
        # session[docid]=lst[0]
        query="select hospital_name from hospitals where hospital_id=%s"
        data=[lst[0][5]]
        my_cursor.execute(query,data)
        hospital_name=my_cursor.fetchall()[0][0]
        session['doc_data']=[lst[0][0],lst[0][1],lst[0][2],lst[0][3],lst[0][5],hospital_name]
        # session['docid']=docid
        # print(session['docid'])
        responce=redirect(f"dashboard/{docid}")
        responce.set_cookie('doc_data',docid,max_age=30)
        return responce
    else:
        message="Incorrect Credentials!!"
        return render_template('doctors_interface.html',message=message)
    
@doctor_bp.route('/dashboard/<docid>')
def doctor_details(docid):
    data=session.get('doc_data')
    # print("This is the data that is printed ",data)
    return render_template('doctor_portal.html',list=data)

@doctor_bp.route('/past_records',methods=['POST'])
def past_records():
    docid=session['doc_data'][0]
    userid=request.form['username']
    password=request.form['password']
    query="""select * from patients where patient_id=%s"""
    data=[userid]
    my_cursor.execute(query,data)
    lst=my_cursor.fetchall()
    if len(lst)==0:
        # message="No such user.Please use sign up"
        # return redirect(url_for(f"dashboard/{docid}"))
        return '<p>No such user exists!!<p>'
    elif(str(lst[0][0])==userid and lst[0][5]!=password_encryption(password)):
        # message="Wrong password. Try again!!"
        return '<p>Wrong Password!!<p>'
    elif (lst[0][5]==password_encryption(password) and str(lst[0][0])==userid):
        session['pat_data']=lst[0]
        session['pat_id']=lst[0][0]
        return redirect(f"/patient_interface/{userid}")
    

@doctor_bp.route('/add_report_doctor_check',methods=['POST'])
def add_report_doctor_check():
    userid=request.form['username']
    entered_password=request.form['password']
    query="""select * from patients where patient_id=%s"""
    data=[userid]
    my_cursor.execute(query,data)
    lst=my_cursor.fetchall()
    if len(lst)==0:
        # message="No such user.Please use sign up"
        return '<p>No such user exists!!<p>'
    elif(str(lst[0][0])==userid and lst[0][5]!=password_encryption(entered_password)):
        # message="Wrong password. Try again!!"
        return '<p>Wrong Password!!<p>'
    elif (lst[0][5]==password_encryption(entered_password) and str(lst[0][0])==userid):
        session['pat_data']=lst[0]
        session['pat_id']=lst[0][0]
        return redirect(f"/patient_interface/{userid}/add_report")
    
@doctor_bp.route("/patient_interface/<userid>/add_report")
def add_report(userid):
    return render_template("report.html")

@doctor_bp.route("/submit_report", methods=['GET','POST'])
def submit_report():
    tests=request.form.getlist("tests_suggested")
    description=request.form.get("description")
    medicines=request.form.getlist("medicine[]")
    schedules=[]
    for i in range(len(medicines)):
        medicine_schedule = request.form.getlist("schedule" + str(i + 1))
        # schedules.append(medicine_schedule)
        schedules.append(''.join(medicine_schedule))
    tests=','.join(tests)
    schedules=','.join(schedules)
    medicines=','.join(medicines)

    docid=session['doc_data'][0]
    print(docid)
    sql_query="""Select doctor_name from doctors
                    where doctor_id=%s;"""
    data=[docid]
    my_cursor.execute(sql_query,data)
    doc_name=my_cursor.fetchall()
    print(doc_name)

    #  To add the data into the prescriptions 
    sql_query=""" INSERT INTO medical_prescriptions(patient_id,doctor_id,tests_done,problem_description,medicines_given,medicines_schedule,doctor_name)
                    VALUES (%s,%s,%s,%s,%s,%s,%s);"""

    patid=session['pat_id']
    data=(patid,docid,tests,description,medicines,schedules,doc_name[0][0])
    my_cursor.execute(sql_query,data)
    maps_db.commit()

    # To get the record id
    sql_query="""SELECT * FROM medical_prescriptions
                WHERE patient_id = %s and doctor_id= %s
                ORDER BY record_id DESC
                LIMIT 1;"""
    data=(patid,docid)
    my_cursor.execute(sql_query,data)
    lst=my_cursor.fetchall()
    record_id=lst[0][0]
    print(lst)

    # To get the files into the test results tables
    files=request.files.getlist('file')
    print(files)
    for file in files:
        file_data=file.read()
        if(file_data):
            sql_query="""INSERT INTO test_results(record_id,patient_id,result_image)
                            VALUES(%s,%s,%s)"""
            data=(record_id,patid,file_data)
            my_cursor.execute(sql_query,data)
            maps_db.commit()
    
    data=session.get('doc_data')
    return render_template('doctor_portal.html',list=data,message="Submitted successfully!!     ")

