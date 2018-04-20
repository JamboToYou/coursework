
class Student():
    def __init__(self, studentId, firstName, lastName, course, faculty, speciality):
        self._studentId = studentId
        self._firstName = firstName
        self._lastName = lastName
        self._course = course
        self._faculty = faculty
        self._speciality = speciality

    def __repr__(self):
        return '[{}] {} {} : {} course, {}, {}'.format(self._studentId, self._firstName, self._lastName, self._course, self._faculty, self._speciality)

    def get_values(self):
        return \
            {
                "studentId": self._studentId,
                "firstName": self._firstName,
                "lastName": self._lastName,
                "course": self._course,
                "faculty": self._faculty,
                "speciality": self._speciality
            }

    @staticmethod
    def form_values_for_db(student):
        return (
            student['firstName'],
            student['lastName'],
            student['course'],
            student['specialityId']
        )


class Mark():
    def __init__(self, studentId, lastName, firstName, mark, subject):
        self._studentId = studentId
        self._lastName = lastName
        self._firstName = firstName
        self._mark = mark
        self._subject = subject

    def get_values(self):
        return \
            {
                "studentId": self._studentId,
                "lastName": self._lastName,
                "firstName": self._firstName,
                "mark": self._mark,
                "subject": self._subject
            }

    @staticmethod
    def form_values_for_db(mark):
        return (
            mark['mark'],
            mark['studentId'],
            mark['subjectId']
        )


class Subject():
    def __init__(self, subjectId, subject):
        self._subjectId = subjectId
        self._subject = subject

    def get_values(self):
        return \
            {
                "subjectId": self._subjectId,
                "subject": self._subject
            }

    @staticmethod
    def form_values_for_db(subject):
        return subject['subject']


class Faculty():
    def __init__(self, facultyId, faculty):
        self._facultyId = facultyId
        self._faculty = faculty

    def get_values(self):
        return \
            {
                "facultyId": self._facultyId,
                "faculty": self._faculty
            }

    @staticmethod
    def form_values_for_db(faculty):
        return faculty['faculty']


class Speciality():
    def __init__(self, specialityId, facultyId, speciality):
        self._specialityId = specialityId
        self._facultyId = facultyId
        self._speciality = speciality

    def get_values(self):
        return \
            {
                "specialityId": self._specialityId,
                "facultyId": self._facultyId,
                "speciality": self._speciality
            }

    @staticmethod
    def form_values_for_db(speciality):
        return \
            (
                speciality['facultyId'],
                speciality['speciality']
            )