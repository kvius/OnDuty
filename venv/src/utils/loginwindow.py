import MyWindow
from PyQt5.QtWidgets import  QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import  Qt


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