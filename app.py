from flask import Flask, flash, redirect,render_template,request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key = 'mahan70900'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:70900@localhost/students'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Branch(db.Model):
    __tablename__ = 'branches'
    branch_id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100), nullable=False, unique=True)
    branch_code = db.Column(db.String(10), nullable=False, unique=True)

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    
    student_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=True, unique=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'))

class Courses(db.Model):
     __tablename__ = 'courses'
     course_id=db.Column(db.Integer, primary_key=True)
     course_name= db.Column(db.String(50), nullable=False)

class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollments_id = db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Integer, db.ForeignKey('students.student_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))
    enrollment_date=db.Column(db.Date, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'))
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/student')
def student():
    students = db.session.query(
        Student.student_id,  
        Student.student_name,
        Student.dob,
        Student.gender,
        Student.email,
        Student.phone,
        Branch.branch_code  
    ).join(Branch, Student.branch_id == Branch.branch_id).all()
    return render_template('students.html',students=students)

@app.route('/addstudent',methods=['GET', 'POST'])
def addstundet():
    branches = Branch.query.all()
    if request.method == 'POST':
        student_name = request.form['name']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        branch_id = request.form['branch_id']
        new_student = Student(student_name=student_name, dob=dob,gender=gender,email=email,phone=phone,branch_id=branch_id)
        db.session.add(new_student)
        db.session.commit()
        flash("student added successfully!")
        return redirect('/student')
    return render_template('add_student.html',branches=branches)
@app.route('/editstudent/<int:student_id>',methods=['GET'])
def editstudent(student_id):
    student = Student.query.get_or_404(student_id)  
    branches = Branch.query.all() 
    return render_template('edit_student.html', student=student, branches=branches)
@app.route('/update-student/<int:student_id>', methods=['POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.student_name = request.form['name']
    student.dob = request.form['dob']
    student.gender = request.form['gender']
    student.email = request.form['email']
    student.phone = request.form['phone']
    student.branch_id = request.form['branch_id']
    db.session.commit()
    flash('Student updated successfully!')
    return redirect('/student')
@app.route('/delete-student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!')
    return redirect('/student')
@app.route('/branch')
def branch():
    branches = Branch.query.all()
    
    return render_template('branches.html',branches=branches)
@app.route('/addbranch',methods=['GET', 'POST'])
def addbranch():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        

        new_branch = Branch(branch_name=name, branch_code=code)
        db.session.add(new_branch)
        db.session.commit()
        flash("Branch added successfully!")
        return redirect('/branch')
    return render_template('add_branch.html')
@app.route('/course')
def course():
    courses=Courses.query.all()
    return render_template('courses.html',courses=courses)
@app.route('/addcourse',methods=['GET', 'POST'])
def addcourse():
    if request.method == 'POST':
        name = request.form['name']
       
        

        new_course = Courses(course_name=name )
        db.session.add(new_course)
        db.session.commit()
        flash("course added successfully!")
        return redirect('/course')
    return render_template('add_course.html')


if __name__=="__main__":
    app.run(debug=True)
