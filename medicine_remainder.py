from flask import Flask,Blueprint,render_template,request,session,redirect
from dependencies import *
from twilio.rest import Client
import schedule
import time
from functools import partial

# maps_db=mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Pdnejoh@18",
#     database="maps"
#     )

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
        sql_query="""select medicines_given, medicines_schedule from medical_prescriptions
                    where patient_id=%s
                    order by record_id desc
                    limit 1;"""
        data=[lst[0][0]]
        my_cursor.execute(sql_query,data)
        medicine_data=my_cursor.fetchall()
        print(medicine_data)

        if(len(medicine_data)==0):
            message="You don't have any recent medications !"
            return render_template('medicine_remainder_register_page.html',message=message)

        sql_query="""INSERT INTO medicine_remainder (patient_id, medicines, schedule, days_remaining, mobile_number)
                VALUES (%s,%s,%s,%s,%s);"""
        data=[lst[0][0],medicine_data[0][0],medicine_data[0][1],3,lst[0][4]]
        my_cursor.execute(sql_query,data)
        maps_db.commit()
        return render_template('medicine_remainder_register_page.html',message=message)
    
def send_message(code):
    account_sid = 'account_sid'
    auth_token = 'auth_token'
    client = Client(account_sid, auth_token)

    my_cursor2=maps_db.cursor()
    sql_query="select * from medicine_remainder;"
    my_cursor2.execute(sql_query)
    lst=my_cursor2.fetchall()
    # maps_db.commit()
    print(lst)
    
    for i in lst:
        medicines=i[1].split(',')
        schedule=i[2].split(',')
        result=[]
        for j in range(len(medicines)):
            if(code in schedule[j]):
                result.append(medicines[j])
            print(result)
    
        message = client.messages.create(
            from_='+19094803354',
            body="Dont forget to take your medicines: "+','.join(result),
            to='+91'+i[4]
            )
    print("sent message")
    if(code=='2'):
        sql_query1="""UPDATE medicine_remainder
                    SET days_remaining = days_remaining - 1;
                    delete * from medicine_remainder
                    where days_remaining = 0;
                    """
        my_cursor2.execute(sql_query1)
        lst=my_cursor2.fetchall()
        print("done")
        # maps_db.commit()


if __name__ == "__main__":

    send_message_1_partial = partial(send_message, code='0')
    send_message_2_partial = partial(send_message, code='1')
    send_message_3_partial = partial(send_message, code='2')

    schedule.every().day.at("11:31").do(send_message_1_partial)
    schedule.every().day.at("11:32").do(send_message_2_partial)
    schedule.every().day.at("11:33").do(send_message_3_partial)

    while True:
        schedule.run_pending()
        time.sleep(1)