import db_controller
from db_config import connect
import requests
from faker import Faker

# speciality = db_controller.Speciality(121, "Інженерія програмного забезпечення", 75, 120)
# speciality.save()

# sp = db_controller.Speciality.filter(code=121)
# if sp:
#     sp = sp[0]
# sp.coefs = {"Математика": 0.5, "Українська мова": 0.3, "Англійська мова": 0.2}
# print(sp)
# sp.contract_places = 20
# sp.save()
#
# print(sp)
#
# print(str(db_controller.Speciality.get_all()))
# print(str(db_controller.Speciality.filter(name="Інженерія програмного забезпечення")))
# student = db_controller.Student.filter(name="Ярослав")[0]
# student.points = {"Математика": 192, "Українська мова": 186, "Англійська мова": 191}
# student.save()
# print(student.points)
# text = ""
# with open("coefs.txt", "r", encoding="utf-8") as file:
#     text = file.read()
#     text = text.replace("\t", " ")
#     text = text.replace(",", ".")
#     text = text.replace("-", "0")
#
# with open("coefs1.txt", "w", encoding="utf-8") as file:
#     file.write(text)


# fake = Faker(locale='uk')
# print(fake.full_name())
# response = requests.request("GET", "https://api.namefake.com/ukrainian-ukraine/random/")
# print(response.json())

# spec = db_controller.Speciality.filter(code=121)
# print(spec[0].coefs)
#
# student = db_controller.Student.filter(id=1)[0]
# student.make_request(121)
connection = connect()
cursor = connection.cursor()

# specs = db_controller.Speciality.get_all()
# for spec in specs:
#     if not spec.coefs:
#         cursor.execute("DELETE FROM specialities WHERE (code=(?))", (spec.code, ))
# connection.commit()
# student = db_controller.Student.filter(id=48)[0]
# student.make_request(202)
# cursor.execute("ALTER TABLE students RENAME TO old_students")
# cursor.execute("ALTER TABLE specialities RENAME TO old_specialities")
# cursor.execute("ALTER TABLE coefficients RENAME TO old_coefficients")
# cursor.execute("ALTER TABLE points RENAME TO old_points")
# cursor.execute("ALTER TABLE requests RENAME TO old_requests")
# cursor.execute('''CREATE TABLE IF NOT EXISTS specialities
# (code INTEGER PRIMARY KEY, name TEXT, budget_places INTEGER, contract_places INTEGER)''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS coefficients
# (speciality_code INTEGER, subject_name TEXT, coef FLOAT, FOREIGN KEY (speciality_code) REFERENCES specialities(code))''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS points
# (student_id INTEGER, subject_name TEXT, point FLOAT, FOREIGN KEY (student_id) REFERENCES students(id))''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS requests
# (speciality_code INTEGER, student_id INTEGER, competition_point FLOAT, FOREIGN KEY (speciality_code) REFERENCES specialities(code),
# FOREIGN KEY (student_id) REFERENCES students(id))''')
# cursor.execute("ALTER TABLE requests ADD competition_point FLOAT")
# cursor.execute("INSERT INTO specialities SELECT * FROM old_specialities")
# cursor.execute("INSERT INTO coefficients SELECT * FROM old_coefficients")
# cursor.execute("INSERT INTO points SELECT * FROM old_points")
# cursor.execute("INSERT INTO requests SELECT * FROM old_requests")
# cursor.execute("CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT, surname TEXT, middle_name TEXT, "
#                "CONSTRAINT unique_name UNIQUE (surname, name, middle_name))")
# cursor.execute("INSERT INTO students SELECT * FROM old_students")
# cursor.execute("DROP TABLE old_students")
# cursor.execute("DROP TABLE old_coefficients")
# cursor.execute("DROP TABLE old_points")
# cursor.execute("DROP TABLE old_requests")
# cursor.execute("DROP TABLE old_specialities")
# cursor.execute("INSERT INTO specialities (code, name, budget_places, contract_places) "
#                "VALUES (?, ?, ?, ?)", (121, "Інженерія програмного забезпечення", 150, 50))
spec = db_controller.Speciality.filter(code=121)[0]
spec.coefs = {"Українська мова": 0.3, "Математика": 0.5, "Історія України": 0.2, "Іноземна мова": 0.3,
"Біологія": 0.2, "Фізика": 0.4, "Хімія": 0.2, "Українська література": 0, "Географія": 0, "Творчий конкурс": 0}
spec.save()
# connection.commit()
