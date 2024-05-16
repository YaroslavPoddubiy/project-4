import db_controller
from db_config import connect
import json
from faker import Faker
import random


def specialities_fill():
    with open("specialities.json", "r", encoding='utf-8') as json_file:
        specialities = json.load(json_file)
        for speciality in specialities:
            new_spec = db_controller.Speciality(speciality["code"], speciality["name"], speciality["budget_places"],
                                                speciality["contract_places"])
            new_spec.save()

    connection.commit()


def students_fill():
    fake = Faker(locale="uk")
    optional_subjects = ["Українська література", "Біологія", "Хімія", "Фізика", "Географія", "Іноземна мова"]
    for _ in range(500):
        try:
            student = db_controller.Student(*fake.full_name().split())
        except (TypeError, ValueError):
            continue
        student.points = {"Українська мова": random.randint(120, 200), "Математика": random.randint(120, 200),
                          "Історія України": random.randint(120, 200), random.choice(optional_subjects): random.randint(120, 200)}
        student.save()


def coefs_fill():
    coefs_names = ["Українська мова", "Математика", "Історія України", "Іноземна мова", "Біологія", "Фізика", "Хімія",
                   "Українська література", "Географія", "Творчий конкурс"]
    with open("coefs1.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            coefs_dict = {}
            line_list = line.split()
            speciality = db_controller.Speciality.filter(code=int(line_list[0]))
            if speciality:
                speciality: db_controller.Speciality = speciality[0]
                for i in range(len(coefs_names)):
                    coefs_dict[coefs_names[i]] = float(line_list[i + 1])
                speciality.coefs = coefs_dict
                speciality.save()


def points_fill():
    pass


def requests_fill():
    students = db_controller.Student.get_all()
    for student in students:
        student.make_random_requests()


connection = connect()
cursor = connection.cursor()

# specialities_fill()
# coefs_fill()
students_fill()
requests_fill()
# cursor.execute('''INSERT INTO specialities (code, name, budget_places, contract_places) VALUES (?, ?, ?, ?)''',
#                (121, "Інженерія програмного забезпечення", 50, 50))
# connection.commit()
