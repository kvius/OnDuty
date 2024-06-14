import unittest
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QComboBox, QPushButton, QTableWidget
from src.utils.datedelegate import DateDelegate
from src.utils.database import DatabaseManager
from src.main import StatsManager


class TestStatsManager(unittest.TestCase):
    def setUp(self):
        self.combogroup = QComboBox()
        self.comboposition = QComboBox()
        self.combosex = QComboBox()
        self.stats_submit = QPushButton()
        self.db_manager = DatabaseManager()
        self.table = QTableWidget()
        self.parent = None
        self.role_data = {"role": "admin", "group": "A"}

        self.stats_manager = StatsManager(self.combogroup, self.comboposition, self.combosex, self.stats_submit,
                                          self.db_manager, self.table, self.parent, self.role_data)

    def test_load_data_into_table(self):
        # Mock the db_manager.execute_query method
        self.db_manager.execute_query = MagicMock(return_value=[(1, 'A', 'Курсант', 'Чоловіча', '2024-01-01')])

        # Mock the QComboBox currentText method
        self.combogroup.currentText = MagicMock(return_value="Група")
        self.comboposition.currentText = MagicMock(return_value="Курсанти")
        self.combosex.currentText = MagicMock(return_value="Стать")

        self.stats_manager.load_data_into_table()

        # Check that execute_query was called with the correct query
        self.db_manager.execute_query.assert_called_with("SELECT * FROM kurs WHERE `position` = 'Курсант' ORDER BY id")

        # Check that the table has the correct number of rows
        self.assertEqual(self.table.rowCount(), 1)

        # Check that the table contains the correct data
        self.assertEqual(self.table.item(0, 0).text(), '1')
        self.assertEqual(self.table.item(0, 1).text(), 'A')
        self.assertEqual(self.table.item(0, 2).text(), 'Курсант')
        self.assertEqual(self.table.item(0, 3).text(), 'Чоловіча')
        self.assertEqual(self.table.item(0, 4).text(), '2024-01-01')

    def test_save_changes_datepicker(self):
        # Mock the QDateEdit widget
        self.stats_manager.current_widget = MagicMock()
        self.stats_manager.current_widget.date.return_value = QDate(2024, 1, 1)
        self.table.model().index = MagicMock()
        self.table.indexWidget = MagicMock()
        self.table.indexWidget.return_value = self.stats_manager.current_widget

        self.stats_manager.save_changes_datepicker()

        # Check that the date was correctly saved
        self.assertEqual(self.table.item(self.stats_manager.cel_prev_row, self.stats_manager.cel_prev_col).text(),
                         '2024-01-01')

    def test_save_changes(self):
        # Mock the QComboBox widget
        combo_box = QComboBox()
        combo_box.addItems(["сол.", "мол. с-т", "с-т", "ст с-т", "генерал"])
        combo_box.setCurrentText("сол.")
        self.table.setCellWidget(0, 1, combo_box)

        self.stats_manager.cel_prev_row = 0
        self.stats_manager.cel_prev_col = 1
        self.stats_manager.current_widget = combo_box

        self.stats_manager.save_changes(0, 1)

        # Check that the text was correctly saved
        self.assertEqual(self.table.item(0, 1).text(), 'сол.')

    def test_submit(self):
        # Mock the QMessageBox
        QMessageBox.question = MagicMock(return_value=QMessageBox.Yes)

        # Add a query to the query_arr
        self.stats_manager.query_arr.append("UPDATE kurs SET `position` = 'Курсант' WHERE `id` = '1';")

        # Mock the db_manager.load_data method
        self.db_manager.load_data = MagicMock()

        self.stats_manager.submit()

        # Check that the load_data method was called with the correct query
        self.db_manager.load_data.assert_called_with("UPDATE kurs SET `position` = 'Курсант' WHERE `id` = '1';")


if __name__ == '__main__':
    unittest.main()
