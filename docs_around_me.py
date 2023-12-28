from flask import Flask,render_template,request,redirect,session,Blueprint
from dependencies import my_cursor

docs_around_me_bp=Blueprint('docs_around_me',__name__)

@docs_around_me_bp.route('/maps/docs_around_me')
def doctors_around_me():
    return render_template('docs_around_me.html')

@docs_around_me_bp.route('/maps/docs_around_you',methods=['POST'])
def doctors_around_you():    
    city=request.form['city_name']
    specialist=request.form['specialist_type']
    query="select * from doctors where specialisation=%s and hospital_address=%s;"
    data=[specialist,city]
    my_cursor.execute(query,data)
    lst=my_cursor.fetchall()
    return render_template('docs_around_you.html',list=lst)