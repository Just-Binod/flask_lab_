from flask import Flask,render_template,request,url_for,redirect

from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

# mysql connection  ( using py mysql sriver)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/flask_crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

# Model

# class Student(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(100),nullable=False)
#     age=db.Column(db.Integer,nullable=False)
#     grade=db.Column(db.String(200),nullable=False)

class Category (db.Model):
    id=db.Column(db.Integer,primary_key=True)
    code=db.Column(db.String(20),nullable=False)
    name=db.Column(db.Integer,nullable=False)
    grade=db.Column(db.String(200),nullable=False)

@app.route('/')
def index_page():
    data=students=Student.query.all()
    return render_template('index.html',students=data)

@app.route('/create',methods=['GET','POST'])
def create():
    if request.method=='POST':
        name= request.form['name']
        age= request.form['age']
        grade= request.form['grade']

        new_student=Student(name=name,age=age,grade=grade)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index_page'))
    return render_template('create.html')

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    student=Student.query.get_or_404(id)
    if request.method=="POST":
        student.name= request.form['name']
        student.age= request.form['age']
        student.grade= request.form['grade']
        db.session.commit()
        return redirect(url_for('index_page'))
    return render_template('update.html',student=student)
        
@app.route('/delete/<int:id>')
def delete(id):
    student=Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index_page'))

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)




