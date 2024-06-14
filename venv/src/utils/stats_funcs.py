from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QDateEdit,QComboBox,QMessageBox
from PyQt5.QtGui import QColor,QIcon
from src.utils import datedelegate
from src.utils.test import *

class StatsManager:
    def __init__(self, combogroup, comboposition, combosex, stats_submit, db_manager, table,parent,role_data):
        self.combogroup = combogroup
        self.comboposition = comboposition
        self.combosex = combosex
        self.stats_submit = stats_submit
        self.db_manager = db_manager
        self.table = table
        self.parent=parent

        self.role=role_data["role"]
        self.group = role_data["group"]

        self.current_widget = None

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.combogroup.currentIndexChanged.connect(self.load_data_into_table)
        self.comboposition.currentIndexChanged.connect(self.load_data_into_table)
        self.combosex.currentIndexChanged.connect(self.load_data_into_table)

        self.stats_submit.clicked.connect(self.submit)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellClicked.connect(self.on_cell_clicked)




    def load_data_into_table(self):
        self.query_txt = ""
        self.par=0
        self.cel_prev_row = None
        self.cel_prev_col = None
        self.query_arr=[]

        grp = self.combogroup.currentText()
        pos = self.comboposition.currentText()
        sex = self.combosex.currentText()

        # Initialize the base query and conditions
        base_query = "SELECT * FROM kurs"
        conditions = []
        print(grp, pos, sex)
        # Check each combo box for a user-selected value (assuming default values indicate 'no filter')
        if grp != "Група":
            conditions.append(f"`group` = '{grp}'")  # Replace group_column_name with your actual column name
        if pos != "Посада":
            if pos == "Курсанти":
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

        self.icon = QIcon('edit.png')

        for row_number, row_data in enumerate(results):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                # Создаем элемент таблицы с данными
                item = QTableWidgetItem(str(data))

                # Проверяем, находится ли текущая колонка в списке индексов для специальной обработк
                if (column_number in [rank, position, cant_stay] and  self.role == "senioradmin") or (column_number == cant_stay and (self.role == "admin" and str(row_data[group]) == self.group)) :
                    print(1)
                    item.setIcon(self.icon)

                    # Также можно добавить tooltip, если нужно
                    item.setToolTip("Это поле можно редактировать")

                # Устанавливаем элемент в таблицу
                self.table.setItem(row_number, column_number, item)
        self.table.hideColumn(id)
        self.table.setColumnWidth(2, 500)
        date_column_index = 11  # replace with the actual index of your date column
        self.date_delegate = datedelegate.DateDelegate()
        self.table.setItemDelegateForColumn(cant_stay, self.date_delegate)
        # kastil

    def on_cell_clicked(self, row, column):
        print(1)
        if ( self.cel_prev_row != row or self.cel_prev_col != column):
            if self.current_widget:
                if isinstance(self.current_widget, QDateEdit):
                    self.save_changes_datepicker()
                if isinstance(self.current_widget, QComboBox):
                    self.save_changes(self.cel_prev_row,self.cel_prev_col)
        self.cel_prev_row = row
        self.cel_prev_col = column
        date_column_index = 11  # replace with the actual index of your date column
        if (column == date_column_index) and ((self.role == "admin" and self.table.item(row,group).text() == self.group) or self.role == "senioradmin") :
            self.table.openPersistentEditor(self.table.item(row, column))
            self.current_widget = self.table.cellWidget(row, column)
            self.par=1
        if (column == rank or column==position) and self.role == "senioradmin":
            combo_box = QComboBox()
            self.prev_combobox_text=self.table.item(row, column).text()
            # Determine possible values based on the column
            if column == rank:
                combo_box.addItems(["сол.", "мол. с-т", "с-т","ст с-т","генерал"])  # Replace with your rank values
                width = combo_box.fontMetrics().boundingRect(max(["сол.", "мол. с-т", "с-т","ст с-т","генерал"], key=len)).width()
                combo_box.view().setFixedWidth(width+12)
            else:  # column == position
                combo_box.addItems(["курсант", "командир","сержант","старшина"])  # Replace with your position values
                combo_box.setMinimumWidth(combo_box.fontMetrics().boundingRect(max(["курсант", "командир","сержант","старшина"], key=len)).width())

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
            item.setIcon(self.icon)
        self.current_widget=None


    def save_changes(self, row, column):
        # Get the selected text from the combobox
        combo_box = self.table.cellWidget(row, column)
        text = combo_box.currentText()

        # Remove the combobox and replace it with the updated text
        self.table.removeCellWidget(row, column)
        self.table.setItem(row, column, QTableWidgetItem(text))
        self.table.item(row, column).setIcon(self.icon)
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
        if self.current_widget:
            if isinstance(self.current_widget, QDateEdit):
                self.save_changes_datepicker()
            if isinstance(self.current_widget, QComboBox):
                self.save_changes(self.cel_prev_row, self.cel_prev_col)
        reply = QMessageBox.question(self.parent, 'Confirmation',
                                     'Are you sure you want to save the changes?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            print(self.query_arr)
            for query in self.query_arr:
                self.db_manager.load_data(query)
            self.load_data_into_table()