from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QApplication
import sys

def show_chp_details(details):
    """
    Функция для отображения окна с людьми из ключа "chp".
    """
    formatted_details = "\n".join([f"{person['name']} (группа {person['group']})" for person in details])
    msg = QMessageBox()
    msg.setWindowTitle("CHP Details")
    msg.setText(formatted_details)
    msg.exec_()


def fill_schedule_table(schedule_table: QTableWidget, arr: dict):
    """
    Заполняет таблицу schedule_table данными из массива arr с включением групп.

    :param schedule_table: QTableWidget, таблица для заполнения
    :param arr: dict, массив с данными
    """
    schedule_table.setRowCount(9)  # CK, dn1, dn2, dng, chnk27, pchnk271, pchnk272, pchnk273, schp, cp
    schedule_table.setColumnCount(len(arr))

    # Вставка данных в таблицу
    col = 0
    for date, roles in arr.items():
        row = 0
        for role, value in roles.items():
            if role == "chp":
                continue  # Пропуск ключа "chp"
            if role == "cp" and isinstance(value, list):
                # Преобразование списка фамилий в строку с указанием групп
                value = ", ".join(f"{person['name']} (группа {person['group']})" for person in value)
            else:
                value = f"{value['name']} (группа {value['group']})" if isinstance(value, dict) else value

            if role == "schp":
                button = QPushButton(value)
                button.setStyleSheet(
                    "background-color: none; border: none; padding: 0; margin: 0;")  # Отключение стилей
                button.clicked.connect(lambda _, chp_details=roles.get("chp", []): show_chp_details(chp_details))
                schedule_table.setCellWidget(row, col, button)
            else:
                item = QTableWidgetItem(value)
                schedule_table.setItem(row, col, item)
            row += 1
        col += 1
