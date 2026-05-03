from flask import Flask, render_template, request, redirect, session 
import pickle
import numpy as np
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mansi555",
    database="career_db"
)

cursor = db.cursor()

app = Flask(__name__)

model, le_skill, le_interest, le_career = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    user = session.get('user')

    skill = request.form['skills']
    interest = request.form['interest']
    marks = int(request.form['marks'])

    skill_encoded = le_skill.transform([skill])[0]
    interest_encoded = le_interest.transform([interest])[0]

    prediction = model.predict([[skill_encoded, interest_encoded, marks]])
    career = le_career.inverse_transform(prediction)[0]

    # Save to DB
    cursor.execute(
        "INSERT INTO predictions (username, skill, interest, marks, result) VALUES (%s,%s,%s,%s,%s)",
        (user, skill, interest, marks, career)
    )
    db.commit()

    return render_template('index.html', result=career)
app.secret_key = "secret123"

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        
        cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)", (user,pwd))
        db.commit()
        
        return redirect('/login')
    return render_template('signup.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user,pwd))
        result = cursor.fetchone()
        
        if result:
            session['user'] = user
            return redirect('/')
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    user = session.get('user')

    cursor.execute("SELECT * FROM predictions WHERE username=%s", (user,))
    data = cursor.fetchall()

    return render_template('dashboard.html', data=data)
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')
if __name__ == "__main__":
    app.run(debug=True)