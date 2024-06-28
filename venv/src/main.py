import mysql.connector
from pyqt5_plugins.examplebuttonplugin import QtGui
import os
from utils.config import host, user, password, database
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView, QPushButton, QLineEdit, \
    QWidget, QHBoxLayout, QItemDelegate, QDateEdit, QComboBox, QMessageBox, QVBoxLayout, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate, Qt
import warnings
import sys

from utils.database import DatabaseManager

from utils.stats_funcs import StatsManager

from utils.test import *
from utils.schedule_arr import fill_schedule_table,cell_clicked

from utils.do import make_word
from utils.search import search
from datetime import datetime, timedelta
print(id)
print(cant_stay)

warnings.filterwarnings("ignore", category=DeprecationWarning)  # Ignore warnings



from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

# Цвета
colors = {
    "yellow_border": QColor(255, 255, 0),
    "blue_border": QColor(0, 0, 255),
    "white_background": QColor(255, 255, 255),
    "grey_background": QColor(220, 220, 220),
    "white_border": QColor(255, 255, 255),
    "main": QColor("#5A9BD5"),  # Red
    "maindark": QColor("#4A8CC5"),  # Red
}

class BorderAndBackgroundDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()

        # Get the column number
        col = index.column()

        # Set background color for even columns to red
        if col % 2 == 0:
            painter.fillRect(option.rect, colors["main"])  # Red for even columns
        else:
            painter.fillRect(option.rect, colors["maindark"])  # Light grey for odd columns

        # Call the base class method to paint the item
        super().paint(painter, option, index)

        # Set borders for the first 4 rows and the next 4 rows
        row = index.row()
        rect = option.rect

        # Apply white border for odd columns

        if row < 4:
            pen = QPen(colors["yellow_border"], 2)  # Yellow border
        elif 4 <= row < 8:
            pen = QPen(colors["blue_border"], 2)  # Blue border
        else:
            pen = QPen(colors["white_border"], 2)  # White border

        painter.setPen(pen)

        if row == 0 or row == 4:
            painter.drawLine(rect.topLeft(), rect.topRight())  # Top border

        if row == 3 or row == 7:
            painter.drawLine(rect.bottomLeft(), rect.bottomRight())  # Bottom border

        if col == 0:
            painter.drawLine(rect.topLeft(), rect.bottomLeft())  # Left border

        if col == index.model().columnCount() - 1:
            painter.drawLine(rect.topRight(), rect.bottomRight())  # Right border

        painter.restore()


        # Override borders for grey background cells to be white



# Основной класс окна логина
class LoginWindow(QMainWindow):
    def __init__(self, db_manager):
        super(LoginWindow, self).__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'ui', 'login.ui')
        loadUi(ui_path, self)
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
        ui_path = os.path.join(os.path.dirname(__file__), 'ui', 'ui.ui')
        loadUi(ui_path, self)

        self.role_data= {
                "role":role,
                "group":group,
            }
        if role != "senioradmin":
            self.widget_3.setParent(None)
            self.calculate_schedule.setParent(None)
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
        self.add_label("Як міняти людей в нарядах",bold=True)
        self.add_label("альт + клік на комірку")
        self.add_label("Як міняти группу в наряді", bold=True)
        self.add_label("ктрл + клік на комірку")
        self.add_label("Як видаляти людей з наряду", bold=True)
        self.add_label("шифт + клік на комірку")



        # table
        self.stats_manager = StatsManager(self.combogroup, self.comboposition, self.combosex, self.stats_submit,
                                          db_manager,self.table, self,self.role_data)

        #schedule
        self.schedule_date_l.setAlignment(Qt.AlignCenter)
        self.schedule_table.setItemDelegate(BorderAndBackgroundDelegate())

        #export
        self.export_button.clicked.connect(lambda : make_word(db_manager,self))

        self.search_button.clicked.connect(lambda: search(db_manager,self))

    from PyQt5.QtWidgets import QLabel
    from PyQt5.QtGui import QFont



    def add_label(self, text, bold=False):
        if self.stretch_added:  # Если растяжимое пространство уже добавлено, удаляем его
            self.layout.removeItem(self.layout.itemAt(self.layout.count() - 1))
            self.stretch_added = False

        label = QLabel(text)  # Создаем QLabel с текстом
        label.setWordWrap(True)  # Разрешаем перенос слов, если текст не помещается

        if bold:  # Проверяем, должен ли текст быть жирным
            font = label.font()  # Получаем текущий шрифт
            font.setBold(True)  # Устанавливаем шрифт жирным
            label.setFont(font)  # Применяем шрифт к label

        self.layout.addWidget(label)  # Добавляем QLabel в вертикальное расположение

        if not self.stretch_added:  # Добавляем растяжимое пространство, если оно еще не добавлено
            self.layout.addStretch()
            self.stretch_added = True

    def display_pdf(self):
        self.date_start.setDate(QDate.currentDate())
        self.date_end.setDate(QDate.currentDate().addDays(1))
        self.stackedWidget.setCurrentWidget(self.pdf_pg)

    def display_faq(self):
        self.stackedWidget.setCurrentWidget(self.faq_pg)

    def display_search(self):
        #search(self.db_manager,self)
        self.stackedWidget.setCurrentWidget(self.search_pg)


    def display_schedule(self):



        # Customize table backgrounds
        for row in range(self.schedule_table.rowCount()):
            for col in range(self.schedule_table.columnCount()):
                item = self.schedule_table.item(row, col)
                if not item:
                    item = QTableWidgetItem()
                    self.schedule_table.setItem(row, col, item)
        fill_schedule_table(self.schedule_table,self.db_manager,self,False)
        self.stackedWidget.setCurrentWidget(self.schedule_pg)
        # сместить
        self.schedule_table.cellClicked.connect(lambda row, col: cell_clicked(row, col, self.schedule_table,self.db_manager,self))
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
