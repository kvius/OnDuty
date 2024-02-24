from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDateEdit, QItemDelegate


class DateDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QDateEdit(parent)
        editor.setCalendarPopup(True)
        editor.setDisplayFormat('yyyy-MM-dd')
        self.noDate = QDate().currentDate()
        print(self.noDate)
        editor.setDate(QDate().currentDate())
        return editor