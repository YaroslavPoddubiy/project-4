import random
import sqlite3
from db_config import connect


connection = connect()
cursor = connection.cursor()


SUBJECTS = ("українська мова", "математика", "історія україни", "іноземна мова", "біологія", "фізика", "хімія",
            "українська література", "географія", "творчий конкурс")


class Speciality:
    def __init__(self, code, name, budget_places, contract_places, coefs: dict = None):
        self.code = code
        self.name = name
        self.budget_places = budget_places
        self.contract_places = contract_places
        self.__coefs = dict()
        self.coefs = coefs

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, sp_code):
        self.__code = int(sp_code)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def budget_places(self):
        return self.__budget_places

    @budget_places.setter
    def budget_places(self, places):
        self.__budget_places = int(places)

    @property
    def contract_places(self):
        return self.__contract_places

    @contract_places.setter
    def contract_places(self, places):
        self.__contract_places = int(places)

    @property
    def coefs(self):
        cursor.execute("SELECT * FROM coefficients WHERE (speciality_code = ?)", (self.code, ))
        coefficients = cursor.fetchall()
        coefs_dict = {}
        for coef in coefficients:
            coefs_dict[coef[1]] = coef[2]
        return coefs_dict

    @coefs.setter
    def coefs(self, coefficients):
        if coefficients:
            for coef in coefficients:
                self.__coefs[coef] = coefficients[coef]

    @property
    def requests(self):
        cursor.execute("SELECT student_id, competition_point FROM requests WHERE (speciality_code=(?))", (self.code, ))
        reqs = cursor.fetchall()
        requests_dict = {}
        for i in range(len(reqs)):
            requests_dict[reqs[i][0]] = reqs[i][1]
        return requests_dict

    @staticmethod
    def get_all():
        cursor.execute('''SELECT * FROM specialities''')
        specialities = cursor.fetchall()
        for i in range(len(specialities)):
            specialities[i] = Speciality(*specialities[i])
        return specialities

    @staticmethod
    def filter(**filters):
        keys = ""
        for fltr in filters:
            keys += str(fltr) + " = ?" + " AND "
        if keys:
            keys = " WHERE (" + keys[:-5] + ") "
        cursor.execute("SELECT * FROM specialities " + keys, tuple(filters.values()))
        specialities = cursor.fetchall()
        for i in range(len(specialities)):
            specialities[i] = Speciality(*specialities[i])
        return specialities

    def save(self):
        is_new = True
        specialities = Speciality.get_all()
        for speciality in specialities:
            if speciality.code == self.code:
                is_new = False
                break
        if is_new:
            cursor.execute("INSERT INTO specialities (code, name, budget_places, contract_places) VALUES (?, ?, ?, ?)",
                           (self.code, self.name, self.budget_places, self.contract_places))
        else:
            cursor.execute("UPDATE specialities SET name = ?, budget_places = ?, contract_places = ? WHERE code = ?",
                           (self.name, self.budget_places, self.contract_places, self.code))
        if self.__coefs:
            existing_coefs = [item[1] for item in self.coefs]
            for coef in self.__coefs:
                if coef in existing_coefs:
                    cursor.execute("UPDATE coefficients SET coef = ? WHERE speciality_code = ? AND subject_name = ?",
                                   (self.__coefs[coef], self.code, coef))
                else:
                    cursor.execute("INSERT INTO coefficients (speciality_code, subject_name, coef) VALUES (?, ?, ?)",
                                   (self.code, coef, self.__coefs[coef]))
        connection.commit()

    def __str__(self):
        return f"Код: {self.code}\nНазва: {self.name}\nКількість бюджетних місць: {self.budget_places}\n" \
               f"Кількість контрактних місць: {self.contract_places}\nВагові коефіцієнти: {self.coefs}"


