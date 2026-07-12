from flask import Flask,render_template,redirect,request,url_for,flash,session
from werkzeug.security import generate_password_hash,check_password_hash
import mysql.connector
import re
import joblib
import numpy as np
import pandas as pd

app=Flask(__name__)
app.secret_key='12345'

#load saved model and encoder
model=joblib.load("rf_model_delivery_time.pkl")


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="fooddb"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/methodology')
def methodology():
    return render_template('methodology.html')

@app.route('/predict',methods=['GET','POST'])
def predict(): 

    #check login
    if 'user_id' not in session:
        flash("Please login to access the prediction page,","warning")
        return redirect(url_for('login'))
    
    result=0
    
    if request.method == 'POST':
        #Take user input
        Distance_km =float(request.form['distance'])
        Traffic_Level=request.form['traffic']
        Preparation_Time_min=request.form['preparation']
        Courier_Experience_yrs=float(request.form['experience'])
        Weather=request.form['weather']   
        Time_of_Day=request.form['time'] 
        Vehicle_Type=request.form['vehicle']

        if Traffic_Level=='High':
            Traffic_Level=0
        elif Traffic_Level=='Low':
            Traffic_Level=1
        else:
            Traffic_Level=2  

        Weather_Clear, Weather_Foggy,Weather_Rainy,Weather_Snowy,Weather_Windy=0,0,0,0,0
        if Weather=='Clear':
            Weather_Clear=1
        elif Weather=='Foggy':
            Weather_Foggy=1
        elif Weather=='Rainy':
            Weather_Rainy=1
        elif Weather=='Snowy':
            Weather_Snowy=1    
        else:
            Weather_Windy=1 

        Time_of_Day_Afternoon,Time_of_Day_Evening,Time_of_Day_Morning,Time_of_Day_Night=0,0,0,0
        if Time_of_Day=='Afternoon':
         Time_of_Day_Afternoon=1
        elif Time_of_Day=='Evening':
            Time_of_Day_Evening=1
        elif Time_of_Day=='Morning':
            Time_of_Day_Morning=1  
        else:
             Time_of_Day_Night=1 

        Vehicle_Type_Bike,Vehicle_Type_Car,Vehicle_Type_Scooter=0,0,0
        if Vehicle_Type=='Bike':
            Vehicle_Type_Bike=1
        elif Vehicle_Type=='Car':
            Vehicle_Type_Car=1    
        else:
            Vehicle_Type_Scooter=1  

        data=pd.DataFrame([[Distance_km,Traffic_Level,Preparation_Time_min,
            Courier_Experience_yrs, Weather_Clear,Weather_Foggy,Weather_Rainy,
            Weather_Snowy,Weather_Windy,Time_of_Day_Afternoon, Time_of_Day_Evening, 
            Time_of_Day_Morning,Time_of_Day_Night,Vehicle_Type_Bike,Vehicle_Type_Car,
            Vehicle_Type_Scooter]],columns=['Distance_km', 'Traffic_Level', 'Preparation_Time_min',
            'Courier_Experience_yrs', 'Weather_Clear', 'Weather_Foggy',
            'Weather_Rainy', 'Weather_Snowy', 'Weather_Windy',
            'Time_of_Day_Afternoon', 'Time_of_Day_Evening', 'Time_of_Day_Morning',
            'Time_of_Day_Night', 'Vehicle_Type_Bike', 'Vehicle_Type_Car',
            'Vehicle_Type_Scooter'])

        result=model.predict(data)[0] 
        result=f"Estimated Delivery Time:(prediction,2) minutes"
        
        
    return render_template('predict.html',prediction_text=result)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        uname=request.form['uname']
        email=request.form['email']
        password=request.form['password']

        # Basic validation
        if not uname.strip():
            flash("username is required","danger")
            return redirect(url_for('register'))
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
            flash("Invalid email address","danger")
            return redirect(url_for('register'))
        
        if len(password)<6:
            flash("password must be atleast 6 character","danger")
            return redirect(url_for('register'))   
        hashed_password=generate_password_hash(password)
        conn=get_db_connection()
        cursor=conn.cursor()

        # check existing email
        cursor.execute("SELECT u_id FROM users WHERE email=%s",(email,))
        if cursor.fetchone():
            flash("Email already registered","danger")
            cursor.close()
            conn.close()
            return redirect(url_for('register'))
        
        # Insert user
        cursor.execute(
            "INSERT INTO users (uname, email, password) VALUES (%s, %s, %s)",
            (uname, email, hashed_password)
        )
        conn.commit()

        cursor.close()
        conn.close()

        flash("Registration Successfull.Please Login.","success")
        return redirect(url_for('login'))


    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
         
        if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
            flash("Invalid email address","danger")
            return redirect(url_for('register'))
        
        if len(password)<6:
            flash("password must be atleast 6 character","danger")
            return redirect(url_for('register')) 
        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
        user=cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'],password):
            session['user_id']=user['u_id']
            session['username']=user['uname']
            return redirect(url_for('index'))
        else:
            flash("invalid email or password","danger")
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True, port=4000)
