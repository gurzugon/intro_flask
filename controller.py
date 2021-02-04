
#python as a programming language
#flask - web framework
#thonny - IDE
#MVC - model, view, controller

# --- Flask with dynamic variable ---#

# import the Flask class from the flask library

import sqlite3 as sql

from model import *
#from user_authentication import *
from flask import Flask,render_template,request,redirect,jsonify

# create the application object
app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('loginnew.html')
    else:
        return render_template('home.html')
 
@app.route('/login', methods=['POST'])
def dologin():
    if checklogin(request.form['nomatrik'],request.form['password']):
        session['logged_in'] = True
        return render_template('home.html')
    else:
        flash('wrong password!')
        return render_template('loginnew.html',message='Invalid NoMatrik or Password!')
       
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()      
       
       # return redirect('/')

@app.route('/list_students')
def list_students():
    rows=list_student()
    return render_template('list_student.html', rows=rows)

@app.route('/new')
def new():
    # Make and blank array of five elements
    row=['']*5
    status='0'
    return render_template('form.html',row=row,status=status)
                  
@app.route('/update',methods=['GET','POST'])
def  insert_update():
    matrixno = request.form['matrixno']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    dob=request.form['dob']
    
    if request.method=='POST' and request.form['status']=='0':                                                     
        row=['']*5
        row[0] = matrixno
        row[1] = name
        row[2] = email
        row[3] = password
        row[4] = dob
        if matrixno == '' or name == '' or password == '':
            msg = '';
            if matrixno == '':
                msg += 'NoMatrik' if len(msg)==0 else ',NoMatrik'
            if name == '':
                msg += 'Name' if len(msg)==0 else ',Name'
            if password == '':
                msg += 'Password' if len(msg)==0 else ',Password'
            msg = msg + ' cannot be empty!';
            return render_template('form.html',message=msg,status='0',row=row)
        else:
            if check_nomatrik(matrixno):
                row[0] = ''
                flash('Nomatrik already exist!')                
                return render_template('form.html',message='NoMatrik '+matrixno+' already exist!',status='0',row=row)

            else:        
                insert_student(matrixno,name,email,password,dob)        
                return redirect('/list_students')
        
        insert_student(matrixno,name,email,password,dob)
        return redirect('/list_students')
      
    if request.method=='POST' and request.form['status']=='0':                            
        insert_student(matrixno,name,email,password,dob)
        return redirect('/list_students')
          
    if request.method=="POST" and request.form['status']=='1':
        update_student(name,email,password,dob,matrixno)
        return redirect('/list_students')
    
@app.route('/new_grade')
def newg():
    # Make and blank array of six elements
    row=['']*6
    status='0'
    students=list_student()
    subjects=list_subject()
    return render_template('frm_stu_grade.html',row=row,status=status,students=students,subjects=subjects)

@app.route('/inupdategred',methods=['GET','POST'])
def  insert_updateg():
    id = None
    if 'id' in request.files:
        id = request.form['id']
    matrixno = request.form['matrixno']
    subject_code = request.form['subject_code']
    marks=request.form['marks']
    grade=request.form['grade']
    grade_point=request.form['grade_point']
    
    if request.method=='POST' and request.form['status']=='0':                            
                
        insert_grade(matrixno,subject_code,marks,grade,grade_point)        
        return redirect('/list_stu_grade')  
    
    #if request.method=="POST" and request.form['status']=='1':
        
        #update_grade(id,nomatrik,kod_subjek,markah,gred,mata_nilai)
        #return redirect('/list_grade')
    
@app.route('/edit/<matrixno>')
def edit(matrixno): 
    row=find_student(matrixno)
    status='1'
    return render_template('form.html',row=row,status=status)

@app.route('/find_student',methods=['GET','POST'])
def find():
    if request.method=="POST":
        matrixno=request.form['matrixno']
        row=find_student(matrixno)
        return render_template('form2.html',row=row)
    else:   
        return render_template('form1.html')

@app.route('/delete/<matrixno>')
def delete(matrixno): 
    delete_student(matrixno)
    return redirect('/list_students')

@app.route('/list_stu_grades')
def list_sg():
    rows=list_stu_grades()
    return render_template('list_student_grade.html', rows=rows)

@app.route('/list_subjects')
def subject():
    rows=list_subject()
    return render_template('list_subject.html', rows=rows)

@app.route('/list_grades')
def grade():
    rows=list_grade()
    return render_template('list_grade.html', rows=rows)

# start the server using the run() method
if __name__ == "__main__":
     app.secret_key = "!mzo53678912489"
     app.run(debug=True,host='0.0.0.0', port=3000)
