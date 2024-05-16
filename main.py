import db_controller
import sys
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox


class SpecialityWindow(QMainWindow):
    def __init__(self):
        super(SpecialityWindow, self).__init__()
        loadUi("uis/MainWindow.ui", self)

        self.setWindowTitle("Список спеціальностей")

        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 630)

        self.load_data()

        self.lineEdit.textChanged.connect(self.filter)
        self.more.clicked.connect(self.speciality_info)
        self.students_list.clicked.connect(self.students)
        self.request.clicked.connect(self.make_request)

    def load_data(self):
        specialities = db_controller.Speciality.get_all()
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.setRowCount(len(specialities))
        for i in range(len(specialities)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(specialities[i].code)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(specialities[i].name))

    def filter(self, text):
        text = text.strip().lower()
        visible_rows = []
        row_count = self.tableWidget.rowCount()

        for row in range(row_count):
            if text in self.tableWidget.item(row, 0).text().lower() or \
                    text in self.tableWidget.item(row, 1).text().lower():
                visible_rows.append(row)

        for row in range(row_count):
            self.tableWidget.setRowHidden(row, True)

        if text == "":
            visible_rows = [i for i in range(row_count)]

        for row in visible_rows:
            self.tableWidget.setRowHidden(row, False)

    def speciality_info(self):
        item = self.tableWidget.selectedIndexes()
        if item:
            code = int(self.tableWidget.item(item[0].row(), 0).text())
            self.window = CoefsWindow(code)
            self.window.show()

    def students(self):
        item = self.tableWidget.selectedIndexes()
        if item:
            code = int(self.tableWidget.item(item[0].row(), 0).text())
            self.students_window = StudentsWindow(code)
            self.students_window.show()

    def make_request(self):
        item = self.tableWidget.selectedIndexes()
        if item:
            code = int(self.tableWidget.item(item[0].row(), 0).text())
            self.check_window = NameCheckWindow(code)
            self.check_window.show()


def make_request(student_id, speciality_code):
    student = db_controller.Student.filter(id=student_id)[0]
    speciality = db_controller.Speciality.filter(code=speciality_code)[0]
    try:
        student.make_request(speciality_code)
        text = f"{student.surname} {student.name} {student.middle_name}, " \
               f"Вашу заявку на спеціальність {speciality_code}: {speciality.name}, прийнято."
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setText(text)
        msgbox.exec_()
    except (ValueError, TypeError) as ex:
        text = str(ex)
        print(text)
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setText(text)
        msgbox.exec_()


class CoefsWindow(QDialog):
    def __init__(self, speciality_code):
        self.__speciality_code = speciality_code
        super(CoefsWindow, self).__init__()
        loadUi("uis/CoefsWindow.ui", self)

        self.setWindowTitle("Вагові коефіцієнти")

        self.load_data()

    def load_data(self):
        speciality = db_controller.Speciality.filter(code=int(self.__speciality_code))
        if speciality:
            speciality: db_controller.Speciality = speciality[0]

            self.tableWidget.setRowCount(1)

            coefs = speciality.coefs
            for column, coef in enumerate(coefs.values()):
                self.tableWidget.setItem(0, column, QTableWidgetItem(str(coef)))


class StudentsWindow(QMainWindow):
    def __init__(self, speciality_code):
        self.__speciality_code = speciality_code
        super().__init__()
        loadUi("uis/StudentsWindow.ui", self)

        self.setWindowTitle("Список кандидатів")

        self.tableWidget.setColumnWidth(0, 600)
        self.tableWidget.setColumnWidth(1, 120)

        self.load_data()
        self.lineEdit.textChanged.connect(self.filter)

    def load_data(self):
        speciality = db_controller.Speciality.filter(code=self.__speciality_code)[0]
        requests: dict = speciality.requests
        sorted_requests = sorted(requests.items(), key=lambda x: x[1], reverse=True)
        new_requests = {}
        for request in sorted_requests:
            student = db_controller.Student.filter(id=request[0])[0]
            full_name = student.surname + " " + student.name + " " + student.middle_name
            new_requests[full_name] = request[1]

        self.tableWidget.setRowCount(len(new_requests))
        for row, student in enumerate(new_requests):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(student)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(round(new_requests[student], 1))))

    def filter(self, text):
        text = text.strip().lower()
        visible_rows = []
        row_count = self.tableWidget.rowCount()

        for row in range(row_count):
            if text in self.tableWidget.item(row, 0).text().lower():
                visible_rows.append(row)

        for row in range(row_count):
            self.tableWidget.setRowHidden(row, True)

        if text == "":
            visible_rows = [i for i in range(row_count)]

        for row in visible_rows:
            self.tableWidget.setRowHidden(row, False)


class NameCheckWindow(QDialog):
    def __init__(self, speciality_code):
        self.__speciality_code = speciality_code
        super().__init__()
        loadUi("uis/NameCheckWindow.ui", self)

        self.setWindowTitle("Перевірка імені")

        self.pushButton.clicked.connect(self.check)

    def check(self):
        text: str = self.lineEdit.text()
        text_list = text.strip().split()
        if len(text_list) != 3:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText("Потрібно ввести прізвище, ім'я і по-батькові")
            msgbox.exec_()
            return
        surname, name, middle_name = text_list
        student = db_controller.Student.filter(surname=surname, name=name, middle_name=middle_name)
        if student:
            make_request(student[0].id, self.__speciality_code)
        else:
            self.new_student_window = NewStudentWindow(self.__speciality_code)
            self.new_student_window.show()


class NewStudentWindow(QDialog):
    def __init__(self, speciality_code):
        self.__speciality_code = speciality_code
        super().__init__()
        loadUi("uis/NewStudentWindow.ui", self)

        self.setWindowTitle("Новий профіль")

        self.pushButton.clicked.connect(self.create_new_student)

    def create_new_student(self):
        surname = self.surname.text()
        name = self.name.text()
        middle_name = self.middle_name.text()
        math = float(self.math.text())
        ukrainian = float(self.ukrainian.text())
        history = float(self.history.text())
        optional_subject = self.comboBox.currentText()
        optional_subject_point = float(self.optional_subject.text())
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Warning)
        try:
            student = db_controller.Student(name, surname, middle_name, {"Українська мова": ukrainian, "Математика": math,
                                            "Історія України": history, optional_subject: optional_subject_point})
            student.save()
            make_request(student.id, self.__speciality_code)
        except (TypeError, ValueError) as ex:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText(str(ex))
            msgbox.exec_()
        except Exception as ex:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText("Такий студент вже існує")
            msgbox.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SpecialityWindow()
    window.show()
    sys.exit(app.exec())
