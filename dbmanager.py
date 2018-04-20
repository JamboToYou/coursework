import sqlite3
from models import Student, Faculty, Mark, Speciality, Subject


tables_init_query = """
                        PRAGMA foreign_keys=ON;
                        
                        CREATE TABLE IF NOT EXISTS Faculties(
                            facultyId INTEGER PRIMARY KEY,
                            faculty TEXT
                        );
                        
                        CREATE TABLE IF NOT EXISTS Specialities(
                            specialityId INTEGER PRIMARY KEY,
                            facultyId INTEGER,
                            speciality TEXT,
                            FOREIGN KEY (facultyId) REFERENCES Faculties (facultyId)
                        );
                        
                        CREATE TABLE IF NOT EXISTS Students(
                            studentId INTEGER PRIMARY KEY,
                            firstName TEXT,
                            lastName TEXT,
                            course INTEGER,
                            specialityId INTEGER,
                            FOREIGN KEY (specialityId) REFERENCES Specialities (specialityId)
                        );
                        
                        CREATE TABLE IF NOT EXISTS Subject(
                            subjectId INTEGER PRIMARY KEY,
                            subject TEXT
                        );
                        
                        CREATE TABLE IF NOT EXISTS MarksTable(
                            markId INTEGER PRIMARY KEY,
                            mark INTEGER,
                            studentId INTEGER,
                            subjectId INTEGER,
                            FOREIGN KEY (studentId) REFERENCES Students (studentId),
                            FOREIGN KEY (subjectId) REFERENCES Subjects (subjectId)
                        );
                    """


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



class Dbmanager():
    def __init__(self, dbname):
        self._dbname = dbname

    def init_tables(self):
        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()
            c.executescript(tables_init_query)
            conn.commit()

    def add_student(self, student):
        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()
            c.execute(
                """
                    INSERT INTO Students(firstName, lastName, course, specialityId)
                    VALUES(?, ?, ?, ?)
                """, student)
            conn.commit()

    def add_subject(self, subject):
        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()
            c.execute(
                """
                    INSERT INTO Subject(subject)
                    VALUES(?)
                """, (subject,))
            conn.commit()

    def add_faculty(self, faculty):
        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()
            c.execute(
                """
                    INSERT INTO Faculties(faculty)
                    VALUES(?)
                """, (faculty,))
            conn.commit()

    def add_speciality(self, speciality):
        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()
            c.execute(
                """
                    INSERT INTO Specialities(facultyId, speciality)
                    VALUES(?, ?)
                """, speciality)
            conn.commit()

    def add_mark(self, markpack):
        with sqlite3.connect(self._dbname) as conn:
            c = conn.cursor()
            c.execute(
                """
                    INSERT INTO MarksTable(mark, studentId, subjectId)
                    VALUES(?, ?, ?)
                """, markpack)
            conn.commit()

    def get_students(self):
        result = None
        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = dict_factory
            c = conn.cursor()
            c.execute(
                """ 
                    SELECT studentId, firstName, lastName, course, faculty, speciality
                    FROM Students LEFT JOIN 
                      (Specialities LEFT JOIN Faculties 
                        ON Specialities.facultyId = Faculties.facultyId) 
                        ON Students.specialityId = Specialities.specialityId
                    ORDER BY studentId;
                """)
            result = [Student(**student) for student in c.fetchall()]
        return result

    def get_students_by_spec(self, specialityId, course):
        result = None
        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = dict_factory
            c = conn.cursor()
            c.execute(
                """ 
                    SELECT studentId, firstName, lastName, course, faculty, speciality
                    FROM Students LEFT JOIN 
                      (Specialities LEFT JOIN Faculties 
                        ON Specialities.facultyId = Faculties.facultyId) 
                        ON Students.specialityId = Specialities.specialityId
                        WHERE Students.specialityId = ? AND course = ?
                    ORDER BY studentId;
                """, (specialityId, course))
            result = [Student(**student) for student in c.fetchall()]
        return result

    def get_faculties(self):
        result = None
        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = dict_factory
            c = conn.cursor()
            c.execute(
                """
                    SELECT facultyId, faculty 
                    FROM Faculties
                    ORDER BY facultyId
                """)
            result = [Faculty(**faculty) for faculty in c.fetchall()]
        return result

    def get_specialities(self):
        result = None
        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = dict_factory
            c = conn.cursor()
            c.execute(
                """
                    SELECT specialityId, facultyId, speciality
                    FROM Specialities
                    ORDER BY specialityId
                """)
            result = [Speciality(**speciality) for speciality in c.fetchall()]
        return result

    def get_subjects(self):
        result = None
        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = dict_factory
            c = conn.cursor()
            c.execute(
                """
                    SELECT subjectId, subject 
                    FROM Subject
                    ORDER BY subjectId
                """)
            result = [Subject(**subject) for subject in c.fetchall()]
        return result

    def get_specialities_by_faculty(self, facultyId):
        result = None
        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = dict_factory
            c = conn.cursor()
            c.execute(
                """
                    SELECT specialityId, facultyId, speciality 
                    FROM Specialities
                    WHERE facultyId = ?
                    ORDER BY specialityId
                """, (facultyId,))
            result = [Speciality(**speciality) for speciality in c.fetchall()]
        return result

    def get_marks_table(self, specialityId, course):
        result = None
        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = dict_factory
            c = conn.cursor()
            c.execute(
                """
                    SELECT studentId, lastName, firstName, subject, mark
                    FROM MarksTable 
                    LEFT JOIN Students ON MarksTable.studentId = Students.studentId
                    LEFT JOIN Subject ON MarksTable.subjectId = Subject.subjectId
                    WHERE specialityId = ? AND course = ?
                    ORDER BY studentId;
                """, (specialityId, course))

            result = [Mark(**mark) for mark in c.fetchall()]

        return result

    def get_students_marks(self, studentId):
        result = None
        with sqlite3.connect(self._dbname) as conn:
            conn.row_factory = dict_factory
            c = conn.cursor()
            c.execute(
                """
                    SELECT mark, subjectId FROM MarksTable WHERE studentId = ?
                """, (studentId,))
            result = {item['subjectId']: item['mark'] for item in c.fetchall()}
        return result

    def form_marks_table(self, specialityId, course, **kwargs):
        students = self.get_students_by_spec(specialityId, course)
        subjects = self.get_subjects()

        table = []

        titles = ['Students ID', 'Students name']

        for subject in subjects:
            titles.append(subject.get_values()['subject'])

        table.append(titles)

        for student in students:
            s = student.get_values()
            student_marks = self.get_students_marks(s['studentId'])
            row = []
            row.append(s['studentId'])
            row.append(s['lastName'] + ' ' + s['firstName'])
            for subject in subjects:
                try:
                    row.append(student_marks[subject.get_values()['subjectId']])
                except:
                    row.append('-')

            table.append(row)

        return table