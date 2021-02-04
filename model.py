import sqlite3 as sql

from functools import wraps
from flask import session,flash,redirect,url_for

connect_db ='smp2.db' 

def list_student():
  with sql.connect(connect_db) as db:
    qry = 'select * from students' 
    result=db.execute(qry)
    return(result)

def insert_student(matrixno,name,email,password,dob):
  with sql.connect(connect_db) as db:
    qry='insert into students (matrixno,name,email,password,dob) values (?,?,?,?,?)' 
    db.execute(qry,(matrixno,name,email,password,dob))
    
def check_nomatrik(matrixno):
  with sql.connect(connect_db) as db: 
    qry = 'select matrixno,password from students where matrixno=?'
    result=db.execute(qry,(matrixno,)).fetchone()
    return(result)

def delete_student(matrixno):
  with sql.connect(connect_db) as db:
    qry='delete from students where matrixno=?' 
    db.execute(qry,(matrixno,))
    
def update_student(name,email,password,dob,matrixno):
  with sql.connect(connect_db) as db:
    qry='update students set name=?,email=?,password=?,dob=? where matrixno=?' 
    db.execute(qry, (name,email,password,dob,matrixno))
    
def find_student(matrixno):
  with sql.connect(connect_db) as db:
    qry = 'select * from students where matrixno=?'
    result=db.execute(qry,(matrixno,)).fetchone()
    return(result)

def list_stu_grades():
  with sql.connect(connect_db) as db:
    qry = 'select students.matrixno, students.name, subjects.name, subjects.subject_code, grade.marks, grade.grade, grade.grade_point from students, grade, subjects where students.matrixno=grade.matrixno and subjects.subject_code=grade.subject_code' 
    result=db.execute(qry)
    return(result)

def list_subject():
  with sql.connect(connect_db) as db:
    qry = 'select * from subjects' 
    result=db.execute(qry)
    return(result)

def list_grade():
  with sql.connect(connect_db) as db:
    qry = 'select * from grade' 
    result=db.execute(qry)
    return(result)

def result():
  rows=list_student()
  rows=list_subject()
  rows=list_grade()
  for row in rows:
   print (rows)
  
def insert_grade(matrixno,subject_code,marks,grade,grade_point):
  with sql.connect(connect_db) as db:
    qry='insert into grade (matrixno, subject_code, marks, grade, grade_point) values (?,?,?,?,?)' 
    db.execute(qry,(matrixno,subject_code,marks,grade,grade_point))

def checklogin(nomatrik,password):
  with sql.connect(connect_db) as db: 
    qry = 'select matrixno,password from students where matrixno=? and password=?'
    result=db.execute(qry,(nomatrik,password)).fetchone()
    return(result)

# helper function

def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
        return f(*args, **kwargs)
    else:
        flash("You need to login first")
        return redirect(url_for('home'))
  return wrap