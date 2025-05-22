#Импорт библиотек, окон и классов
import sys
from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMessageBox
from py_forms.Request import Ui_MainWindow
from py_forms.CreateRequest import Ui_Dialog as Ui_Create
from py_forms.Partners import Ui_Dialog as Ui_Partners
from py_forms.SostavRequest import Ui_Dialog as Ui_Sostav
from py_forms.ChangeRequest import Ui_Dialog as Ui_Change
from base import Base
from database import Database

#Класс окна заявок
class RequestWindow(QtWidgets.QMainWindow, Ui_MainWindow, Base):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = Database()

        #Вывод логотипа
        self.setWindowIcon(QtGui.QIcon(r"C:\Users\alena\PycharmProjects\request_system\static\Новые технологии.png"))
        self.logo_label.setPixmap(QtGui.QPixmap(r"C:\Users\alena\PycharmProjects\request_system\static\Новые технологии.png").scaled(100, 100, QtCore.Qt.AspectRatioMode.KeepAspectRatio))

        #Подключение кнопок
        self.add_pushButton.clicked.connect(self.create_request)
        self.update_pushButton_2.clicked.connect(self.show_request)
        self.sostav_pushButton.clicked.connect(self.sostav_request)z
        self.change_pushButton.clicked.connect(self.change_request)

        #Подключение таблиц
        self.show_request()

    #Функция вывода данных о заявках в таблицу
    def show_request(self):
        self.create_table(
            self.tableView,
            ['Номер', 'Название', 'Статус', 'Сумма', 'Время изготовления в дн.'],
            self.db.show_request()
        )

    def create_request(self):
        self.create_request_window = CreateRequestWindow()
        self.close()
        self.create_request_window.show()

    def sostav_request(self):
        try:
            request_id = self.selected_table_data(self.tableView)
            self.sostav_request = SostavRequestWindow(request_id)
            self.hide()
            self.sostav_request.show()
        except Exception as err:
            QMessageBox.warning(self, "Ошибка", "Выберете заявку")

    def change_request(self):
        try:
            request_id = self.selected_table_data(self.tableView)
            self.change_window = ChangeRequestWindow(request_id)
            self.hide()
            self.change_window.show()
        except Exception as err:
            QMessageBox.warning(self, "Ошибка", "Выберете заявку")



