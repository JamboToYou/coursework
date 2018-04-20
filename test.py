from dbmanager import Dbmanager


if __name__ == '__main__':
    db = Dbmanager('test.sqlite')
    """db.init_tables()

    faculties = [
        'InPIT', 'InETS'
    ]

    specialities = [
        (1, 'IFST'),
        (2, 'QQQQ'),
        (3, 'WWWW'),
        (4, 'DDDD')
    ]

    students = []

    for i in range(1, 21):
        students.append((str(i), str(i) + 'ov', (i-1)%3 + 1, (i-1)%4 + 1))

    for faculty in faculties:
        db.add_faculty(faculty)

    for speciality in specialities:
        db.add_speciality(speciality)

    for student in students:
        db.add_student(student)

    subjects = [
        'Math', 'Phys', 'English', 'Programming'
    ]

    for subject in subjects:
        db.add_subject(subject)

    for i in range(200):
        mark = (i, (i-1)%20 + 1, (i-1)%4 + 1)
        db.add_mark(mark)"""

    for student in db.get_students():
        print(student.get_values())
#    for i in range(1, 5):
#        print('--------------------')
#        for mark in db.get_marks_table(i):
#            print(mark)
