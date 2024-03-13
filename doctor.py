from flask import Flask, Blueprint, render_template,request,session,redirect,url_for
from dependencies import my_cursor,password_encryption

doctor_bp=Blueprint('doctor',__name__)

@doctor_bp.route('/doctors_interface')
def doctor_interface():
    cookie=request.cookies.get('docid')
    if(cookie):
        docid=session['docid']
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
    if len(lst)==0:
        message="User not found!!"
        # return redirect(url_for('doctor_interface'),message=message)
        return render_template('doctors_interface.html',message=message)
    elif(lst[0][6]==password_encryption(password)):
        session[docid]=lst[0]
        session['docid']=docid
        responce=redirect(f"dashboard/{docid}")
        responce.set_cookie('docid',docid,max_age=30)
        return responce
    else:
        message="Incorrect Credentials!!"
        return render_template('doctors_interface.html',message=message)
    
@doctor_bp.route('/dashboard/<docid>')
def doctor_details(docid):
    data=session.get(docid)
    return render_template('doctor_portal.html',list=data,docid=docid)

@doctor_bp.route('/past_records',methods=['POST'])
def past_records():
    docid=session['docid']
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
        session[userid]=lst[0]
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
        session[userid]=lst[0]
        return redirect(f"/patient_interface/{userid}/add_report")
    
@doctor_bp.route("/patient_interface/<userid>/add_report")
def add_report(userid):
    return render_template("report.html")