class Student:
    def __init__(self, name, surname, middle_name, points=None, id=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.middle_name = middle_name
        self.__points = None
        self.points = points

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name: str):
        if not isinstance(new_name, str):
            raise TypeError("Ім'я повинно бути символьним")
        if not new_name.isalpha():
            raise ValueError("Ім'я повинно містити лише букви")
        self.__name = new_name

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, new_surname: str):
        if not isinstance(new_surname, str):
            raise TypeError("Прізвище повинно бути символьним")
        if not new_surname.isalpha():
            raise ValueError("Прізвище повинно містити лише букви")
        self.__surname = new_surname

    @property
    def middle_name(self):
        return self.__middle_name

    @middle_name.setter
    def middle_name(self, new_middle_name: str):
        if not isinstance(new_middle_name, str):
            raise TypeError("По-батькові повинно бути символьним")
        if not new_middle_name.isalpha():
            raise ValueError("По-батькові повинно містити лише букви")
        self.__middle_name = new_middle_name

    @property
    def points(self):
        if self.id:
            cursor.execute("SELECT subject_name, point FROM points WHERE (student_id = ?)", (self.id, ))
            points_dict = dict()
            points = cursor.fetchall()
            for i in range(len(points)):
                points_dict[points[i][0]] = points[i][1]
            return points_dict

    @points.setter
    def points(self, student_points: dict | None):
        if self.points and student_points:
            raise TypeError("Студент уже має бали")
        if not student_points:
            return
        if not isinstance(student_points, dict):
            raise TypeError("Бали повинні подаватися у вигляді словника")
        for subject in student_points:
            if subject.lower() not in SUBJECTS:
                raise ValueError("Не існує предмета", subject)
            if student_points[subject] < 120 or student_points[subject] > 200:
                raise ValueError("Бал повинен бути в межах від 120 до 200")
        else:
            self.__points = student_points

    def get_requests(self):
        if not self.id:
            return None
        cursor.execute("SELECT speciality_code FROM requests WHERE (student_id=(?))", (self.id, ))
        requests = cursor.fetchall()
        if requests:
            requests = tuple(request[0] for request in requests)
        return requests

    def make_request(self, speciality_code):
        if not self.id:
            raise TypeError("Student object must be saved before this action")
        if len(self.get_requests()) >= 5:
            raise TypeError("Досягнуто максимальної кількості заявок")
        if speciality_code in self.get_requests():
            raise ValueError("Заявку на цю спеціальність вже подано")
        all_coefficients = Speciality.filter(code=speciality_code)[0].coefs
        coefficients = {}
        points = self.points
        for coef in all_coefficients:
            if coef in points:
                coefficients[coef] = all_coefficients[coef]
        sorted_coefs = sorted(coefficients)
        competition_point = 0
        coefs_sum = 0
        for subject in points:
            coefs_sum += coefficients[subject]
        if coefs_sum < 1:
            raise ValueError("Не здано потрібні предмети")
        if coefs_sum > 1:
            for i in range(len(coefficients)):
                if coefs_sum - coefficients[sorted_coefs[i]] <= 1:
                    same_coefs = [subject for subject in coefficients
                                  if coefficients[subject] == coefficients[sorted_coefs[i]]]
                    lowest_point = 201
                    coef_to_delete = None
                    for coef in same_coefs:
                        if points[coef] < lowest_point:
                            coef_to_delete = coef
                            lowest_point = points[coef]
                    del points[coef_to_delete]
                    break
        for subject in points:
            competition_point += points[subject] * coefficients[subject]
        cursor.execute("INSERT INTO requests (speciality_code, student_id, competition_point) VALUES (?, ?, ?)",
                       (speciality_code, self.id, competition_point))
        connection.commit()

    def make_random_requests(self):
        specs = Speciality.get_all()
        points = self.points

        for _ in range(5):
            while True:
                spec = random.choice(specs)
                coefs = spec.coefs
                coefs_sum = 0
                for subject in self.points:
                    coefs_sum += coefs[subject]
                if coefs_sum >= 1:
                    self.make_request(spec.code)
                    specs.remove(spec)
                    break

    @staticmethod
    def get_all():
        cursor.execute('''SELECT * FROM students''')
        students = cursor.fetchall()
        for i in range(len(students)):
            students[i] = Student(*students[i][1:], id=students[i][0])
        return students

    @staticmethod
    def filter(**filters):
        keys = ""
        for fltr in filters:
            keys += str(fltr) + " = ?" + " AND "
        if keys:
            keys = " WHERE (" + keys[:-5] + ") "
        cursor.execute("SELECT * FROM students " + keys, tuple(filters.values()))
        students = cursor.fetchall()
        for i in range(len(students)):
            students[i] = Student(*students[i][1:], id=students[i][0])
        return students

    def save(self):
        if not self.id:
            cursor.execute("INSERT INTO students (name, surname, middle_name) VALUES (?, ?, ?)",
                           (self.name, self.surname, self.middle_name))
            connection.commit()
            students = Student.get_all()
            student_id = 0 if not students else students[-1].id
            self.id = student_id
            if self.__points:
                for subject in self.__points:
                    cursor.execute("INSERT INTO points (student_id, subject_name, point) VALUES (?, ?, ?)",
                                   (student_id, subject, self.__points[subject]))
        else:
            cursor.execute("UPDATE students SET name = ?, surname = ?, middle_name = ? WHERE id = ?",
                           (self.name, self.surname, self.middle_name, self.id))
            if self.__points:
                for subject in self.__points:
                    cursor.execute("INSERT INTO points (student_id, subject_name, point) VALUES (?, ?, ?)",
                                   (self.id, subject, self.__points[subject]))

        connection.commit()

    def __str__(self):
        return f'{self.name} {self.surname} {self.middle_name}\n{self.points}'
