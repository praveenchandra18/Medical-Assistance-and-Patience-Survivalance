from flask import Flask,render_template, request, redirect, session, Blueprint
from dependencies import my_cursor,password_encryption,maps_db,id_generator
import base64
from datetime import datetime

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
        session['pat_data']=lst[0]
        session['pat_id']=lst[0][0]
        return redirect(f"/patient_interface/{userid}")
    
@patient_bp.route('/patient_interface/<userid>')
def patient_details(userid):
    data=session.get('pat_data')
    # print(data)
    # session.pop('user_data')
    sql_query="""select * from medical_prescriptions
                 where patient_id=%s
                 order by record_id desc;"""
    query_data=[session['pat_id']]
    my_cursor.execute(sql_query,query_data)
    lists_of_lists=my_cursor.fetchall()
    record_ids=[i[0] for i in lists_of_lists]
    if(len(record_ids)==0):
        return render_template('patient_portal.html',list=data)
    # sql_query2 = "SELECT * FROM test_results WHERE record_id IN (%s)" % (",".join(["%s"] * len(record_ids))) + "order by record_id desc;"
    sql_query2 = "SELECT * FROM test_results WHERE record_id IN (%s) " % (",".join(["%s"] * len(record_ids))) + "ORDER BY record_id DESC;"
    my_cursor.execute(sql_query2,record_ids)
    images_lst=my_cursor.fetchall()
    images={}
    for i in range(len(images_lst)):
        if(images_lst[i][1] in images):
            images[images_lst[i][1]].append(images_lst[i][3])
        else:
            images[images_lst[i][1]]=[images_lst[i][3]]
    
    images_lst=[]
    for i in images:
        images_lst.append(images[i])

    result_images=[[base64.b64encode(j).decode('utf-8') for j in i] for i in images_lst]
    date_object = datetime.strptime(data[2], "%a, %d %b %Y %H:%M:%S %Z")
    date = date_object.date()
    return render_template('patient_portal.html',list=data , list_of_lists=lists_of_lists,images=result_images,date=date)

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
    