arr = {
    "27_05_2024": {
        "chk": {"name": "Мишеніна А. І.", "group": 1},
        "dn1": {"name": "Медуниця П. Ю.", "group": 2},
        "dn2": {"name": "Кудленок А. В.", "group": 3},
        "dng": {"name": "Кісельов Д. В.", "group": 4},
        "chnk27": {"name": "Каменев М. С.", "group": 1},
        "pchnk271": {"name": "Зозулюк М. О.", "group": 2},
        "pchnk272": {"name": "Гурський М. М.", "group": 3},
        "pchnk273": {"name": "Геращенко Т. М.", "group": 4},
        "schp": {"name": "Буряк К. С.", "group": 5},
        "chp": [
            {"name": "Щербатюк М. О.", "group": 1},
            {"name": "Андрощук Є. С.", "group": 2},
            {"name": "Бакай Р. Р.", "group": 3},
            {"name": "Юзвенко Є. О.", "group": 4},
            {"name": "Бойчук О. В.", "group": 5},
            {"name": "Братко Д. В.", "group": 1},
            {"name": "Дергаусов О. С.", "group": 2},
            {"name": "Дергачов С. О.", "group": 3},
            {"name": "Заставнюк В. В.", "group": 4}
        ]
    },
    "28_05_2024": {
        "chk": {"name": "Буряк К. С.", "group": 1},
        "dn1": {"name": "Безнос О. С.", "group": 2},
        "dn2": {"name": "Щербатюк М. О.", "group": 3},
        "dng": {"name": "Андрощук Є. С.", "group": 4}
    },
    "29_05_2024": {
        "chk": {"name": "Бакай Р. Р.", "group": 1},
        "dn1": {"name": "Юзвенко Є. О.", "group": 2},
        "dn2": {"name": "Бойчук О. В.", "group": 3},
        "dng": {"name": "Братко Д. В.", "group": 4},
        "chnk27": {"name": "Дергаусов О. С.", "group": 1},
        "pchnk271": {"name": "Дергачов С. О.", "group": 2},
        "pchnk272": {"name": "Заставнюк В. В.", "group": 3},
        "pchnk273": {"name": "Здунюк К. О.", "group": 4},
        "schp": {"name": "Зубков І. О.", "group": 5},
        "chp": [
            {"name": "Йосипчук О. В.", "group": 1},
            {"name": "Кириченко Б. В.", "group": 2},
            {"name": "Книш П. М.", "group": 3},
            {"name": "Кошмяков А. Д.", "group": 4},
            {"name": "Крутько Д. М.", "group": 5},
            {"name": "Кукало Д. В.", "group": 1},
            {"name": "Мануйленко М. Г.", "group": 2},
            {"name": "Мельник І. В.", "group": 3},
            {"name": "Мороз І. О.", "group": 4}
        ]
    },
    "30_05_2024": {
        "chk": {"name": "Найдьон М. А.", "group": 1},
        "dn1": {"name": "Петрашевський Н. С.", "group": 2},
        "dn2": {"name": "Сивенко Є. О.", "group": 3},
        "dng": {"name": "Струтинська А. О.", "group": 4}
    },
    "31_05_2024": {
        "chk": {"name": "Шевченко Ю. С.", "group": 1},
        "dn1": {"name": "Бузак З. Т.", "group": 2},
        "dn2": {"name": "Венцківський С. В.", "group": 3},
        "dng": {"name": "Гапоненко Є. О.", "group": 4},
        "chnk27": {"name": "Гашинський В. В.", "group": 1},
        "pchnk271": {"name": "Гетманська А. В.", "group": 2},
        "pchnk272": {"name": "Данканич Д. Р.", "group": 3},
        "pchnk273": {"name": "Йовенко А. П.", "group": 4},
        "schp": {"name": "Карпенко А. О.", "group": 5},
        "chp": [
            {"name": "Козубенко О. С.", "group": 1},
            {"name": "Комендант С. Ю.", "group": 2},
            {"name": "Корж Я. А.", "group": 3},
            {"name": "Лужецька А. В.", "group": 4},
            {"name": "Максименко К. Р.", "group": 5},
            {"name": "Мартинюк В. О.", "group": 1},
            {"name": "Медвецька А. Ю.", "group": 2},
            {"name": "Мірошніченко М. В.", "group": 3},
            {"name": "Мялькіна А. Р.", "group": 4}
        ]
    },
    "01_06_2024": {
        "chk": {"name": "Науменко А. В.", "group": 1},
        "dn1": {"name": "Олейников В. Д.", "group": 2},
        "dn2": {"name": "Руденок В. С.", "group": 3},
        "dng": {"name": "Смага С. О.", "group": 4}
    },
    "02_06_2024": {
        "chk": {"name": "Срібний Р. Р.", "group": 1},
        "dn1": {"name": "Толок К. А.", "group": 2},
        "dn2": {"name": "Черниш В. О.", "group": 3},
        "dng": {"name": "Щербаченко Д. Ю.", "group": 4},
        "chnk27": {"name": "Юзвенко К. Р.", "group": 1},
        "pchnk271": {"name": "Белеля А. М.", "group": 2},
        "pchnk272": {"name": "Ботвинко К. Ю.", "group": 3},
        "pchnk273": {"name": "Букатар І. Д.", "group": 4},
        "schp": {"name": "Волошин Д. В.", "group": 5},
        "chp": [
            {"name": "Геращенко А. О.", "group": 1},
            {"name": "Гімарі А. А.", "group": 2},
            {"name": "Денчик І. В.", "group": 3},
            {"name": "Ємяшев Д. В.", "group": 4},
            {"name": "Заровний Є. А.", "group": 5},
            {"name": "Клевко А. П.", "group": 1},
            {"name": "Кортилісець Д. І.", "group": 2},
            {"name": "Костюкевич О. Р.", "group": 3},
            {"name": "Литвиненко В. О.", "group": 4}
        ]
    }
}
if __name__ == "__main__":
    app = QApplication(sys.argv)
    table_widget = QTableWidget()
    fill_schedule_table(table_widget, arr)
    table_widget.show()
    sys.exit(app.exec_())
