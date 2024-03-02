from cringe.config import host, user, password, database
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
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
        self.password.setPlaceholderText("Password")

    def attempt_login(self):
        username = self.login.text()
        password = self.password.text()

        if not username or not password:
            print("Ошибка входа", "Поля логин и пароль не могут быть пустыми.")
            return

        user_data = self.db_manager.check_credentials(username, password)
        if user_data:
            self.accept_login(user_data['role'])
        else:
            print("Ошибка входа", "Неверный логин или пароль.")

    def accept_login(self, user_role):
        self.main_window = MyWindow(self.db_manager)  # Создаем экземпляр главного окна
        self.main_window.show()  # Показываем главное окно
        self.close()  # Закрываем окно логина

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.attempt_login()
        else:
            super().keyPressEvent(event)


# Основной класс главного окна
class MyWindow(QMainWindow):
    def __init__(self, db_manager):
        super(MyWindow, self).__init__()
        loadUi("ui.ui", self)

        self.db_manager = db_manager

        self.schedule_b.clicked.connect(self.display_schedule)
        self.logout_b.clicked.connect(self.logout)
        self.settings_b.clicked.connect(self.display_settings)
        self.stats_b.clicked.connect(self.display_stats)

        # table
        self.stats_manager = StatsManager(self.combogroup, self.comboposition, self.combosex, self.stats_submit,
                                          db_manager,self.table, self)


    def display_schedule(self):
        result = self.db_manager.execute_query('''SELECT * FROM kurs ORDER BY id''')
        self.schedule_l.setText(result[0][1])
        self.stackedWidget.setCurrentWidget(self.schedule_pg)

    def logout(self):
        self.stackedWidget.setCurrentWidget(self.logout_pg)

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
        # Directly create and show the MyWindow instead of LoginWindow
        main_window = MyWindow(db_manager)
        main_window.show()
        sys.exit(app.exec_())
    except Exception as ex:
        print("[INFO] Error", ex)
    finally:
        if 'db_manager' in locals() or 'db_manager' in globals():
            db_manager.close()
        print("[INFO] Connection closed")
