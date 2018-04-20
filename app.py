from flask import Flask, render_template, request, redirect
from dbmanager import Dbmanager
from models import *
from config import Config
from htmlforms import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/')
@app.route('/index')
def index():
    Dbmanager(Config.dbname).init_tables()
    return render_template('index.html')


@app.route('/students')
def students():
    students = Dbmanager(Config.dbname).get_students()
    return render_template('students.html', title='Students', students=students)


@app.route('/subjects')
def subjects():
    subjects = Dbmanager(Config.dbname).get_subjects()
    return render_template('subject.html', title='Subjects', subjects=subjects)


@app.route('/marks', methods=['GET', 'POST'])
def marks():
    form = GetMarksForm()
    form.specialities.choices = [(item.get_values()['specialityId'], item.get_values()['speciality']) for item in Dbmanager(Config.dbname).get_specialities()]
    if form.validate_on_submit():
        result = Dbmanager(Config.dbname).form_marks_table(form.specialities.data, form.course.data)
        return render_template('marks.html', title='Marks', table=result)
    return render_template('premarks.html', title='Marks', form=form)


@app.route('/facspec')
def facspec():
    facs = Dbmanager(Config.dbname).get_faculties()
    faculties = [{"faculty": faculty, "specialities": Dbmanager(Config.dbname).get_specialities_by_faculty(faculty.get_values()['facultyId'])} for faculty in facs]
    return render_template('facspec.html', title='Faculties and specialities', faculties=faculties)


@app.route('/addstudent', methods=['GET', 'POST'])
def addstudent():
    form = AddStudentForm()
    if form.validate_on_submit():
        student = Student.form_values_for_db(form.data)
        try:
            Dbmanager(Config.dbname).add_student(student)
        except:
            return redirect('/error')
        else:
            return redirect('/index')
    return render_template('addstudent.html', title='Add student', form=form)


@app.route('/addsubject', methods=['GET', 'POST'])
def addsubject():
    form = AddSubjectForm()
    if form.validate_on_submit():
        subject = Subject.form_values_for_db(form.data)
        try:
            Dbmanager(Config.dbname).add_subject(subject)
        except:
            return redirect('/error')
        else:
            return redirect('/index')
    return render_template('addsubject.html', title='Add subject', form=form)


@app.route('/addfaculty', methods=['GET', 'POST'])
def addfaculty():
    form = AddFacultyForm()
    if form.validate_on_submit():
        faculty = Faculty.form_values_for_db(form.data)
        try:
            Dbmanager(Config.dbname).add_faculty(faculty)
        except:
            return redirect('/error')
        else:
            return redirect('/index')
    return render_template('addfaculty.html', title='Add faculty', form=form)


@app.route('/addspeciality', methods=['GET', 'POST'])
def addspeciality():
    form = AddSpecialityForm()
    if form.validate_on_submit():
        speciality = Speciality.form_values_for_db(form.data)
        try:
            Dbmanager(Config.dbname).add_speciality(speciality)
        except:
            return redirect('/error')
        else:
            return redirect('/index')
    return render_template('addspeciality.html', title='Add speciality', form=form)


@app.route('/addmark', methods=['GET', 'POST'])
def addmark():
    form = AddMarkForm()
    if form.validate_on_submit():
        mark = Mark.form_values_for_db(form.data)
        try:
            Dbmanager(Config.dbname).add_mark(mark)
        except:
            return redirect('/error')
        else:
            return redirect('/index')
    return render_template('addmark.html', title='Add mark', form=form)


@app.route('/error')
def error():
    return render_template('error.html', title='Error')

"""
@app.route('/init')
def init():
    Dbmanager(Config.dbname).init_tables()
    return redirect('/index')
"""


if __name__ == '__main__':
    app.run()
