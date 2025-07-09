from flask import Flask,render_template,request,url_for,redirect

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import relationship

app=Flask(__name__)

# mysql connection  ( using py mysql sriver)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/flask_crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

# Model
class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    grade=db.Column(db.String(200),nullable=False)





class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    code=db.Column(db.String(20),nullable=False)
    name=db.Column(db.String(200),nullable=False)
    description=db.Column(db.String(500),nullable=False)

    product=relationship('Product' , back_populates="category")


class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
    name=db.Column(db.String(100),nullable=False)
    quantity=db.Column(db.Numeric(10,2),nullable=False)
    rate=db.Column(db.Numeric(10,2),nullable=False)
    unit_of_measurement=db.Column(db.String(200),nullable=False)

    category=relationship('Category',back_populates='product')

# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     code = db.Column(db.String(20), nullable=False)
#     name = db.Column(db.String(20), nullable=False)  # Changed from Integer to String
#     grade = db.Column(db.String(200), nullable=False)
    
#     products = db.relationship('Product', back_populates="category")  # Plural for one-to-many, fixed class name


# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
#     name = db.Column(db.String(20), nullable=False)
#     quantity = db.Column(db.Numeric(10, 2), nullable=False)
#     rate = db.Column(db.Numeric(10, 2), nullable=False)
    
#     category = db.relationship('Category', back_populates="products")  # Singular for many-to-one

# class Product(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     category_id=db.Column(db.Integer,db.ForeignKey('category.id'), nullable=False)
#     name=db.Column(db.String(20),nullable=False)
#     quantity=db.Column(db.Numeric(10,2),nullable=False)
#     rate=db.Column(db.Numeric(10,2),nullable=False)

#     product=relationship('Product',back_populates="category")




# class Category (db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     code=db.Column(db.String(20),nullable=False)
#     name=db.Column(db.Integer,nullable=False)
#     grade=db.Column(db.String(200),nullable=False)

#     product=relationship('Category',back_populates="product")



@app.route('/add_Category',methods=['POST','GET'])
def add_category():
    if request.method=='POST':
        code=request.form.get('code')
        name=request.form.get('name')
        description=request.form.get('description')
        category=Category(code=code,name=name,description=description)
        db.session.add(category)
        db.session.commit()


    return render_template('add_category.html')


@app.route('/add_product',methods=['POST','GET'])
def add_product():
    if request.method=='POST':
        category=request.form.get('category_id')
        name=request.form.get('name')
        qyt=request.form.get('qyt')
        rate=request.form.get('rate')
        unit=request.form.get('unit')
        product=Product(category_id=category,name=name,quantity=qyt,rate=rate,unit_of_measurement=unit)
        db.session.add(product)
        db.session.commit()

    category=Category.query.all()    
    return render_template('add_product.html',category=category)
# @app.route('/category')
# def add_category():
#     return render_template('add_category.html')


# @app.route('/product')
# def add_product():
#     return render_template('add_product.html')

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




