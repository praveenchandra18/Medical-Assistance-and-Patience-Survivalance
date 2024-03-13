from flask import Flask,Blueprint,render_template,request,session,redirect
from dependencies import *
medicine_remainder_bp=Blueprint('medicine_remainder',__name__)

@medicine_remainder_bp.route('/medicine_remainder')
def fun():
    return render_template("medicine_remainder_register_page.html")

@medicine_remainder_bp.route('/medicine_remainder_check',methods=['GET','POST'])
def patient_check():
    userid=request.form['username']
    entered_password=request.form['password']
    query="""select * from patients where patient_id=%s"""
    data=[userid]
    my_cursor.execute(query,data)
    lst=my_cursor.fetchall()
    if len(lst)==0:
        message="No such user. Please use sign up in patients interface portal"
        return render_template('medicine_remainder_register_page.html',message=message)
    elif(str(lst[0][0])==userid and lst[0][5]!=password_encryption(entered_password)):
        message="Wrong password. Try again!!"
        return render_template('medicine_remainder_register_page.html',message=message)
    elif (lst[0][5]==password_encryption(entered_password) and str(lst[0][0])==userid):
        message="You have registered succesfully !!"
        return render_template('medicine_remainder_register_page.html',message=message)