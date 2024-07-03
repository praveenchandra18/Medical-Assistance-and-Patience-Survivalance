from flask import Flask,render_template

app=Flask(__name__)

app.secret_key="jnaskjnakgnjaslgnaskjsnfgkjangkjdfgnkj"

from doctor import doctor_bp
app.register_blueprint(doctor_bp)

from patients import patient_bp
app.register_blueprint(patient_bp)

from docs_around_me import docs_around_me_bp
app.register_blueprint(docs_around_me_bp)

from medicine_remainder import medicine_remainder_bp
app.register_blueprint(medicine_remainder_bp)

from diet_suggestor import suggestor_bp
app.register_blueprint(suggestor_bp)

@app.route('/')
def home():
    return render_template('index.html')

if (__name__=="__main__"):
    app.run(debug=True)