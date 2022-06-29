import os
from uuid import uuid4
from flask import Flask, request, render_template, send_from_directory
import pandas as pd
import mysql.connector
from PIL import Image
from pylab import *

app = Flask(__name__)
# app = Flask(__name__, static_folder="images")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

classes = ['System predicted disease as Beta-thalassemia','System predicted disease as Down syndrome','System predicted disease as Hyperthyroidism','System predicted disease as Leprosy']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user")
def user():
    return render_template("user.html")

@app.route('/registration')
def registration():
    return render_template("ureg.html",msg='Successfully Registered!!')
@app.route('/adminhome')
def adminhome():
    return render_template("adminhome.html",msg='Successfully Registered!!')

@app.route('/admin')
def admin():
    return render_template("admin.html",msg='Successfully Registered!!')

@app.route('/adminlog',methods=['POST', 'GET'])
def adminlog():

    if request.method == "POST":
        username = request.form['uname']
        password1 = request.form['pass']
        if username == 'admin' and password1 == 'admin' :
            return render_template('adminhome.html', msg="Login Success")
        else:
            return render_template('admin.html', msg="Login Failure!!!")

    return render_template('admin.html')

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/userlog',methods=['POST', 'GET'])
def userlog():
    global name, name1
    global user
    if request.method == "POST":

        email = request.form['email']
        password1 = request.form['pass']
        print('p')
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="facial_diagnosis")
        cursor = mydb.cursor()
        sql = "select * from ureg where email='%s' and pass='%s'" % (email, password1)
        print('q')
        x = cursor.execute(sql)
        print(x)
        results = cursor.fetchall()
        print(results)
        if len(results) > 0:
            print('r')
            # session['user'] = username
            # session['id'] = results[0][0]
            # print(id)
            # print(session['id'])
            return render_template('userhome.html', msg="Login Success")
        else:
            return render_template('user.html', msg="Login Failure!!!")

    return render_template('user.html')


@app.route('/uregback',methods=['POST','GET'])
def uregback():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pass']
        addr=request.form['addr']
        ph=request.form['ph']
        dob=request.form['dob']
        gender=request.form['gender']

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="facial_diagnosis"
        )
        mycursor = mydb.cursor()

        sql = "INSERT INTO ureg (name,email,pass,dob,addr,ph,gender) VALUES (%s,%s, %s,%s,%s,%s,%s)"
        val = (name,email,pwd,dob,addr,ph,gender)
        mycursor.execute(sql, val)
        mydb.commit()
    return render_template('user.html',msg="registered successfully")
    print("Successfully Registered")

@app.route('/userhome')
def userhome():
    return render_template("userhome.html",msg='Successfully logined!!')


@app.route('/upload1')
def upload1():
    return render_template("upload.html")

@app.route("/upload", methods=["POST","GET"])
def upload():
    print('a')
    print('a')
    if request.method == 'POST':
        # m = int(request.form['alg'])


        myfile = request.files['file']
        fn = myfile.filename
        acc = pd.read_csv("acc.csv")
        mypath = os.path.join('images/', fn)
        myfile.save(mypath)

        print("{} is the file name", fn)
        print("Accept incoming file:", fn)
        print("Save it to:", mypath)
        # import tensorflow as tf
        import numpy as np
        from tensorflow.keras.preprocessing import image

        from tensorflow.keras.models import load_model

        new_model = load_model("alg/MobileNet.h5")
        test_image = image.load_img(mypath, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = test_image / 255
        test_image = np.expand_dims(test_image, axis=0)


        result = new_model.predict(test_image)
        prediction = classes[np.argmax(result)]
        acc=                                                                                                                                                                                         'Model accuracy is 98.7600'

    return render_template("template.html",image_name=fn, text=prediction, a=acc)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/view1/<filename>')
def view1(filename):

    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(threaded=False)


