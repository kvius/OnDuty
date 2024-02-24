import mysql.connector
from config import host, user, password, database
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView, QPushButton, QLineEdit, QWidget, QHBoxLayout, QItemDelegate, QDateEdit,QComboBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QColor
import warnings
import sys

from test import *
print(id)
print(cant_stay)

warnings.filterwarnings("ignore", category=DeprecationWarning)  # Ignore warnings

# Class for managing the database
class DatabaseManager:
    def __init__(self, host, user, password, db_name):
        self.connection = None
        self.host = host
        self.user = user
        self.password = password
        self.db_name = database

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
        )

    def load_data(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()  # Добавляем коммит изменений
            print(f"Query executed successfully: {query}")
        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
        finally:
            cursor.close()

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        try:
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
            cursor.close()
            return None

    def check_credentials(self, username, password):
        self.connect()
        query = "SELECT role FROM admins WHERE login = %s AND password = %s"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return {"role": result[0]}
            else:
                return None
        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
            cursor.close()
            return None
    def close(self):
        if self.connection:
            self.connection.close()


class DateDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QDateEdit(parent)
        editor.setCalendarPopup(True)
        editor.setDisplayFormat('yyyy-MM-dd')
        self.noDate = QDate().currentDate()
        print(self.noDate)
        editor.setDate(QDate().currentDate())
        return editor

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
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.schedule_b.clicked.connect(self.display_schedule)
        self.logout_b.clicked.connect(self.logout)
        self.settings_b.clicked.connect(self.display_settings)
        self.stats_b.clicked.connect(self.display_stats)


        # table
        self.current_widget=None

        self.combogroup.currentIndexChanged.connect(self.load_data_into_table)
        self.comboposition.currentIndexChanged.connect(self.load_data_into_table)
        self.combosex.currentIndexChanged.connect(self.load_data_into_table)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellClicked.connect(self.on_cell_clicked)

    def display_schedule(self):
        result = self.db_manager.execute_query('''SELECT * FROM kurs ORDER BY id''')
        self.schedule_l.setText(result[0][1])
        self.stackedWidget.setCurrentWidget(self.schedule_pg)

    def logout(self):
        self.stackedWidget.setCurrentWidget(self.logout_pg)

    def display_settings(self):
        self.stackedWidget.setCurrentWidget(self.settings_pg)

    def display_stats(self):
        self.stats_submit.clicked.connect(self.submit)
        self.load_data_into_table()
        self.stackedWidget.setCurrentWidget(self.stats_pg)

    def load_data_into_table(self):
        self.query_txt = ""
        self.par=0
        self.cel_prev_row = None
        self.cel_prev_col = None
        self.query_arr=[]

        group = self.combogroup.currentText()
        position = self.comboposition.currentText()
        sex = self.combosex.currentText()

        # Initialize the base query and conditions
        base_query = "SELECT * FROM kurs"
        conditions = []
        print(group, position, sex)
        # Check each combo box for a user-selected value (assuming default values indicate 'no filter')
        if group != "Група":
            conditions.append(f"`group` = '{group}'")  # Replace group_column_name with your actual column name
        if position != "Посада":
            if position == "Курсанти":
                conditions.append(f"position = 'Курсант'")  # Replace position_column_name with your actual column name
            else:  # sergants
                conditions.append(f"(position = 'Сержант' or position = 'Командир'  or position = 'Старшина' )")
        if sex != "Стать":
            conditions.append(f"sex = '{sex}'")  # Replace sex_column_name with your actual column name

        # Construct the query with conditions if any

        if conditions:
            query = f"{base_query} WHERE {' AND '.join(conditions)} ORDER BY id"
        else:
            query = f"{base_query} ORDER BY id"
        print(query)
        results = self.db_manager.execute_query(query)
        print(results)
        self.table.setRowCount(0)  # Очищаем таблицу перед заполнением

        for row_number, row_data in enumerate(results):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.table.hideColumn(id)

        date_column_index = 11  # replace with the actual index of your date column
        self.date_delegate = DateDelegate()
        self.table.setItemDelegateForColumn(cant_stay, self.date_delegate)

    def selection_changed(self, selected, deselected):
        for index in selected.indexes():
            print(f"Выделен элемент: строка {index.row()}, столбец {index.column()}")
        #
        #     if isinstance(editor, QDateEdit):
        # # Теперь "editor" содержит ссылку на открытый QDateEdit
        # # ... (сохраните "editor" в переменную)

    def on_cell_clicked(self, row, column):
        if ( self.cel_prev_row != row or self.cel_prev_col != column):
            if self.current_widget:
                if isinstance(self.current_widget, QDateEdit):
                    self.save_changes_datepicker()
                if isinstance(self.current_widget, QComboBox):
                    self.save_changes(self.cel_prev_row,self.cel_prev_col)
        self.cel_prev_row = row
        self.cel_prev_col = column
        date_column_index = 11  # replace with the actual index of your date column
        if column == date_column_index:
            self.table.openPersistentEditor(self.table.item(row, column))
            self.current_widget = self.table.cellWidget(row, column)
            self.par=1
        if column == rank or column==position:
            combo_box = QComboBox()
            self.prev_combobox_text=self.table.item(row, column).text()
            # Determine possible values based on the column
            if column == rank:
                combo_box.addItems(["сол.", "с-т"])  # Replace with your rank values
            else:  # column == position
                combo_box.addItems(["курсант", "командир","сержант","старшина"])  # Replace with your position values

            # Set the current value of the combobox
            current_text = self.table.item(row, column).text() if self.table.item(row, column) else ""
            combo_box.setCurrentText(current_text)

            # Connect the currentIndexChanged signal
            combo_box.currentIndexChanged.connect(lambda idx, row=row, column=column: self.save_changes(row, column))

            # Set the combobox as the cell widget
            self.table.setCellWidget(row, column, combo_box)
            self.table.resizeColumnsToContents()

            self.current_widget = self.table.cellWidget(row, column)

    def save_changes_datepicker(self):

        row = self.cel_prev_row
        column = self.cel_prev_col
        # print(self.table.item(row, column).text())#!!!
        # Assuming the date column is using the CustomDateEdit via the DateDelegate
        index = self.table.model().index(row, column)
        editor = self.table.indexWidget(index)
        item = self.table.item(row, column)
        if self.date_delegate.noDate < editor.date():
            if editor and isinstance(editor, QDateEdit):
                # Manually commit the data to the model
                self.date_delegate.setModelData(editor, self.table.model(), index)
                # Close the editor
                item = self.table.item(row, column)
                self.table.closePersistentEditor(item)
                self.apply_changes_stats(row, column)
        else:
            self.table.closePersistentEditor(item)
            item.setText("None")
        self.current_widget=None


    def save_changes(self, row, column):
        # Get the selected text from the combobox
        combo_box = self.table.cellWidget(row, column)
        text = combo_box.currentText()

        # Remove the combobox and replace it with the updated text
        self.table.removeCellWidget(row, column)
        self.table.setItem(row, column, QTableWidgetItem(text))
        self.table.resizeColumnsToContents()
        print(self.prev_combobox_text, text)
        if self.prev_combobox_text != text:
            self.apply_changes_stats(row, column)
        self.current_widget=None

    def apply_changes_stats(self,row,column):
        item = self.table.item(row, column)
        id_txt = self.table.item(row, id).text()
        item.setForeground(QColor(255, 0, 0))

        # Формирование текста запроса для каждого изменения
        self.query_arr.append(f"UPDATE kurs SET `{columns[column]}` = '{item.text()}' WHERE `id` = '{id_txt}';")

    def submit(self):
        print(self.query_arr)
        for query in self.query_arr:
            db_manager.load_data(query)
        self.load_data_into_table()



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

