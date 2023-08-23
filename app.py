from dependencies import my_cursor,password_encryption,id_generator,maps_db
from flask import Flask,render_template, request, redirect, session
app=Flask(__name__)
app.secret_key="jnaskjnakgnjaslgnaskjsnfgkjangkjdfgnkj"

from doctors import doctor_bp
app.register_blueprint(doctor_bp)

from patients import patient_bp
app.register_blueprint(patient_bp)

@app.route('/')
def home():
    return render_template('index.html')

if (__name__=="__main__"):
    app.run(debug=True)