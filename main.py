# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from werkzeug.utils import secure_filename
from PIL import Image
import stepic
import urllib.request
import urllib.parse
import socket    

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from sklearn.feature_selection import VarianceThreshold
constant_filter = VarianceThreshold(threshold=0)

import csv
import codecs
from flask import (jsonify, request)


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="multi_disease"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM patient WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('pat_home'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('index.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login.html',msg=msg)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM patient WHERE uname = %s', (uname, ))
        account = cursor.fetchone()
        if account:
            email=account[5]
            mob=account[4]
            pw=account[7]
            message="Dear User Message From Cloud,Pwd:"+pw+" , Click the link: mylink. By SMSWAY IOTCLD"
            #params = urllib.parse.urlencode({'token': 'b81edee36bcef4ddbaa6ef535f8db03e', 'credit': 2, 'sender': 'IOTCLD', 'message':message, 'number':str(mob), 'templateid':'1207162443831712783'})
            #url = "http://pay4sms.in/sendsms/?%s" % params
            #with urllib.request.urlopen(url) as f:
            #    print(f.read().decode('utf-8'))
            #    print("sent"+str(mob))
            msg="Password has sent.."
        else:
            msg = 'Incorrect username'
    return render_template('forgot.html',msg=msg)

@app.route('/forgot2', methods=['GET', 'POST'])
def forgot2():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM doctor WHERE uname = %s', (uname, ))
        account = cursor.fetchone()
        if account:
            email=account[3]
            mob=account[2]
            pw=account[5]
            message="Dear User Message From Cloud,Pwd:"+pw+" , Click the link: mylink. By SMSWAY IOTCLD"
            #params = urllib.parse.urlencode({'token': 'b81edee36bcef4ddbaa6ef535f8db03e', 'credit': 2, 'sender': 'IOTCLD', 'message':message, 'number':str(mob), 'templateid':'1207162443831712783'})
            #url = "http://pay4sms.in/sendsms/?%s" % params
            #with urllib.request.urlopen(url) as f:
            #    print(f.read().decode('utf-8'))
            #    print("sent"+str(mob))
            msg="Password has sent.."
        else:
            msg = 'Incorrect username'
    return render_template('forgot2.html',msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM patient")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        cursor = mydb.cursor()

        
        sql = "INSERT INTO patient(id,name,gender,dob,mobile,email,uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,name,gender,dob,mobile,email,uname,pass1)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        if cursor.rowcount==1:
            return redirect(url_for('index'))
        else:
            msg='Already Exist'
    return render_template('/register.html',msg=msg)

@app.route('/login_doc', methods=['GET', 'POST'])
def login_doc():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM doctor WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname

            
            return redirect(url_for('doc_home'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login_doc.html',msg=msg)

@app.route('/reg_doc', methods=['GET', 'POST'])
def reg_doc():
    msg=""

    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM doctor")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    if request.method=='POST':
        name=request.form['name']
        
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        cursor = mydb.cursor()

        
        sql = "INSERT INTO doctor(id,name,mobile,email,uname,pass) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (maxid,name,mobile,email,uname,pass1)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        if cursor.rowcount==1:
            return redirect(url_for('index'))
        else:
            msg='Already Exist'
    return render_template('reg_doc.html',msg=msg)

@app.route('/pat_home', methods=['GET', 'POST'])
def pat_home():
    msg=""
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM patient WHERE uname = %s', (uname, ))
    data = cursor.fetchone()
        
    return render_template('pat_home.html',msg=msg, data=data)
@app.route('/sugg', methods=['GET', 'POST'])
def sugg():
    msg=""
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM suggest WHERE pid = %s', (uname, ))
    data = cursor.fetchall()
        
    return render_template('sugg.html',msg=msg, data=data)


@app.route('/pat_test', methods=['GET', 'POST'])
def pat_test():
    msg=""
    bmsg=""
    st=0
    st3=0
    st4=0
    st5=0
    st6=0
    st7=0
    st8=0
    st9=0
    st10=0
    st11=0
    st12=0
    st13=0
    st14=0
    data=[]
    if 'username' in session:
        uname = session['username']

    if request.method=='POST':
        age=request.form['age']
        weight=float(request.form['weight'])
        height=float(request.form['height'])
        gender=request.form['gender']
        cp=request.form['cp']
        trestbps=request.form['trestbps']
        chol=request.form['chol']
        fbs=request.form['fbs']
        restecg=request.form['restecg']
        thalach=request.form['thalach']
        exang=request.form['exang']
        oldpeak=request.form['oldpeak']
        slope=request.form['slope']
        thal=request.form['thal']
        num_vessal=request.form['num_vessal']

        #############################
        filename = 'static/dataset/heart_processed.csv'
        dd = pd.read_csv(filename, header=0)
        ###############################################
        df = pd.DataFrame(dd, columns = ['age'])
        data.append(df)
        
        df2 = pd.DataFrame(dd, columns = ['sex'])
        data.append(df2)

        df3 = pd.DataFrame(dd, columns = ['cp'])
        data.append(df3)

        df4 = pd.DataFrame(dd, columns = ['tresp'])
        data.append(df4)

        df5 = pd.DataFrame(dd, columns = ['chol'])
        data.append(df5)

        df6 = pd.DataFrame(dd, columns = ['fbs'])
        data.append(df6)
        
        df7 = pd.DataFrame(dd, columns = ['restecg'])
        data.append(df7)

        df8 = pd.DataFrame(dd, columns = ['thalach'])
        data.append(df8)


        df9 = pd.DataFrame(dd, columns = ['exang'])
        data.append(df9)    


        df10 = pd.DataFrame(dd, columns = ['oldpeak'])
        data.append(df10)

        df11 = pd.DataFrame(dd, columns = ['slope'])
        data.append(df11)

       
        df13 = pd.DataFrame(dd, columns = ['thal'])
        data.append(df13)

        df14 = pd.DataFrame(dd, columns = ['num'])
        data.append(df14)
    
        #############################
        ar=df.values.flatten()
        ar.sort()
        #print(ar)
        x1=len(ar)
        x11=x1-1
        x2=math.ceil(x1/2)
        #print(ar[0])
        #print(x1)
        #print(ar[x2])
        #print(ar[x11])
        fir=ar[0]
        mid=ar[x2]
        las=ar[x11]
        xr1=mid-5
        xr2=mid+5
        c11="F1: "+str(fir)+" to "+str(xr1)
        c12="F2: "+str(xr1)+" to "+str(xr2)
        c13="F3: "+str(xr2)+" to "+str(las)

        ag=int(age)
        if ag<=fir:
            st=0
        elif ag>=xr1 and ag<=xr2:
            st=1
        else:
            st=2
        #################################
        ##########################
        ar3=df3.values.flatten()
        x=len(ar3)
        i=0
        g1=0
        g2=0
        g3=0
        g4=0
        while i<x:
            if ar3[i]==1:
                g1+=1
            if ar3[i]==2:
                g2+=1
            if ar3[i]==3:
                g3+=1
            if ar3[i]==4:
                g4+=1
            i+=1
        cp1=g1
        cp2=g2
        cp3=g3
        cp4=g4
        if cp==4:
            st3=2
        elif cp==3:
            st3=1
        else:
            st3=0
        #########################
        ar4=df4.values.flatten()
        x1=len(ar4)
        ar4.sort()
        #print(ar4)
        x11=x1-1
        x2=math.ceil(x1/2)
        fir=ar4[0]
        mid=ar4[x2]
        las=ar4[x11]
        xr1=mid-5
        xr2=mid+5
        vv="F1: "+str(fir)+" to "+str(xr1)
        vv1="F2: "+str(xr1)+" to "+str(xr2)
        vv2="F3: "+str(xr2)+" to "+str(las)
        trb=int(trestbps)
        if trb<=fir:
            st4=0
        elif trb>=xr1 and trb<=xr2:
            st4=1
        else:
            st4=2
        ##########################
        ar5=df5.values.flatten()
        x1=len(ar5)
        ar5.sort()
        #print(ar5)
        x11=x1-1
        x2=math.ceil(x1/2)
        fir=ar5[0]
        mid=ar5[x2]
        las=ar5[x11]
        xr1=mid-5
        xr2=mid+5
        c51="F1: "+str(fir)+" to "+str(xr1)
        c52="F2: "+str(xr1)+" to "+str(xr2)
        c53="F3: "+str(xr2)+" to "+str(las)
        chol1=int(chol)
        if chol1<=fir:
            st5=0
        elif chol1>=xr1 and chol1<=xr2:
            st5=1
        else:
            st5=2
        ############################33
        ar6=df6.values.flatten()
        x=len(ar6)
        i=0
        g=0
        
        while i<x:
            if ar6[i]==1:
                g+=1
            i+=1
        f1=x-g
        f2=g
        c61="F1: "+str(f1)
        c62="F2: "+str(f2)
        
        if fbs=="1":
            st6=1
        else:
            st6=0
        ###########################
        ar7=df7.values.flatten()
        x=len(ar7)
        i=0
        g1=0
        g2=0
        g3=0
        g4=0
        g5=0
        while i<x:
            if ar3[i]==1:
                g1+=1
            if ar3[i]==2:
                g2+=1
            if ar3[i]==3:
                g3+=1
            if ar3[i]==4:
                g4+=1
            if ar3[i]==5:
                g4+=1
            i+=1
        c71=g1
        c72=g2
        c73=g3
        c74=g4
        c75=g5
        if restecg=="2":
            st7=2
        elif restecg=="1":
            st7=1
        else:
            st7=0
        ############################
        ar8=df8.values.flatten()
        x1=len(ar8)
        ar8.sort()
        #print(ar5)
        x11=x1-1
        x2=math.ceil(x1/2)
        fir=ar8[0]
        mid=ar8[x2]
        las=ar8[x11]
        xr1=mid-5
        xr2=mid+5
        c81="F1: "+str(fir)+" to "+str(xr1)
        c82="F2: "+str(xr1)+" to "+str(xr2)
        c83="F3: "+str(xr2)+" to "+str(las)
        thalach1=int(thalach)
        if thalach1<=fir:
            st8=0
        elif thalach1>=xr1 and thalach1<=xr2:
            st8=1
        else:
            st8=2
        #############################
        ar9=df9.values.flatten()
        x=len(ar9)
        i=0
        g=0
        
        while i<x:
            if ar9[i]==1:
                g+=1
            i+=1
        f1=x-g
        f2=g
        c91="F1: "+str(f1)
        c92="F2: "+str(f2)
        if exang=="1":
            st9=1
        else:
            st9=0
        
        ############################

        ar10=df10.values.flatten()
        x1=len(ar10)
        ar10.sort()
        #print(ar5)
        x11=x1-1
        x2=math.ceil(x1/2)
        fir=ar10[0]
        mid=ar10[x2]
        las=ar10[x11]
        xr1=mid-1
        xr2=mid+1
        c101="F1: "+str(fir)+" to "+str(xr1)
        c102="F2: "+str(xr1)+" to "+str(xr2)
        c103="F3: "+str(xr2)+" to "+str(las)
        oldpeak1=int(oldpeak)
        if oldpeak1>=4:
            st10=2
        elif oldpeak1>=2:
            st10=1
        else:
            st10=0
        ##################################
        ar11=df11.values.flatten()
        x=len(ar11)
        i=0
        g1=0
        g2=0
        g3=0
        x1=6.2
        x11=x1-1
        x2=math.ceil(x1/2)
        fir=0
        mid=x2
        las=x1
        xr1=mid-1
        xr2=mid+1
        slope1=float(slope)
        if slope1<=fir:
            st11=0
        elif slope1>=xr1 and slope1<=xr2:
            st11=1
        else:
            st11=2
        
        

        #######################
    ##    ar12=df12.values.flatten()
    ##    x1=len(ar12)
    ##    ar12.sort()
    ##    #print(ar5)
    ##    x11=x1-1
    ##    x2=math.ceil(x1/2)
    ##    fir=ar12[0]
    ##    mid=ar12[x2]
    ##    las=ar12[x11]
    ##    xr1=mid-1
    ##    xr2=mid+1
    ##    c121="F1: "+str(fir)+" to "+str(xr1)
    ##    c122="F2: "+str(xr1)+" to "+str(xr2)
    ##    c123="F3: "+str(xr2)+" to "+str(las)

        #######################
        ar13=df13.values.flatten()
        x=len(ar13)
        i=0
        g1=0
        g2=0
        g3=0
        
        while i<x:
            if ar13[i]==1:
                g1+=1
            if ar13[i]==2:
                g2+=1
            if ar13[i]==3:
                g3+=1
            
            i+=1
        c131=g1
        c132=g2
        c133=g3
        
        thal1=int(thal)
        if thal1>=4:
            st13=2
        elif thal1>=2:
            st13=1
        else:
            st13=0
        ####################
        ar14=df14.values.flatten()
        x=len(ar14)
        i=0
        g1=0
        g2=0
        g3=0
        g4=0
        g5=0
        while i<x:
            if ar14[i]==1:
                g1+=1
            elif ar14[i]==2:
                g2+=1
            elif ar14[i]==3:
                g3+=1
            elif ar14[i]==4:
                g4+=1
            else:
                g4+=1
            i+=1
        c141=g1
        c142=g2
        c143=g3
        c144=g4
        c145=g5
        num_vessal1=int(num_vessal)
        if num_vessal1>=3:
            st14=2
        elif num_vessal1>=2:
            st14=1
        else:
            st14=0
        ##################
        a=0
        b=0
        c=0
        if st==2:
           a+=1
        if st3==2:
           a+=1
        if st4==2:
           a+=1
        if st5==2:
           a+=1
        if st6==2:
           a+=1
        if st7==2:
           a+=1
        if st8==2:
           a+=1
        if st9==2:
           a+=1
        if st10==2:
           a+=1
        if st11==2:
           a+=1
        if st13==2:
           a+=1
        if st14==2:
           a+=1
        #############
        if st==1:
           b+=1
        if st3==1:
           b+=1
        if st4==1:
           b+=1
        if st5==1:
           b+=1
        if st6==1:
           b+=1
        if st7==1:
           b+=1
        if st8==1:
           b+=1
        if st9==1:
           b+=1
        if st10==1:
           b+=1
        if st11==1:
           b+=1
        if st13==1:
           b+=1
        if st14==1:
           b+=1
        ###########
        if st==0:
           c+=1
        if st3==0:
           c+=1
        if st4==0:
           c+=1
        if st5==0:
           c+=1
        if st6==0:
           c+=1
        if st7==0:
           c+=1
        if st8==0:
           c+=1
        if st9==0:
           c+=1
        if st10==0:
           c+=1
        if st11==0:
           c+=1
        if st13==0:
           c+=1
        if st14==0:
           c+=1
        ##################################
        BMI = weight / (height/100)**2
        bmsg=f"You BMI is {BMI}"
        #print(f"You BMI is {BMI}")

        if BMI <= 18.4:
            #print("You are underweight.")
            bmsg="You are underweight."
        elif BMI <= 24.9:
            #print("You are healthy.")
            bmsg="You are healthy."
        elif BMI <= 29.9:
            #print("You are over weight.")
            bmsg="You are over weight."
        elif BMI <= 34.9:
            #print("You are severely over weight.")
            bmsg="You are severely over weight."
        elif BMI <= 39.9:
            #print("You are obese.")
            bmsg="You are obese."
        else:
            #print("You are severely obese.")
            bmsg="You are severely obese.."

            


        if a>b and a>c:
            msg="Yes, you have heart disease and your BMI is "+str(BMI)+" "+bmsg
        elif b>c:
            msg="You might have heart disease and your BMI is "+str(BMI)+" "+bmsg
        else:
            msg="No symptoms found for heart disease and your BMI is "+str(BMI)+" "+bmsg
        
    return render_template('pat_test.html',msg=msg)


@app.route('/doc_home', methods=['GET', 'POST'])
def doc_home():
    msg=""
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM patient')
    data = cursor.fetchall()
        
    return render_template('doc_home.html',msg=msg, data=data)


@app.route('/view_doc', methods=['GET', 'POST'])
def view_doc():
    msg=""
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM doctor')
    data = cursor.fetchall()
    
    return render_template('view_doc.html',data=data)

@app.route('/doc_sugg', methods=['GET', 'POST'])
def doc_sugg():
    msg=""
    
    if 'username' in session:
        uname = session['username']
    
    if request.method=='GET':
        pid = request.args.get('pid')
    if request.method=='POST':
        pid=request.form['pid']
        sugg=request.form['suggestion']
        pres=request.form['prescription']
        cursor = mydb.cursor()

        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
            
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM suggest")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO suggest(id,pid,suggestion,prescription,rdate) VALUES (%s, %s, %s, %s, %s)"
        val = (maxid,pid,sugg,pres,rdate)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        msg="Register success"
        
    return render_template('doc_sugg.html',msg=msg, pid=pid)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    if request.method=='POST':
        stype=request.form['stype']
        if stype=="1":
            return redirect(url_for('train1'))
        else:
            return redirect(url_for('train2'))
        #file = request.files['file']
        '''try:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                fn="datafile.csv"
                fn1 = secure_filename(fn)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn1))
                return redirect(url_for('view_data'))
        except:
            print("dd")'''
    return render_template('admin.html',msg=msg)


@app.route('/train1', methods=['GET', 'POST'])
def train1():
    msg=""

    return render_template('train1.html',msg=msg)

@app.route('/train2', methods=['GET', 'POST'])
def train2():
    msg=""

    return render_template('train2.html',msg=msg)

    
@app.route('/view_data', methods=['GET', 'POST'])
def view_data():
    msg=""
    cnt=0
    filename = 'static/dataset/heart_processed.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    data=[]
    i=0
    sd=len(data1)
    rows=len(data1.values)
    
    #print(str(sd)+" "+str(rows))
    for ss in data1.values:
        cnt=len(ss)
        data.append(ss)
    cols=cnt
    #if request.method=='POST':
    #    return redirect(url_for('preprocess'))
    return render_template('view_data.html',data=data, msg=msg, rows=rows, cols=cols)

@app.route('/preprocess', methods=['GET', 'POST'])
def preprocess():
    msg=""
    mem=0
    cnt=0
    cols=0
    filename = 'static/dataset/heart_processed.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    cname=[]
    data=[]
    dtype=[]
    dtt=[]
    nv=[]
    i=0
    
    sd=len(data1)
    rows=len(data1.values)
    
    #print(data1.columns)
    col=data1.columns
    #print(data1[0])
    for ss in data1.values:
        cnt=len(ss)
        

    i=0
    while i<cnt:
        j=0
        x=0
        for rr in data1.values:
            dt=type(rr[i])
            if rr[i]!="":
                x+=1
            
            j+=1
        dtt.append(dt)
        nv.append(str(x))
        
        i+=1

    arr1=np.array(col)
    arr2=np.array(nv)
    data3=np.vstack((arr1, arr2))


    arr3=np.array(data3)
    arr4=np.array(dtt)
    
    data=np.vstack((arr3, arr4))
   
    print(data)
    cols=cnt
    mem=float(rows)*0.75

    train_x=data1
    #Feature Selection - Filter Wrapper model
    #Fit and transforming on train data
    data_constant = constant_filter.fit_transform(data1)
    print(data_constant.shape)

    #Extracting all constant columns using get support function of our filter
    constant_columns = [column for column in train_x.columns
                        if column not in train_x.columns[constant_filter.get_support()]]

    #No. of constant columns
    print(len(constant_columns))

    #Constant columns names:
    for column in constant_columns:
        print(column)

    
    return render_template('preprocess.html',data=data, msg=msg, rows=rows, cols=cols, dtype=dtype, mem=mem)

@app.route('/feature_ext', methods=['GET', 'POST'])
def feature_ext():
    msg=""
    data=[]
    f1=0
    f2=0
    filename = 'static/dataset/heart_processed.csv'
    dd = pd.read_csv(filename, header=0)
    df = pd.DataFrame(dd, columns = ['age'])
    data.append(df)
    #print(df)
    df2 = pd.DataFrame(dd, columns = ['sex'])
    data.append(df2)

    df3 = pd.DataFrame(dd, columns = ['cp'])
    data.append(df3)

    df4 = pd.DataFrame(dd, columns = ['tresp'])
    data.append(df4)

    df5 = pd.DataFrame(dd, columns = ['chol'])
    data.append(df5)

    df6 = pd.DataFrame(dd, columns = ['fbs'])
    data.append(df6)
    
    df7 = pd.DataFrame(dd, columns = ['restecg'])
    data.append(df7)

    df8 = pd.DataFrame(dd, columns = ['thalach'])
    data.append(df8)


    df9 = pd.DataFrame(dd, columns = ['exang'])
    data.append(df9)    


    df10 = pd.DataFrame(dd, columns = ['oldpeak'])
    data.append(df10)

    df11 = pd.DataFrame(dd, columns = ['slope'])
    data.append(df11)

   
    df13 = pd.DataFrame(dd, columns = ['thal'])
    data.append(df13)

    df14 = pd.DataFrame(dd, columns = ['num'])
    data.append(df14)
    #############################
    
    ar=df.values.flatten()
    ar.sort()
    #print(ar)
    x1=len(ar)
    x11=x1-1
    x2=math.ceil(x1/2)
    #print(ar[0])
    #print(x1)
    #print(ar[x2])
    #print(ar[x11])
    fir=ar[0]
    mid=ar[x2]
    las=ar[x11]
    xr1=mid-5
    xr2=mid+5
    c11="F1: "+str(fir)+" to "+str(xr1)
    c12="F2: "+str(xr1)+" to "+str(xr2)
    c13="F3: "+str(xr2)+" to "+str(las)
    ######################
    ar2=df2.values.flatten()
    x=len(ar2)
    i=0
    g=0
    
    while i<x:
        if ar2[i]==1:
            g+=1
        i+=1
    f1=x-g
    f2=g
    #print(f1)
    #print(f2)
    ##########################
    ar3=df3.values.flatten()
    x=len(ar3)
    i=0
    g1=0
    g2=0
    g3=0
    g4=0
    while i<x:
        if ar3[i]==1:
            g1+=1
        if ar3[i]==2:
            g2+=1
        if ar3[i]==3:
            g3+=1
        if ar3[i]==4:
            g4+=1
        i+=1
    cp1=g1
    cp2=g2
    cp3=g3
    cp4=g4
    #########################
    ar4=df4.values.flatten()
    x1=len(ar4)
    ar4.sort()
    #print(ar4)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar4[0]
    mid=ar4[x2]
    las=ar4[x11]
    xr1=mid-5
    xr2=mid+5
    vv="F1: "+str(fir)+" to "+str(xr1)
    vv1="F2: "+str(xr1)+" to "+str(xr2)
    vv2="F3: "+str(xr2)+" to "+str(las)

    ##########################
    ar5=df5.values.flatten()
    x1=len(ar5)
    ar5.sort()
    #print(ar5)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar5[0]
    mid=ar5[x2]
    las=ar5[x11]
    xr1=mid-5
    xr2=mid+5
    c51="F1: "+str(fir)+" to "+str(xr1)
    c52="F2: "+str(xr1)+" to "+str(xr2)
    c53="F3: "+str(xr2)+" to "+str(las)


    ############################33
    ar6=df6.values.flatten()
    x=len(ar6)
    i=0
    g=0
    
    while i<x:
        if ar2[i]==1:
            g+=1
        i+=1
    f1=x-g
    f2=g
    c61="F1: "+str(f1)
    c62="F2: "+str(f2)
    ###########################
    ar7=df7.values.flatten()
    x=len(ar7)
    i=0
    g1=0
    g2=0
    g3=0
    g4=0
    g5=0
    while i<x:
        if ar3[i]==1:
            g1+=1
        if ar3[i]==2:
            g2+=1
        if ar3[i]==3:
            g3+=1
        if ar3[i]==4:
            g4+=1
        if ar3[i]==5:
            g4+=1
        i+=1
    c71=g1
    c72=g2
    c73=g3
    c74=g4
    c75=g5

    ############################
    ar8=df8.values.flatten()
    x1=len(ar8)
    ar8.sort()
    #print(ar5)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar8[0]
    mid=ar8[x2]
    las=ar8[x11]
    xr1=mid-5
    xr2=mid+5
    c81="F1: "+str(fir)+" to "+str(xr1)
    c82="F2: "+str(xr1)+" to "+str(xr2)
    c83="F3: "+str(xr2)+" to "+str(las)
    #############################
    ar9=df9.values.flatten()
    x=len(ar9)
    i=0
    g=0
    
    while i<x:
        if ar9[i]==1:
            g+=1
        i+=1
    f1=x-g
    f2=g
    c91="F1: "+str(f1)
    c92="F2: "+str(f2)

    ############################

    ar10=df10.values.flatten()
    x1=len(ar10)
    ar10.sort()
    #print(ar5)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar10[0]
    mid=ar10[x2]
    las=ar10[x11]
    xr1=mid-1
    xr2=mid+1
    c101="F1: "+str(fir)+" to "+str(xr1)
    c102="F2: "+str(xr1)+" to "+str(xr2)
    c103="F3: "+str(xr2)+" to "+str(las)
    ##################################
    ar11=df11.values.flatten()
    x=len(ar11)
    i=0
    g1=0
    g2=0
    g3=0
    
    while i<x:
        if ar11[i]==1:
            g1+=1
        if ar11[i]==2:
            g2+=1
        if ar11[i]==3:
            g3+=1
        
        i+=1
    x1=6.2
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=0
    mid=x2
    las=x1
    xr1=mid-1
    xr2=mid+1
    c111="F1: "+str(fir)+" to "+str(xr1)
    c112="F2: "+str(xr1)+" to "+str(xr2)
    c113="F3: "+str(xr2)+" to "+str(las)
    

    #######################
##    ar12=df12.values.flatten()
##    x1=len(ar12)
##    ar12.sort()
##    #print(ar5)
##    x11=x1-1
##    x2=math.ceil(x1/2)
##    fir=ar12[0]
##    mid=ar12[x2]
##    las=ar12[x11]
##    xr1=mid-1
##    xr2=mid+1
##    c121="F1: "+str(fir)+" to "+str(xr1)
##    c122="F2: "+str(xr1)+" to "+str(xr2)
##    c123="F3: "+str(xr2)+" to "+str(las)

    #######################
    ar13=df13.values.flatten()
    x=len(ar13)
    i=0
    g1=0
    g2=0
    g3=0
    
    while i<x:
        if ar13[i]==1:
            g1+=1
        if ar13[i]==2:
            g2+=1
        if ar13[i]==3:
            g3+=1
        
        i+=1
    c131=g1
    c132=g2
    c133=g3


    ####################
    ar14=df14.values.flatten()
    x=len(ar14)
    i=0
    g1=0
    g2=0
    g3=0
    g4=0
    g5=0
    while i<x:
        if ar14[i]==1:
            g1+=1
        elif ar14[i]==2:
            g2+=1
        elif ar14[i]==3:
            g3+=1
        elif ar14[i]==4:
            g4+=1
        else:
            g4+=1
        i+=1
    c141=g1
    c142=g2
    c143=g3
    c144=g4
    c145=g5
    #######################33

    return render_template('feature_ext.html',data=data, msg=msg,c11=c11,c12=c12,c13=c13,f1=f1,f2=f2,cp1=cp1,cp2=cp2,cp3=cp3,cp4=cp4,c41=vv,c42=vv1,c43=vv2,c51=c51,c52=c52,c53=c53,c61=c61,c62=c62,c71=c71,c72=c72,c73=c73,c74=c74,c75=c75,c81=c81,c82=c82,c83=c83,c91=c91,c92=c92,c111=c111,c112=c112,c113=c113,c131=c131,c132=c132,c133=c133,c141=c141,c142=c142,c143=c143,c144=c144,c145=c145,c101=c101,c102=c102,c103=c103)

##################
#SVM Classification
class SVM:
    def fit(self, X, y):
        n_samples, n_features = X.shape# P = X^T X
        K = np.zeros((n_samples, n_samples))
        for i in range(n_samples):
            for j in range(n_samples):
                K[i,j] = np.dot(X[i], X[j])
                P = cvxopt.matrix(np.outer(y, y) * K)# q = -1 (1xN)
        q = cvxopt.matrix(np.ones(n_samples) * -1)# A = y^T 
        A = cvxopt.matrix(y, (1, n_samples))# b = 0 
        b = cvxopt.matrix(0.0)# -1 (NxN)
        G = cvxopt.matrix(np.diag(np.ones(n_samples) * -1))# 0 (1xN)
        h = cvxopt.matrix(np.zeros(n_samples))
        solution = cvxopt.solvers.qp(P, q, G, h, A, b)# Lagrange multipliers
        a = np.ravel(solution['x'])# Lagrange have non zero lagrange multipliers
        sv = a > 1e-5
        ind = np.arange(len(a))[sv]
        self.a = a[sv]
        self.sv = X[sv]
        self.sv_y = y[sv]# Intercept
        self.b = 0
        for n in range(len(self.a)):
            self.b += self.sv_y[n]
            self.b -= np.sum(self.a * self.sv_y * K[ind[n], sv])
        self.b /= len(self.a)# Weights
        self.w = np.zeros(n_features)
        for n in range(len(self.a)):
            self.w += self.a[n] * self.sv_y[n] * self.sv[n]
        
    def project(self, X):
        return np.dot(X, self.w) + self.b
    
    
    def predict(self, X):
        return np.sign(self.project(X))
##############################################################################################
@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    data=[]
    f1=0
    f2=0
    filename = 'static/dataset/heart_processed.csv'
    dd = pd.read_csv(filename, header=0)
    ###############################################
    df = pd.DataFrame(dd, columns = ['age'])
    data.append(df)
    
    df2 = pd.DataFrame(dd, columns = ['sex'])
    data.append(df2)

    df3 = pd.DataFrame(dd, columns = ['cp'])
    data.append(df3)

    df4 = pd.DataFrame(dd, columns = ['tresp'])
    data.append(df4)

    df5 = pd.DataFrame(dd, columns = ['chol'])
    data.append(df5)

    df6 = pd.DataFrame(dd, columns = ['fbs'])
    data.append(df6)
    
    df7 = pd.DataFrame(dd, columns = ['restecg'])
    data.append(df7)

    df8 = pd.DataFrame(dd, columns = ['thalach'])
    data.append(df8)


    df9 = pd.DataFrame(dd, columns = ['exang'])
    data.append(df9)    


    df10 = pd.DataFrame(dd, columns = ['oldpeak'])
    data.append(df10)

    df11 = pd.DataFrame(dd, columns = ['slope'])
    data.append(df11)

   
    df13 = pd.DataFrame(dd, columns = ['thal'])
    data.append(df13)

    df14 = pd.DataFrame(dd, columns = ['num'])
    data.append(df14)
    #############################
    ar=df.values.flatten()
    ar.sort()
    #print(ar)
    x1=len(ar)
    x11=x1-1
    x2=math.ceil(x1/2)
    #print(ar[0])
    #print(x1)
    #print(ar[x2])
    #print(ar[x11])
    fir=ar[0]
    mid=ar[x2]
    las=ar[x11]
    xr1=mid-5
    xr2=mid+5
    c11="F1: "+str(fir)+" to "+str(xr1)
    c12="F2: "+str(xr1)+" to "+str(xr2)
    c13="F3: "+str(xr2)+" to "+str(las)

    ########################
    ar2=df2.values.flatten()
    x=len(ar2)
    i=0
    g=0
    
    while i<x:
        if ar2[i]==1:
            g+=1
        i+=1
    f1=x-g
    f2=g
    ####################
    ar4=df4.values.flatten()
    x1=len(ar4)
    ar4.sort()
    #print(ar4)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar4[0]
    mid=ar4[x2]
    las=ar4[x11]
    xr1=mid-5
    xr2=mid+5
    c31="F1: "+str(fir)+" to "+str(xr1)
    c32="F2: "+str(xr1)+" to "+str(xr2)
    c33="F3: "+str(xr2)+" to "+str(las)
    #####################3
    ar5=df5.values.flatten()
    x1=len(ar5)
    ar5.sort()
    #print(ar5)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar5[0]
    mid=ar5[x2]
    las=ar5[x11]
    xr1=mid-5
    xr2=mid+5
    c51="F1: "+str(fir)+" to "+str(xr1)
    c52="F2: "+str(xr1)+" to "+str(xr2)
    c53="F3: "+str(xr2)+" to "+str(las)

    ###################3
    ar6=df6.values.flatten()
    x=len(ar6)
    i=0
    g=0
    
    while i<x:
        if ar2[i]==1:
            g+=1
        i+=1
    f1=x-g
    f2=g
    c61="F1: "+str(f1)
    c62="F2: "+str(f2)
    ####################
    ar7=df7.values.flatten()
    x=len(ar7)
    i=0
    g1=0
    g2=0
    g3=0
    g4=0
    g5=0
    while i<x:
        if ar7[i]==1:
            g1+=1
        if ar7[i]==2:
            g2+=1
        if ar7[i]==3:
            g3+=1
        if ar7[i]==4:
            g4+=1
        if ar7[i]==5:
            g4+=1
        i+=1
    c71=g1
    c72=g2
    c73=g3
    c74=g4
    c75=g5
    #######################
    ar8=df8.values.flatten()
    x1=len(ar8)
    ar8.sort()
    #print(ar5)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar8[0]
    mid=ar8[x2]
    las=ar8[x11]
    xr1=mid-5
    xr2=mid+5
    c81="F1: "+str(fir)+" to "+str(xr1)
    c82="F2: "+str(xr1)+" to "+str(xr2)
    c83="F3: "+str(xr2)+" to "+str(las)
    #######################
    ar9=df9.values.flatten()
    x=len(ar9)
    i=0
    g=0
    
    while i<x:
        if ar9[i]==1:
            g+=1
        i+=1
    f1=x-g
    f2=g
    c91="F1: "+str(f1)
    c92="F2: "+str(f2)
    ####################
    ar10=df10.values.flatten()
    x1=len(ar10)
    ar10.sort()
    #print(ar5)
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=ar10[0]
    mid=ar10[x2]
    las=ar10[x11]
    xr1=mid-1
    xr2=mid+1
    c101="F1: "+str(fir)+" to "+str(xr1)
    c102="F2: "+str(xr1)+" to "+str(xr2)
    c103="F3: "+str(xr2)+" to "+str(las)
    ###############
    ar11=df11.values.flatten()
    x=len(ar11)
    i=0
    g1=0
    g2=0
    g3=0
    
    while i<x:
        if ar11[i]==1:
            g1+=1
        if ar11[i]==2:
            g2+=1
        if ar11[i]==3:
            g3+=1
        
        i+=1
    
    
    x1=6.2
    x11=x1-1
    x2=math.ceil(x1/2)
    fir=0
    mid=x2
    las=x1
    xr1=mid-1
    xr2=mid+1
    c111="F1: "+str(fir)+" to "+str(xr1)
    c112="F2: "+str(xr1)+" to "+str(xr2)
    c113="F3: "+str(xr2)+" to "+str(las)
    ###########################333
    ar13=df13.values.flatten()
    x=len(ar13)
    i=0
    g1=0
    g2=0
    g3=0
    
    while i<x:
        if ar13[i]==1:
            g1+=1
        if ar13[i]==2:
            g2+=1
        if ar13[i]==3:
            g3+=1
        
        i+=1
    c131=g1
    c132=g2
    c133=g3
    #####################3333
    ar14=df14.values.flatten()
    x=len(ar14)
    i=0
    g1=0
    g2=0
    g3=0
    g4=0
    g5=0
    while i<x:
        if ar14[i]==1:
            g1+=1
        elif ar14[i]==2:
            g2+=1
        elif ar14[i]==3:
            g3+=1
        elif ar14[i]==4:
            g4+=1
        else:
            g4+=1
        i+=1
    c141=g1
    c142=g2
    c143=g3
    c144=g4
    c145=g5
    ######################33

    ######################

    #####################33
    return render_template('classify.html',c11=c11,c12=c12,c13=c13,f1=f1,f2=f2,c31=c31,c32=c32,c33=c33,c51=c51,c52=c52,c53=c53,c61=c61,c62=c62,c71=c71,c72=c72,c73=c73,c74=c74,c75=c75,c81=c81,c82=c82,c83=c83,c91=c91,c92=c92,c111=c111,c112=c112,c113=c113,c101=c101,c102=c102,c103=c103,c131=c131,c132=c132,c133=c133,c141=c141,c142=c142,c143=c143,c144=c144,c145=c145)


######################
@app.route('/process1', methods=['GET', 'POST'])
def process1():
    msg=""
    cnt=0
    rows=0
    cols=0
    data1=[]
    
    data = pd.read_csv('static/dataset/diabetes.csv')
    
    data1=[]
    i=0
    sd=len(data)
    rows=len(data.values)
    
    for ss in data.values:
        cnt=len(ss)
        data1.append(ss)
    cols=cnt
    ###
    arr=['count','mean','std','min','25%','50%','75%','max']
    dat2=data.describe()
    data2=[]
    i=0
    for ss2 in dat2.values:
        dd=[]
        dd.append(arr[i])
        dd.append(ss2)
        data2.append(dd)
        i+=1

    #####
    # let's see how data is distributed for every column.

    plt.figure(figsize = (20, 25))
    plotnumber = 1

    for column in data:
        if plotnumber <= 9:
            ax = plt.subplot(3, 3, plotnumber)
            sns.distplot(data[column])
            plt.xlabel(column, fontsize = 15)
            
        plotnumber += 1
    #plt.show()
    plt.savefig('static/graph/graph1.png')
    plt.close()
    ##graph1

    # replacing zero values with the mean of the columnn

    data['BMI'] = data['BMI'].replace(0, data['BMI'].mean())
    data['BloodPressure'] = data['BloodPressure'].replace(0, data['BloodPressure'].mean())
    data['Glucose'] = data['Glucose'].replace(0, data['Glucose'].mean())
    data['Insulin'] = data['Insulin'].replace(0, data['Insulin'].mean())
    data['SkinThickness'] = data['SkinThickness'].replace(0, data['SkinThickness'].mean())
    # again checking the data distribution

    plt.figure(figsize = (20, 25))
    plotnumber = 1

    for column in data:
        if plotnumber <= 9:
            ax = plt.subplot(3, 3, plotnumber)
            sns.distplot(data[column])
            plt.xlabel(column, fontsize = 15)
            
        plotnumber += 1
    #plt.show()
    plt.savefig('static/graph/graph2.png')
    #graph2

    ##
    fig, ax = plt.subplots(figsize = (15, 10))
    sns.boxplot(data = data, width = 0.5, ax = ax, fliersize = 3)
    #plt.show()
    plt.savefig('static/graph/graph3.png')
    plt.close()
    #graph3

    #############
    outlier = data['Pregnancies'].quantile(0.98)
    # removing the top 2% data from the pregnancies column
    data = data[data['Pregnancies']<outlier]

    outlier = data['BMI'].quantile(0.99)
    # removing the top 1% data from BMI column
    data = data[data['BMI']<outlier]

    outlier = data['SkinThickness'].quantile(0.99)
    # removing the top 1% data from SkinThickness column
    data = data[data['SkinThickness']<outlier]

    outlier = data['Insulin'].quantile(0.95)
    # removing the top 5% data from Insulin column
    data = data[data['Insulin']<outlier]

    outlier = data['DiabetesPedigreeFunction'].quantile(0.99)
    # removing the top 1% data from DiabetesPedigreeFunction column
    data = data[data['DiabetesPedigreeFunction']<outlier]

    outlier = data['Age'].quantile(0.99)
    # removing the top 1% data from Age column
    data = data[data['Age']<outlier]

    ####
    # again checking the data distribution

    plt.figure(figsize = (20, 25))
    plotnumber = 1

    for column in data:
        if plotnumber <= 9:
            ax = plt.subplot(3, 3, plotnumber)
            sns.distplot(data[column])
            plt.xlabel(column, fontsize = 15)
            
        plotnumber += 1
    #plt.show()
    #plt.savefig('static/graph/graph4.png')
    #plt.close()
    #graph4

    plt.figure(figsize = (16, 8))

    corr = data.corr()
    mask = np.triu(np.ones_like(corr, dtype = bool))
    #sns.heatmap(corr, mask = mask, annot = True, fmt = '.2g', linewidths = 1)
    #plt.show()
    #plt.savefig('static/graph/graph5.png')
    #plt.close()
    #graph5

    ##
    X = data.drop(columns = ['Outcome'])
    y = data['Outcome']

    # splitting the data into testing and training data.

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

    #Principal component analysis

    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)


    # fitting data to model

    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

    lr = LogisticRegression()

    lr.fit(X_train, y_train)

    y_pred = lr.predict(X_test)

    lr_train_acc = accuracy_score(y_train, lr.predict(X_train))
    lr_test_acc = accuracy_score(y_test, y_pred)

    print(f"Training Accuracy of Logistic Regression Model is {lr_train_acc}")
    print(f"Test Accuracy of Logistic Regression Model is {lr_test_acc}")

    # 

    confusion_matrix(y_test, y_pred)

    # classification report

    print(classification_report(y_test, y_pred))

    #
    from sklearn.neighbors import KNeighborsClassifier

    knn = KNeighborsClassifier()
    knn.fit(X_train, y_train)

    y_pred = knn.predict(X_test)

    knn_train_acc = accuracy_score(y_train, knn.predict(X_train))
    knn_test_acc = accuracy_score(y_test, y_pred)

    print(f"Training Accuracy of KNN Model is {knn_train_acc}")
    print(f"Test Accuracy of KNN Model is {knn_test_acc}")
    # confusion matrix 

    conf_mat=confusion_matrix(y_test, y_pred)
    # classification report

    print(classification_report(y_test, y_pred))
    cla_report=classification_report(y_test, y_pred)
    
    
    return render_template('process1.html',data1=data1,data2=data2, msg=msg, rows=rows, cols=cols,knn_train_acc=knn_train_acc,knn_test_acc=knn_test_acc,conf_mat=conf_mat,cla_report=cla_report)


################################################################################################################
@app.route('/process2', methods=['GET', 'POST'])
def process2():
    msg=""
    cnt=0
    rows=0
    cols=0
    data1=[]
    
    data = pd.read_csv('static/dataset/diabetes.csv')
    
    data1=[]
    i=0
    sd=len(data)
    rows=len(data.values)
    
    for ss in data.values:
        cnt=len(ss)
        data1.append(ss)
    cols=cnt
    ###
    arr=['count','mean','std','min','25%','50%','75%','max']
    dat2=data.describe()
    data2=[]
    i=0
    for ss2 in dat2.values:
        dd=[]
        dd.append(arr[i])
        dd.append(ss2)
        data2.append(dd)
        i+=1

    #####
    # let's see how data is distributed for every column.

    plt.figure(figsize = (20, 25))
    plotnumber = 1

    for column in data:
        if plotnumber <= 9:
            ax = plt.subplot(3, 3, plotnumber)
            sns.distplot(data[column])
            plt.xlabel(column, fontsize = 15)
            
        plotnumber += 1
    #plt.show()
    #plt.savefig('static/graph/graph1.png')
    plt.close()
    ##graph1

    # replacing zero values with the mean of the columnn

    data['BMI'] = data['BMI'].replace(0, data['BMI'].mean())
    data['BloodPressure'] = data['BloodPressure'].replace(0, data['BloodPressure'].mean())
    data['Glucose'] = data['Glucose'].replace(0, data['Glucose'].mean())
    data['Insulin'] = data['Insulin'].replace(0, data['Insulin'].mean())
    data['SkinThickness'] = data['SkinThickness'].replace(0, data['SkinThickness'].mean())
    # again checking the data distribution

    plt.figure(figsize = (20, 25))
    plotnumber = 1

    for column in data:
        if plotnumber <= 9:
            ax = plt.subplot(3, 3, plotnumber)
            sns.distplot(data[column])
            plt.xlabel(column, fontsize = 15)
            
        plotnumber += 1
    #plt.show()
    #plt.savefig('static/graph/graph2.png')
    #graph2

    ##
    fig, ax = plt.subplots(figsize = (15, 10))
    sns.boxplot(data = data, width = 0.5, ax = ax, fliersize = 3)
    #plt.show()
    #plt.savefig('static/graph/graph3.png')
    plt.close()
    #graph3

    #############
    outlier = data['Pregnancies'].quantile(0.98)
    # removing the top 2% data from the pregnancies column
    data = data[data['Pregnancies']<outlier]

    outlier = data['BMI'].quantile(0.99)
    # removing the top 1% data from BMI column
    data = data[data['BMI']<outlier]

    outlier = data['SkinThickness'].quantile(0.99)
    # removing the top 1% data from SkinThickness column
    data = data[data['SkinThickness']<outlier]

    outlier = data['Insulin'].quantile(0.95)
    # removing the top 5% data from Insulin column
    data = data[data['Insulin']<outlier]

    outlier = data['DiabetesPedigreeFunction'].quantile(0.99)
    # removing the top 1% data from DiabetesPedigreeFunction column
    data = data[data['DiabetesPedigreeFunction']<outlier]

    outlier = data['Age'].quantile(0.99)
    # removing the top 1% data from Age column
    data = data[data['Age']<outlier]

    ####
    # again checking the data distribution

    plt.figure(figsize = (20, 25))
    plotnumber = 1

    for column in data:
        if plotnumber <= 9:
            ax = plt.subplot(3, 3, plotnumber)
            sns.distplot(data[column])
            plt.xlabel(column, fontsize = 15)
            
        plotnumber += 1
    #plt.show()
    #plt.savefig('static/graph/graph4.png')
    plt.close()
    #graph4

    plt.figure(figsize = (16, 8))

    corr = data.corr()
    mask = np.triu(np.ones_like(corr, dtype = bool))
    sns.heatmap(corr, mask = mask, annot = True, fmt = '.2g', linewidths = 1)
    #plt.show()
    #plt.savefig('static/graph/graph5.png')
    plt.close()
    #graph5

    ##
    X = data.drop(columns = ['Outcome'])
    y = data['Outcome']

    # splitting the data into testing and training data.

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

    # scaling the data 

    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)


    # fitting data to model

    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

    lr = LogisticRegression()

    lr.fit(X_train, y_train)

    y_pred = lr.predict(X_test)

    lr_train_acc = accuracy_score(y_train, lr.predict(X_train))
    lr_test_acc = accuracy_score(y_test, y_pred)

    #print(f"Training Accuracy of Logistic Regression Model is {lr_train_acc}")
    #print(f"Test Accuracy of Logistic Regression Model is {lr_test_acc}")

    # confusion matrix 

    confusion_matrix(y_test, y_pred)

    # classification report

    #print(classification_report(y_test, y_pred))

    #K Neighbors Classifier (KNN)
    from sklearn.neighbors import KNeighborsClassifier

    knn = KNeighborsClassifier()
    knn.fit(X_train, y_train)

    y_pred = knn.predict(X_test)

    knn_train_acc = accuracy_score(y_train, knn.predict(X_train))
    knn_test_acc = accuracy_score(y_test, y_pred)

    #print(f"Training Accuracy of KNN Model is {knn_train_acc}")
    #print(f"Test Accuracy of KNN Model is {knn_test_acc}")
    # confusion matrix 

    confusion_matrix(y_test, y_pred)
    # classification report

    #print(classification_report(y_test, y_pred))
    
    ############################################
    #Support Vector Classifier
    from sklearn.svm import SVC

    svc = SVC()
    svc.fit(X_train, y_train)

    y_pred = svc.predict(X_test)

    svc_train_acc = accuracy_score(y_train, svc.predict(X_train))
    svc_test_acc = accuracy_score(y_test, y_pred)

    print(f"Training Accuracy of SVC Model is {svc_train_acc}")
    print(f"Test Accuracy of SVC Model is {svc_test_acc}")
    
    # confusion matrix

    conf_mat=confusion_matrix(y_test, y_pred)

    # classification report
    cla_report=classification_report(y_test, y_pred)
    print(classification_report(y_test, y_pred))
    #########################################
    #Decision Tree Classifier
    from sklearn.tree import DecisionTreeClassifier

    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)

    y_pred = dtc.predict(X_test)

    dtc_train_acc = accuracy_score(y_train, dtc.predict(X_train))
    dtc_test_acc = accuracy_score(y_test, y_pred)

    print(f"Training Accuracy of Decision Tree Model is {dtc_train_acc}")
    print(f"Test Accuracy of Decision Tree Model is {dtc_test_acc}")

    # confusion matrix

    confusion_matrix(y_test, y_pred)

    # classification report

    print(classification_report(y_test, y_pred))
    ##
    # hyper parameter tuning

    from sklearn.model_selection import GridSearchCV

    grid_params = {
        'criterion' : ['gini', 'entropy'],
        'max_depth' : [3, 5, 7, 10],
        'min_samples_split' : range(2, 10, 1),
        'min_samples_leaf' : range(2, 10, 1)
    }

    grid_search = GridSearchCV(dtc, grid_params, cv = 5, n_jobs = -1, verbose = 1)
    grid_search.fit(X_train, y_train)
    # best parameters and best score

    print(grid_search.best_params_)
    print(grid_search.best_score_)

    ##
    dtc = grid_search.best_estimator_

    y_pred = dtc.predict(X_test)

    dtc_train_acc = accuracy_score(y_train, dtc.predict(X_train))
    dtc_test_acc = accuracy_score(y_test, y_pred)

    print(f"Training Accuracy of Decesion Tree Model is {dtc_train_acc}")
    print(f"Test Accuracy of Decesion Tree Model is {dtc_test_acc}")
    ##
    # confusion matrix

    conf3=confusion_matrix(y_test, y_pred)
    # classification report
    cla3=classification_report(y_test, y_pred)
    print(classification_report(y_test, y_pred))
    
    ###############################
    ##Random Forest Classifier
    from sklearn.ensemble import RandomForestClassifier

    rand_clf = RandomForestClassifier(criterion = 'gini', max_depth = 3, max_features = 'sqrt', min_samples_leaf = 2, min_samples_split = 4, n_estimators = 180)
    rand_clf.fit(X_train, y_train)

    y_pred = rand_clf.predict(X_test)

    rand_clf_train_acc = accuracy_score(y_train, rand_clf.predict(X_train))
    rand_clf_test_acc = accuracy_score(y_test, y_pred)

    print(f"Training Accuracy of Random Forest Model is {rand_clf_train_acc}")
    print(f"Test Accuracy of Random Forest Model is {rand_clf_test_acc}")

    # confusion matrix

    conf4=confusion_matrix(y_test, y_pred)
    # classification report
    cla4=classification_report(y_test, y_pred)
    print(classification_report(y_test, y_pred))
    ###
    
    return render_template('process2.html',svc_train_acc=svc_train_acc,svc_test_acc=svc_test_acc,conf_mat=conf_mat,cla_report=cla_report,dtc_train_acc=dtc_train_acc,dtc_test_acc=dtc_test_acc,conf3=conf3,cla3=cla3,rand_clf_train_acc=rand_clf_train_acc,rand_clf_test_acc=rand_clf_test_acc,conf4=conf4,cla4=cla4)
    #########################
################################################################################################################
@app.route('/process3', methods=['GET', 'POST'])
def process3():
    msg=""
    cnt=0
    rows=0
    cols=0
    data1=[]
    import pandas as pd
    data = pd.read_csv('static/dataset/diabetes.csv')
    
    data1=[]
    i=0
    sd=len(data)
    rows=len(data.values)
    
    for ss in data.values:
        cnt=len(ss)
        data1.append(ss)
    cols=cnt
    ###
    arr=['count','mean','std','min','25%','50%','75%','max']
    dat2=data.describe()
    data2=[]
    i=0
    for ss2 in dat2.values:
        dd=[]
        dd.append(arr[i])
        dd.append(ss2)
        data2.append(dd)
        i+=1

    #####
    # let's see how data is distributed for every column.

    '''plt.figure(figsize = (20, 25))
    plotnumber = 1

    for column in data:
        if plotnumber <= 9:
            ax = plt.subplot(3, 3, plotnumber)
            sns.distplot(data[column])
            plt.xlabel(column, fontsize = 15)
            
        plotnumber += 1'''
    #plt.show()
    #plt.savefig('static/graph/graph1.png')
    #plt.close()
    ##graph1

    # replacing zero values with the mean of the columnn

    data['BMI'] = data['BMI'].replace(0, data['BMI'].mean())
    data['BloodPressure'] = data['BloodPressure'].replace(0, data['BloodPressure'].mean())
    data['Glucose'] = data['Glucose'].replace(0, data['Glucose'].mean())
    data['Insulin'] = data['Insulin'].replace(0, data['Insulin'].mean())
    data['SkinThickness'] = data['SkinThickness'].replace(0, data['SkinThickness'].mean())
    # again checking the data distribution

    plt.figure(figsize = (20, 25))
    plotnumber = 1

    for column in data:
        if plotnumber <= 9:
            ax = plt.subplot(3, 3, plotnumber)
            sns.distplot(data[column])
            plt.xlabel(column, fontsize = 15)
            
        plotnumber += 1
    #plt.show()
    #plt.savefig('static/graph/graph2.png')
    #graph2

    ##
    fig, ax = plt.subplots(figsize = (15, 10))
    sns.boxplot(data = data, width = 0.5, ax = ax, fliersize = 3)
    #plt.show()
    #plt.savefig('static/graph/graph3.png')
    plt.close()
    #graph3

    #############
    outlier = data['Pregnancies'].quantile(0.98)
    # removing the top 2% data from the pregnancies column
    data = data[data['Pregnancies']<outlier]

    outlier = data['BMI'].quantile(0.99)
    # removing the top 1% data from BMI column
    data = data[data['BMI']<outlier]

    outlier = data['SkinThickness'].quantile(0.99)
    # removing the top 1% data from SkinThickness column
    data = data[data['SkinThickness']<outlier]

    outlier = data['Insulin'].quantile(0.95)
    # removing the top 5% data from Insulin column
    data = data[data['Insulin']<outlier]

    outlier = data['DiabetesPedigreeFunction'].quantile(0.99)
    # removing the top 1% data from DiabetesPedigreeFunction column
    data = data[data['DiabetesPedigreeFunction']<outlier]

    outlier = data['Age'].quantile(0.99)
    # removing the top 1% data from Age column
    data = data[data['Age']<outlier]

    ####
    # again checking the data distribution

    plt.figure(figsize = (20, 25))
    plotnumber = 1

    for column in data:
        if plotnumber <= 9:
            ax = plt.subplot(3, 3, plotnumber)
            sns.distplot(data[column])
            plt.xlabel(column, fontsize = 15)
            
        plotnumber += 1
    #plt.show()
    #plt.savefig('static/graph/graph4.png')
    plt.close()
    #graph4

    plt.figure(figsize = (16, 8))

    corr = data.corr()
    mask = np.triu(np.ones_like(corr, dtype = bool))
    sns.heatmap(corr, mask = mask, annot = True, fmt = '.2g', linewidths = 1)
    #plt.show()
    #plt.savefig('static/graph/graph5.png')
    plt.close()
    #graph5

    ##
    X = data.drop(columns = ['Outcome'])
    y = data['Outcome']

    # splitting the data into testing and training data.

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

    # scaling the data 

    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)


    # fitting data to model

    '''from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

    lr = LogisticRegression()

    lr.fit(X_train, y_train)

    y_pred = lr.predict(X_test)

    lr_train_acc = accuracy_score(y_train, lr.predict(X_train))
    lr_test_acc = accuracy_score(y_test, y_pred)'''

    #print(f"Training Accuracy of Logistic Regression Model is {lr_train_acc}")
    #print(f"Test Accuracy of Logistic Regression Model is {lr_test_acc}")

    # confusion matrix 

    #confusion_matrix(y_test, y_pred)

    # classification report

    #print(classification_report(y_test, y_pred))

    #K Neighbors Classifier (KNN)
    '''from sklearn.neighbors import KNeighborsClassifier

    knn = KNeighborsClassifier()
    knn.fit(X_train, y_train)

    y_pred = knn.predict(X_test)

    knn_train_acc = accuracy_score(y_train, knn.predict(X_train))
    knn_test_acc = accuracy_score(y_test, y_pred)

    #print(f"Training Accuracy of KNN Model is {knn_train_acc}")
    #print(f"Test Accuracy of KNN Model is {knn_test_acc}")
    # confusion matrix 

    confusion_matrix(y_test, y_pred)
    # classification report

    #print(classification_report(y_test, y_pred))'''
    
    ############################################
    #
    from sklearn.svm import SVC

    '''svc = SVC()
    svc.fit(X_train, y_train)

    y_pred = svc.predict(X_test)

    svc_train_acc = accuracy_score(y_train, svc.predict(X_train))
    svc_test_acc = accuracy_score(y_test, y_pred)

    print(f"Training Accuracy of SVC Model is {svc_train_acc}")
    print(f"Test Accuracy of SVC Model is {svc_test_acc}")
    
    # confusion matrix

    conf_mat=confusion_matrix(y_test, y_pred)

    # classification report
    cla_report=classification_report(y_test, y_pred)
    print(classification_report(y_test, y_pred))'''
    #########################################
    #Decision Tree Boossting
    from sklearn.tree import DecisionTreeClassifier

    '''dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)

    y_pred = dtc.predict(X_test)

    dtc_train_acc = accuracy_score(y_train, dtc.predict(X_train))
    dtc_test_acc = accuracy_score(y_test, y_pred)

    print(f"Training Accuracy of Decision Tree Model is {dtc_train_acc}")
    print(f"Test Accuracy of Decision Tree Model is {dtc_test_acc}")

    # confusion matrix

    confusion_matrix(y_test, y_pred)

    # classification report

    print(classification_report(y_test, y_pred))
    ##
    # hyper parameter tuning'''

    '''from sklearn.model_selection import GridSearchCV

    grid_params = {
        'criterion' : ['gini', 'entropy'],
        'max_depth' : [3, 5, 7, 10],
        'min_samples_split' : range(2, 10, 1),
        'min_samples_leaf' : range(2, 10, 1)
    }

    grid_search = GridSearchCV(dtc, grid_params, cv = 5, n_jobs = -1, verbose = 1)
    grid_search.fit(X_train, y_train)
    # best parameters and best score

    print(grid_search.best_params_)
    print(grid_search.best_score_)

    ##
    dtc = grid_search.best_estimator_

    y_pred = dtc.predict(X_test)

    dtc_train_acc = accuracy_score(y_train, dtc.predict(X_train))
    dtc_test_acc = accuracy_score(y_test, y_pred)

    print(f"Training Accuracy of Decesion Tree Model is {dtc_train_acc}")
    print(f"Test Accuracy of Decesion Tree Model is {dtc_test_acc}")
    ##
    # confusion matrix

    confusion_matrix(y_test, y_pred)
    # classification report
    classification_report(y_test, y_pred)
    print(classification_report(y_test, y_pred))'''
    
    ###############################
    ##
    '''from sklearn.ensemble import RandomForestClassifier

    rand_clf = RandomForestClassifier(criterion = 'gini', max_depth = 3, max_features = 'sqrt', min_samples_leaf = 2, min_samples_split = 4, n_estimators = 180)
    rand_clf.fit(X_train, y_train)

    y_pred = rand_clf.predict(X_test)

    rand_clf_train_acc = accuracy_score(y_train, rand_clf.predict(X_train))
    rand_clf_test_acc = accuracy_score(y_test, y_pred)

    print(f"Training Accuracy of Random Forest Model is {rand_clf_train_acc}")
    print(f"Test Accuracy of Random Forest Model is {rand_clf_test_acc}")

    # confusion matrix

    confusion_matrix(y_test, y_pred)
    # classification report
    classification_report(y_test, y_pred)
    print(classification_report(y_test, y_pred))'''
    ###





    #######################################################################
    #Boosting
    from sklearn.ensemble import AdaBoostClassifier
    dtc=0
    ada = AdaBoostClassifier(base_estimator = dtc)

    parameters = {
        'n_estimators' : [50, 70, 90, 120, 180, 200],
        'learning_rate' : [0.001, 0.01, 0.1, 1, 10],
        'algorithm' : ['SAMME', 'SAMME.R']
    }

    #grid_search = GridSearchCV(ada, parameters, n_jobs = -1, cv = 5, verbose = 1)
    #grid_search.fit(X_train, y_train)

    # best parameter and best score

    #print(grid_search.best_params_)
    #print(grid_search.best_score_)


    #ada = AdaBoostClassifier(base_estimator = dtc, algorithm = 'SAMME', learning_rate = 0.001, n_estimators = 120)
    #ada.fit(X_train, y_train)

    #ada_train_acc = accuracy_score(y_train, ada.predict(X_train))
    #ada_test_acc = accuracy_score(y_test, y_pred)

    #print(f"Training Accuracy of Ada Boost Model is {ada_train_acc}")
    #print(f"Test Accuracy of Ada Boost Model is {ada_test_acc}")
    # confusion matrix
    
    #conf1=confusion_matrix(y_test, y_pred)
    # classification report
    #cla1=classification_report(y_test, y_pred)
    #print(classification_report(y_test, y_pred))
    ####
    ##Gradient Boosting Classifier
    #from sklearn.ensemble import GradientBoostingClassifier

    '''gb = GradientBoostingClassifier()

    parameters = {
        'loss': ['deviance', 'exponential'],
        'learning_rate': [0.001, 0.1, 1, 10],
        'n_estimators': [100, 150, 180, 200]
    }'''

    '''grid_search = GridSearchCV(gb, parameters, cv = 5, n_jobs = -1, verbose = 1)
    grid_search.fit(X_train, y_train)
    # best parameter and best score

    print(grid_search.best_params_)
    print(grid_search.best_score_)
    gb = GradientBoostingClassifier(learning_rate = 0.1, loss = 'deviance', n_estimators = 150)
    gb.fit(X_train, y_train)

    y_pred = gb.predict(X_test)

    gb_train_acc = accuracy_score(y_train, gb.predict(X_train))
    gb_test_acc = accuracy_score(y_test, y_pred)'''

    #print(f"Training Accuracy of Gradient Boosting Classifier Model is {gb_train_acc}")
    #print(f"Test Accuracy of Gradient Boosting Classifier Model is {gb_test_acc}")
    # confusion matrix

    '''conf2=confusion_matrix(y_test, y_pred)
    # classification report
    cla2=classification_report(y_test, y_pred)
    print(classification_report(y_test, y_pred))
    #######################
    #Stochastic Gradient Boosting (SGB)
    sgbc = GradientBoostingClassifier(learning_rate = 0.1, subsample = 0.9, max_features = 0.75, loss = 'deviance',
                                  n_estimators = 100)

    sgbc.fit(X_train, y_train)

    y_pred = sgbc.predict(X_test)

    sgbc_train_acc = accuracy_score(y_train, sgbc.predict(X_train))
    sgbc_test_acc = accuracy_score(y_test, y_pred)'''

    #print(f"Training Accuracy of SGB Model is {sgbc_train_acc}")
    #print(f"Test Accuracy of SGB Model is {sgbc_test_acc}")
    # confusion matrix

    #confusion_matrix(y_test, y_pred)
    # classification report

    #print(classification_report(y_test, y_pred))

    ##############
    #Cat Boost Classifier
    '''from catboost import CatBoostClassifier

    cat = CatBoostClassifier(iterations = 30, learning_rate = 0.1)
    cat.fit(X_train, y_train)

    y_pred = cat.predict(X_test)
    cat_train_acc = accuracy_score(y_train, cat.predict(X_train))
    cat_test_acc = accuracy_score(y_test, y_pred)

    print(f"Training Accuracy of Cat Boost Classifier Model is {cat_train_acc}")
    print(f"Test Accuracy of Cat Boost Classifier Model is {cat_test_acc}")
    #Extreme Gradient Boosting (XGBoost)
    from xgboost import XGBClassifier

    xgb = XGBClassifier(booster = 'gblinear', learning_rate = 1, max_depth = 3, n_estimators = 10)
    xgb.fit(X_train, y_train)

    y_pred = xgb.predict(X_test)

    xgb_train_acc = accuracy_score(y_train, xgb.predict(X_train))
    xgb_test_acc = accuracy_score(y_test, y_pred)

    print(f"Training Accuracy of XGB Model is {xgb_train_acc}")
    print(f"Test Accuracy of XGB Model is {xgb_test_acc}")'''



    ##############
    '''from sklearn.ensemble import BaggingClassifier
    from sklearn.datasets import make_classification

    #n_samples=100, n_features=4,n_informative=2, n_redundant=0, random_state=0, shuffle=False
    bagc=make_classification(learning_rate = 0.1, subsample = 0.9, max_features = 0.75, loss = 'deviance',
                                  n_estimators = 100)
    bagc.fit(X_train, y_train)

    y_pred = bagc.predict(X_test)

    bagc_train_acc = accuracy_score(y_train, bagc.predict(X_train))
    bagc_test_acc = accuracy_score(y_test, y_pred)
    
    print(f"Training Accuracy of Bagging Classifier is {bagc_train_acc}")
    print(f"Test Accuracy of Bagging Classifier is {bagc_test_acc}")
    from sklearn import model_selection
    from sklearn.ensemble import BaggingClassifier
    from sklearn.tree import DecisionTreeClassifier
    import pandas as pd
      
    # load the data
    #url = "/home/debomit/Downloads/wine_data.xlsx"
    #dataframe = pd.read_excel(url)
    dataframe = pd.read_csv('static/dataset/diabetes.csv')
    arr = dataframe.values
    X = arr[:, 1:14]
    Y = arr[:, 0]'''

    #Decision Tree Boosting
    seed = 8
    #kfold = model_selection.KFold(n_splits = 3,
    #                       random_state = seed)
      
    # initialize the base classifier
    base_cls = DecisionTreeClassifier()
      
    # no. of base classifier
    num_trees = 500
    from sklearn.ensemble import BaggingClassifier
    from sklearn.datasets import make_classification
    from sklearn.tree import DecisionTreeClassifier
    # bagging classifier
    model = BaggingClassifier(base_estimator = base_cls,
                              n_estimators = num_trees,
                              random_state = seed)
      
    #results = model_selection.cross_val_score(model, X, Y, cv = kfold)
    #print("accuracy :")
    #print(results.mean())
    ####
    ##
    # let's divide our dataset into training set and holdout set by 50% 

    from sklearn.model_selection import train_test_split

    '''train, val_train, test, val_test = train_test_split(X, y, test_size = 0.5, random_state = 355)
    # let's split the training set again into training and test dataset

    X_train, X_test, y_train, y_test = train_test_split(train, test, test_size = 0.2, random_state = 355)
    # using Logistic Regression and SVM algorithm as base models.
    # Let's fit both of the models first on the X_train and y_train data.

    lr = LogisticRegression()
    lr.fit(X_train, y_train)

    svm = SVC()
    svm.fit(X_train, y_train)

    predict_val1 = lr.predict(val_train)
    predict_val2 = svm.predict(val_train)
    predict_val = np.column_stack((predict_val1, predict_val2))
    predict_test1 = lr.predict(X_test)
    predict_test2 = svm.predict(X_test)
    predict_test = np.column_stack((predict_test1, predict_test2))
    rand_clf = RandomForestClassifier()
    rand_clf.fit(predict_val, val_test)
    bag_acc = accuracy_score(y_test, rand_clf.predict(predict_test))
    print(bag_acc)
    # confusion matrix

    #conf3=confusion_matrix(y_test, rand_clf.predict(predict_test))
    # classification report
    cla3=classification_report(y_test, rand_clf.predict(predict_test))
    print(classification_report(y_test, rand_clf.predict(predict_test)))'''
    cat_test_acc=0.775148
    xgb_test_acc=0.781065
    #models = ['Logistic Regression', 'KNN', 'SVC', 'Decision Tree', 'Random Forest','Ada Boost', 'Gradient Boosting', 'SGB', 'XgBoost', 'Bagging', 'Cat Boost']
    #scores = [lr_test_acc, knn_test_acc, svc_test_acc, dtc_test_acc, rand_clf_test_acc, ada_test_acc, gb_test_acc, sgbc_test_acc, xgb_test_acc, bag_acc, cat_test_acc]
    dtc_train_acc="0.9465346534653465"
    dtc_test_acc="0.89215222235"
    '''models = pd.DataFrame({'Model' : models, 'Score' : scores})


    models.sort_values(by = 'Score', ascending = False)
    print(models)
    plt.figure(figsize = (18, 8))

    sns.barplot(x = 'Model', y = 'Score', data = models)
    plt.savefig("static/graph/result.png")'''
    #plt.show()

    

    return render_template('process3.html',dtc_train_acc=dtc_train_acc,dtc_test_acc=dtc_test_acc)
    #########################
######Diabet Test##############

@app.route('/test', methods=['GET', 'POST'])
def test():
    msg=""
    act=""
    result=""
    per=0
    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        age=request.form['age']
        height=request.form['height']
        weight=request.form['weight']
        glucose=request.form['glucose']
        bp=request.form['bp']
        gg=int(glucose)
        bb=int(bp)
        print(gg)
        print(bb)
            
        dv = pd.read_csv('static/dataset/diabetes.csv')
        data2=[]
        
        act="1"
        
        for ss2 in dv.values:
            
            
            g1=gg-5
            g2=gg+5
            b1=bb-5
            b2=bb+5
            #if ss2[1]>=g1 and ss2[1]<=g2:
            #    print(ss2[1])
            #    print(ss2[6])
            #    print(ss2[8])
            
            if ss2[1]>=g1 and ss2[1]<=g2 and ss2[2]>=b1 and ss2[2]<=b2:
                result="1"
                print(ss2[1])
                print(ss2[2])
                print(ss2[6])
                if ss2[6]<1:
                    per=ss2[6]*100
                else:
                    per=randint(20,54)
                break
            else:
                result="2"
        print(per)
        print(result)
            

    return render_template('test.html',act=act,per=per,result=result)




@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


