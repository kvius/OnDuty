import mysql.connector
from config import host, user, password, database
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView, QPushButton, QLineEdit, \
    QWidget, QHBoxLayout, QItemDelegate, QDateEdit, QComboBox, QMessageBox, QVBoxLayout, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate, Qt
import warnings
import sys

from database import DatabaseManager

from stats_funcs import StatsManager

from test import *

print(id)
print(cant_stay)

warnings.filterwarnings("ignore", category=DeprecationWarning)  # Ignore warnings


# Основной класс окна логина
class LoginWindow(QMainWindow):
    def __init__(self, db_manager):
        super(LoginWindow, self).__init__()
        loadUi("login.ui", self)
        self.db_manager = db_manager
        self.submit.clicked.connect(self.attempt_login)
        self.login.setPlaceholderText("Login")
        self.login.setFocus()
        self.password.setPlaceholderText("Password")

    def attempt_login(self):
        username = self.login.text()
        password = self.password.text()

        if not username or not password:
            print("Ошибка входа", "Поля логин и пароль не могут быть пустыми.")
            return

        user_data = self.db_manager.check_credentials(username, password)
        if user_data:
            self.accept_login(user_data['role'],user_data['group'])
        else:
            print("Ошибка входа", "Неверный логин или пароль.")

    def accept_login(self, user_role,user_group):
        self.main_window = MyWindow(self.db_manager,user_role,user_group)  # Создаем экземпляр главного окна
        self.main_window.show()  # Показываем главное окно
        self.close()  # Закрываем окно логина


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.attempt_login()
        else:
            super().keyPressEvent(event)


# Основной класс главного окна
class MyWindow(QMainWindow):
    def __init__(self, db_manager,role,group):
        super(MyWindow, self).__init__()
        loadUi("ui.ui", self)

        self.role_data= {
                "role":role,
                "group":group,
            }
        print(self.role_data)

        self.db_manager = db_manager

        self.schedule_b.clicked.connect(self.display_schedule)
        self.logout_b.clicked.connect(self.logout)
        self.settings_b.clicked.connect(self.display_settings)
        self.stats_b.clicked.connect(self.display_stats)
        self.pdf_b.clicked.connect(self.display_pdf)
        self.faq_b.clicked.connect(self.display_faq)
        self.search_b.clicked.connect(self.display_search)

        #faq
        self.container = QWidget()  # Создаем контейнер для виджетов
        self.layout = QVBoxLayout()  # Создаем вертикальное расположение для виджетов в контейнере
        self.container.setLayout(self.layout)

        self.faq_scroll.setWidget(self.container)  # Устанавливаем контейнер в качестве виджета для QScrollArea
        self.faq_scroll.setWidgetResizable(True)
        self.stretch_added = False# Разрешаем QScrollArea изменять размер контейнера
        self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");self.add_label(" text");





        # table
        self.stats_manager = StatsManager(self.combogroup, self.comboposition, self.combosex, self.stats_submit,
                                          db_manager,self.table, self,self.role_data)

    def add_label(self, text):
        if self.stretch_added:  # Если растяжимое пространство уже добавлено, удаляем его
            self.layout.removeItem(self.layout.itemAt(self.layout.count() - 1))
            self.stretch_added = False

        label = QLabel(text)  # Создаем QLabel с текстом
        label.setWordWrap(True)  # Разрешаем перенос слов, если текст не помещается
        self.layout.addWidget(label)  # Добавляем QLabel в вертикальное расположение

        if not self.stretch_added:  # Добавляем растяжимое пространство, если оно еще не добавлено
            self.layout.addStretch()
            self.stretch_added = True

    def display_pdf(self):
        self.stackedWidget.setCurrentWidget(self.pdf_pg)

    def display_faq(self):
        self.stackedWidget.setCurrentWidget(self.faq_pg)

    def display_search(self):
        self.stackedWidget.setCurrentWidget(self.search_pg)
    def display_schedule(self):
        result = self.db_manager.execute_query('''SELECT * FROM kurs ORDER BY id''')
        self.schedule_l.setText(result[0][1])
        self.stackedWidget.setCurrentWidget(self.schedule_pg)


    def logout(self):
        # Placeholder (add confirmation dialog if you like)
        self.login_window = LoginWindow(self.db_manager)
        self.login_window.show()
        self.close()  # Close the current main window

    def display_settings(self):
        self.stackedWidget.setCurrentWidget(self.settings_pg)

    def display_stats(self):
        self.stats_manager.load_data_into_table()
        self.stackedWidget.setCurrentWidget(self.stats_pg)


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        db_manager = DatabaseManager(host, user, password, database)
        db_manager.connect()
        # Create and show the LoginWindow instead of MyWindow
        login_window = LoginWindow(db_manager)
        login_window.show()
        sys.exit(app.exec_())
    except Exception as ex:
        print("[INFO] Error", ex)
    finally:
        if 'db_manager' in locals() or 'db_manager' in globals():
            db_manager.close()
        print("[INFO] Connection closed")
