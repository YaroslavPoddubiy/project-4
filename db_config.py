import os
import sqlite3


def create_database(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS specialities
    (code INTEGER PRIMARY KEY, name TEXT, budget_places INTEGER, contract_places INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS coefficients
    (speciality_code INTEGER, subject_name TEXT, coef FLOAT, FOREIGN KEY (speciality_code) REFERENCES specialities(code))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS students
    (id INTEGER PRIMARY KEY, name TEXT, surname TEXT, middle_name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS points
    (student_id INTEGER, subject_name TEXT, point FLOAT, FOREIGN KEY (student_id) REFERENCES students(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS requests
    (speciality_code INTEGER, student_id INTEGER, competition_point FLOAT, FOREIGN KEY (speciality_code) REFERENCES specialities(code), 
    FOREIGN KEY (student_id) REFERENCES students(id))''')
    connection.commit()
    return cursor


def connect() -> sqlite3.Connection:
    db_exists = os.path.exists("db.sqlite3")
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()
    if not db_exists:
        cursor = create_database(connection)

    return connection


def main():
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS requests
            (speciality_code INTEGER, student_id INTEGER, FOREIGN KEY (speciality_code) REFERENCES specialities(code), 
            FOREIGN KEY (student_id) REFERENCES students(id))''')
    connection.commit()


if __name__ == '__main__':
    main()