#Класс создания заявки
class CreateRequestWindow(QtWidgets.QWidget, Ui_Create, Base):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = Database()

        # Вывод логотипа
        self.setWindowIcon(QtGui.QIcon(r"C:\Users\alena\PycharmProjects\request_system\static\Новые технологии.png"))
        self.logo_label.setPixmap(
            QtGui.QPixmap(r"C:\Users\alena\PycharmProjects\request_system\static\Новые технологии.png").scaled(100, 100,

                                                                                                     QtCore.Qt.AspectRatioMode.KeepAspectRatio))

        #Подключение кнопок
        self.add_pushButton_3.clicked.connect(self.add_product)
        self.del_pushButton.clicked.connect(self.del_product)
        self.save_pushButton.clicked.connect(self.add_request)
        self.exit_pushButton.clicked.connect(self.del_request)

        # Подключение таблиц
        self.show_product()
        self.show_new_product()

    #Функция вывода данных о продуктах в таблицу
    def show_product(self):
        self.create_table(
            self.product_tableView,
            ['Номер', 'Тип', 'Материал', 'Название', 'Артикул', 'Цена', 'Время изготовления'],
            self.db.show_product()
        )

    # Функция вывода данных о продуктах в создаваемом заказе в таблицу
    def show_new_product(self):
        self.create_table(
            self.sostav_tableView,
            ['Номер', 'Продукт', 'Количестко', 'Цена за шт.', 'Сумма', 'Время изготовления общ.'],
            self.db.show_new_product()
        )

    #добавление продукта в заявку
    def add_product(self):
        try:
            kolvo = int(self.lineEdit.text())
            prod_id = self.selected_table_data(self.product_tableView)
            if prod_id is not None and kolvo is not None and kolvo > 0:
                self.db.add_product(prod_id, kolvo)
                self.lineEdit.clear()
                self.show_new_product()
            else:
                QMessageBox.warning(self, "Ошибка", "Выберете продукт и введите количество (целое положительное)")
        except Exception as err:
            QMessageBox.warning(self, "Ошибка", "Ошибка ввода")

    #Фуекция удаления продукта из состава заказа
    def del_product(self):
        try:
            prod_id = self.selected_table_data(self.sostav_tableView)
            self.db.del_product(prod_id)
            self.show_new_product()
        except Exception as err:
            QMessageBox.warning(self, "Ошибка", "Выберете продукт из состава заявки для удаления")

    def add_request(self):
        self.partners_window = PartnersWindow()
        self.partners_window.show()

    def del_request(self):
        reply = QMessageBox.question(self, "Подтверждение", "Вы хотите отменит заказ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.del_request()
            self.close()
            request_window.show()

#Класс редактирования заявки
class ChangeRequestWindow(QtWidgets.QWidget, Ui_Change, Base):
    def __init__(self, req_id):
        super().__init__()
        self.setupUi(self)
        self.db = Database()
        self.req_id = req_id

        # Вывод логотипа
        self.setWindowIcon(QtGui.QIcon(r"C:\Users\alena\PycharmProjects\request_system\static\Новые технологии.png"))
        self.logo_label.setPixmap(
            QtGui.QPixmap(r"C:\Users\alena\PycharmProjects\request_system\static\Новые технологии.png").scaled(100, 100,

                                                                                                     QtCore.Qt.AspectRatioMode.KeepAspectRatio))

        #Подключение кнопок
        self.add_pushButton_3.clicked.connect(self.add_product)
        self.del_pushButton.clicked.connect(self.del_product)
        self.exit_pushButton.clicked.connect(self.exit)

        # Подключение таблиц
        self.show_product()
        self.show_request_product()

    #Функция вывода данных о продуктах в таблицу
    def show_product(self):
        self.create_table(
            self.product_tableView,
            ['Номер', 'Тип', 'Материал', 'Название', 'Артикул', 'Цена', 'Время изготовления'],
            self.db.show_product()
        )

    # Функция вывода данных о продуктах в создаваемом заказе в таблицу
    def show_request_product(self):
        self.create_table(
            self.sostav_tableView,
            ['Номер', 'Продукт', 'Количестко', 'Цена за шт.', 'Сумма', 'Время изготовления общ.'],
            self.db.show_request_product(self.req_id)
        )

    #добавление продукта в заявку
    def add_product(self):
        try:
            kolvo = int(self.lineEdit.text())
            prod_id = self.selected_table_data(self.product_tableView)
            if prod_id is not None and kolvo is not None and kolvo > 0:
                self.lineEdit.clear()
                self.show_request_product()
            else:
                QMessageBox.warning(self, "Ошибка", "Выберете продукт и введите количество (целое положительное)")
        except Exception as err:
            QMessageBox.warning(self, "Ошибка", "Ошибка ввода")

    #Фуекция удаления продукта из состава заказа
    def del_product(self):
        try:
            prod_id = self.selected_table_data(self.sostav_tableView)
            self.db.del_product(prod_id)
            self.show_request_product()
        except Exception as err:
            QMessageBox.warning(self, "Ошибка", "Выберете продукт из состава заявки для удаления")

    def exit(self):
        self.close()
        request_window.show()

#Класс сохранения заявки с указанием партнера
class PartnersWindow(QtWidgets.QWidget, Ui_Partners, Base):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = Database()

        # Вывод логотипа
        self.setWindowIcon(
            QtGui.QIcon(r"C:\Users\alena\PycharmProjects\request_system\static\Новые технологии.png"))

        #Подключение кнопок
        self.save_pushButton.clicked.connect(self.save_request)
        self.exit_pushButton.clicked.connect(self.exit)

        #Подключение таблиц
        self.show_partners()

# Функция вывода данных о партнерах в таблицу
    def show_partners(self):
        self.create_table(
            self.partners_tableView,
            ['Номер', 'Тип', 'Название', 'Адрес', 'Директор', 'Телефон', 'Почта', 'Рейтинг'],
            self.db.show_partners()
        )

    def save_request(self):
        try:
            part_id = self.selected_table_data(self.partners_tableView)
            reply = QMessageBox.question(self, "Подтверждение", "Сохранить заказ", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.db.add_request(part_id)
                QMessageBox.information(self, "Упсех", "Заявка сохранена")
                self.hide()
                request_window.show()
        except Exception as err:
            QMessageBox.warning(self, "Ошибка", "Выберете партнера")

    def exit(self):
        self.close()

#Класс просмотра состава заявки
class SostavRequestWindow(QtWidgets.QWidget, Ui_Sostav, Base):
    def __init__(self, req_id):
        super().__init__()
        self.setupUi(self)
        self.db = Database()
        self.req_id = req_id

        # Вывод логотипа
        self.setWindowIcon(QtGui.QIcon(r"C:\Users\alena\PycharmProjects\request_system\static\Новые технологии.png"))
        self.logo_label.setPixmap(
            QtGui.QPixmap(r"C:\Users\alena\PycharmProjects\request_system\static\Новые технологии.png").scaled(100, 100,

                                                                                                     QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.exit_pushButton.clicked.connect(self.exit)

        self.show_sostav()

    # Функция вывода данных состава заявки
    def show_sostav(self):
        self.create_table(
            self.sostav_tableView,
            ['Номер', 'Продукт', 'Количестко', 'Цена за шт.', 'Сумма', 'Время изготовления общ.'],
            self.db.show_request_product(self.req_id)
        )

    def exit(self):
        self.close()
        request_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    request_window = RequestWindow()
    request_window.show()
    sys.exit(app.exec())