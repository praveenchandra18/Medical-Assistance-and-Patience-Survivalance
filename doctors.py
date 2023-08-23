from flask import Flask,render_template, request, redirect, session, Blueprint
from dependencies import my_cursor,password_encryption

doctor_bp=Blueprint('doctor',__name__)

@doctor_bp.route('/doctors_interface')
def doctors_login():
    return render_template('doctors_interface.html')

@doctor_bp.route('/doctor_check',methods=['POST','GET'])
def doctor_check():
    docid=request.form['username']
    password=request.form['password']
    query="""select * from doctors where doctor_id=%s"""
    data=[docid]
    my_cursor.execute(query,data)
    lst=my_cursor.fetchall()
    if len(lst)==0:
        message="User not found!!"
        return render_template('doctors_interface.html',message=message)
    elif(lst[0][6]==password_encryption(password)):
        # return render_template('doctor_portal.html',list=lst[0])
        session[docid]=lst[0]
        return redirect(f"maps/doctor_interface/{docid}")
    else:
        message="Incorrect Credentials!!"
        return render_template('doctors_interface.html',message=message)

@doctor_bp.route('/maps/doctor_interface/<docid>')
def doctor_details(docid):
    data=session.get(docid)
    session.pop(docid)
    return render_template('doctor_portal.html',list=data)


@doctor_bp.route('/add_report_check')
def add_report_check():
    return render_template('add_report_check.html')

@doctor_bp.route('/add_report',methods=['POST'])
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