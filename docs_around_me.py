from flask import Flask,render_template,request,redirect,session,Blueprint
from dependencies import my_cursor

docs_around_me_bp=Blueprint('docs_around_me',__name__)

@docs_around_me_bp.route('/docs_around_me')
def doctors_around_me():
    return render_template('docs_around_me.html')

@docs_around_me_bp.route('/docs_around_you',methods=['POST'])
def doctors_around_you():    
    city=request.form['city_name']
    specialist=request.form['specialist_type']
    # query="select * from doctors where specialisation=%s and hospital_address=%s;"
    query="""SELECT * FROM hospitals
        WHERE LOCATE(%s, address) > 0;"""
    data=[city]
    # data=[specialist,city]
    my_cursor.execute(query,data)
    lst=my_cursor.fetchall()
    Doctors=[]
    for i in lst:
        query="""Select * from doctors where specialisation=%s and hospital_id=%s"""
        data=[specialist,i[0]]
        my_cursor.execute(query,data)
        for j in my_cursor.fetchall():
            Doctors.append([j[0],j[1],j[2],j[3],i[1],i[2],i[3],i[4]])
    return render_template('docs_around_you.html',list=Doctors)