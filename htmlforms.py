from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired


class AddStudentForm(FlaskForm):
    firstName = StringField('First name', validators=[DataRequired()])
    lastName = StringField('Last name', validators=[DataRequired()])
    course = IntegerField('Course', validators=[DataRequired()])
    specialityId = IntegerField('Speciality ID', validators=[DataRequired()])
    submit = SubmitField('Add')


class AddSubjectForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    submit = SubmitField('Add')


class AddFacultyForm(FlaskForm):
    faculty = StringField('Faculty', validators=[DataRequired()])
    submit = SubmitField('Add')


class AddSpecialityForm(FlaskForm):
    speciality = StringField('Speciality', validators=[DataRequired()])
    facultyId = IntegerField('Faculty ID', validators=[DataRequired()])
    submit = SubmitField('Add')


class AddMarkForm(FlaskForm):
    mark = IntegerField('Mark', validators=[DataRequired()])
    studentId = IntegerField('Student ID', validators=[DataRequired()])
    subjectId = IntegerField('Subject ID', validators=[DataRequired()])
    submit = SubmitField('Add')


class GetMarksForm(FlaskForm):
    specialities = SelectField('Specialities', coerce=int)
    course = IntegerField('Course', validators=[DataRequired()])
    submit = SubmitField('Show')
