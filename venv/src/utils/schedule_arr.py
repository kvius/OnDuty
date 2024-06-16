from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QApplication, QVBoxLayout, QLabel, QWidget, \
    QComboBox
from PyQt5.QtCore import Qt
import sys
import datetime
from PyQt5.QtCore import QDate
def show_chp_details(details):
    """
    Функция для отображения окна с людьми из ключа "chp".
    """
    chp_widget = QWidget()
    chp_layout = QVBoxLayout()

    for person in details:
        name_label = QLabel(f"<a>{person['name']} (группа {person['group']})</a>")

        name_label.setTextFormat(Qt.RichText)
        name_label.setProperty('id', person['id'])
        name_label.setProperty('group', person['group'])
        name_label.setProperty('name', person['name'])
        name_label.linkActivated.connect(lambda _, p=person: cell_clicked(None, None, None, p))
        chp_layout.addWidget(name_label)

    chp_widget.setLayout(chp_layout)

    msg = QMessageBox()
    msg.setWindowTitle("CHP Details")
    msg.layout().addWidget(chp_widget)
    msg.exec_()


def person_clicked(person):
    """
    Обрабатывает нажатие на имя человека и выводит его данные.
    """
    msg = QMessageBox()
    msg.setWindowTitle("Person Details")
    msg.setText(f"Name: {person['name']}\nID: {person['id']}\nGroup: {person['group']}")
    msg.exec_()




def get_week_boundaries(date):
    # Перевірка, чи введена дата є об'єктом datetime
    if not isinstance(date, datetime.date):
        raise ValueError("Введена дата повинна бути об'єктом datetime.date")

    # Визначення першого дня тижня (понеділка)
    start_of_week = date - datetime.timedelta(days=date.weekday())
    # Визначення останнього дня тижня (неділі)
    end_of_week = start_of_week + datetime.timedelta(days=6)

    # Створення масиву з усіма датами між початком і кінцем тижня
    week_dates = [(start_of_week + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    return week_dates,start_of_week,end_of_week


# Приклад використання функції
date = datetime.date(2024, 6, 16)
week_dates = get_week_boundaries(date)
print(week_dates)




def fill_schedule_table(schedule_table: QTableWidget, arr: dict,db_manager):
    """
    Заполняет таблицу schedule_table данными из массива arr с включением групп.

    :param schedule_table: QTableWidget, таблица для заполнения
    :param arr: dict, массив с данными

    """

    cur_date=db_manager.get_cur_date()
    print(cur_date)
    week_dates, start_of_week, end_of_week =get_week_boundaries(cur_date)
    print(f"Початок тижня: {start_of_week}")
    print(f"Кінець тижня: {end_of_week}")
    schedule_table.setHorizontalHeaderLabels(week_dates)
    # Выполните запрос и получите результаты
    results = db_manager.execute_query("SELECT id, pib, `group`, naryad, kurs, nk FROM kurs ORDER BY naryad")
    global result_dict
    # Преобразуйте результаты в словарь
    result_dict = {
        row[0]: {
            'pib': row[1],
            'group': row[2],
            'naryad': row[3],
            'kurs': row[4],
            'nk': row[5]
        }
        for row in results
    }

    # Вывод результата для проверки
    for key, value in result_dict.items():
        print(f"id: {key}, data: {value}")

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
                value_str = ", ".join(f"{person['name']} (группа {person['group']})" for person in value)
                item = QTableWidgetItem(value_str)
                item.setData(Qt.UserRole + 1, [person['id'] for person in value])
                item.setData(Qt.UserRole + 2, [person['group'] for person in value])
                item.setData(Qt.UserRole + 3, role)
                schedule_table.setItem(row, col, item)
            else:
                value_str = render_cell_text(value, role)
                item = QTableWidgetItem(value_str)
                if isinstance(value, dict):
                    item.setData(Qt.UserRole + 1, value['id'])
                    item.setData(Qt.UserRole + 2, value['group'])
                item.setData(Qt.UserRole + 3, role)
                if role == "schp":
                    item.setData(Qt.UserRole + 4, roles.get("chp", []))  # Store CHP details for later use
                schedule_table.setItem(row, col, item)
            row += 1
        col += 1


def render_cell_text(value, role):
    """
    Renders the cell text based on the data.
    """
    if role == "cp" and isinstance(value, list):
        return ", ".join(f"{person['name']} (группа {person['group']})" for person in value)
    elif isinstance(value, dict):
        return f"{value['name']} (группа {value['group']})"
    else:
        return str(value)


def cell_clicked(row, col, schedule_table, person=None):
    """
    Обрабатывает нажатие на ячейку таблицы и выводит данные ячейки.
    """
    if person:
        person_id = person['id']
        person_group = person['group']
        person_type = 'chp'
    else:
        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers == Qt.ControlModifier
        alt_pressed = modifiers == Qt.AltModifier

        item = schedule_table.item(row, col)
        if not item:
            return

        person_id = item.data(Qt.UserRole + 1)
        person_group = item.data(Qt.UserRole + 2)
        person_type = item.data(Qt.UserRole + 3)

        if ctrl_pressed:
            handle_ctrl_click(row, col, schedule_table, person_group)
            return
        elif alt_pressed:
            handle_alt_click(row, col, schedule_table, person_group)
            return
        elif person_type == "schp":
            chp_details = item.data(Qt.UserRole + 4)
            show_chp_details(chp_details)
            return

    msg = QMessageBox()
    msg.setWindowTitle("Cell Details")
    msg.setText(f"ID: {person_id}\nGroup: {person_group}\nType: {person_type}")
    msg.exec_()


def handle_ctrl_click(row, col, schedule_table, current_group):
    """
    Handles the Ctrl click event to display a combo box for group selection.
    """
    combo_box = QComboBox()
    groups = ["Группа 11", "Группа 12", "Группа 13", "Группа 14", "Группа 15"]
    combo_box.addItems(groups)

    combo_box.setCurrentIndex(current_group - 1 if current_group else 0)
    schedule_table.setCellWidget(row, col, combo_box)

    def on_group_selected():
        selected_group = combo_box.currentIndex() + 11
        schedule_table.removeCellWidget(row, col)
        item = schedule_table.item(row, col)
        item.setData(Qt.UserRole + 2, selected_group)
        item.setData(Qt.UserRole + 1, None)  # Clear ID
        item.setText(render_cell_text({"group": selected_group,"name":""}, item.data(Qt.UserRole + 3)))

    combo_box.activated.connect(on_group_selected)


def handle_alt_click(row, col, schedule_table, current_group):
    """
    Handles the Alt click event to display a combo box for name selection.
    #4682B4
    #3B699E;
    """
    global result_dict
    # Получаем текущую группу из ячейки
    item = schedule_table.item(row, col)
    selected_group = item.data(Qt.UserRole + 2)

    # Фильтруем людей по текущей группе
    names = [f"{data['pib']} ({data['kurs']}+{data['nk']} = {data['naryad']})" for data in result_dict.values() if data['group'] == selected_group]

    # Создаем и заполняем комбо-бокс
    combo_box = QComboBox()
    combo_box.addItems(names)
    combo_box.view().setMinimumSize(200, 250)  # ширина, высота
    # Устанавливаем комбо-бокс в ячейку
    schedule_table.setCellWidget(row, col, combo_box)

    def on_name_selected():
        selected_name = combo_box.currentText()
        schedule_table.removeCellWidget(row, col)
        item = schedule_table.item(row, col)
        item.setData(Qt.UserRole + 1, selected_name)  # Assuming the name is being set as the ID temporarily
        item.setText(render_cell_text({"name": selected_name, "group": current_group}, item.data(Qt.UserRole + 3)))

    combo_box.activated.connect(on_name_selected)



arr = {
    "27_05_2024": {
        "chk": {"name": "Мишеніна А. І.", "group": 11, "id": 1},
        "dn1": {"name": "Медуниця П. Ю.", "group": 12, "id": 2},
        "dn2": {"name": "Кудленок А. В.", "group": 13, "id": 3},
        "dng": {"name": "Кісельов Д. В.", "group": 14, "id": 4},
        "chnk27": {"name": "Каменев М. С.", "group": 11, "id": 5},
        "pchnk271": {"name": "Зозулюк М. О.", "group": 12, "id": 6},
        "pchnk272": {"name": "Гурський М. М.", "group": 13, "id": 7},
        "pchnk273": {"name": "Геращенко Т. М.", "group": 14, "id": 8},
        "schp": {"name": "Буряк К. С.", "group": 15, "id": 9},
        "chp": [
            {"name": "Щербатюк М. О.", "group": 11, "id": 10},
            {"name": "Андрощук Є. С.", "group": 12, "id": 11},
            {"name": "Бакай Р. Р.", "group": 13, "id": 12},
            {"name": "Юзвенко Є. О.", "group": 14, "id": 13},
            {"name": "Бойчук О. В.", "group": 15, "id": 14},
            {"name": "Братко Д. В.", "group": 11, "id": 15},
            {"name": "Дергаусов О. С.", "group": 12, "id": 16},
            {"name": "Дергачов С. О.", "group": 13, "id": 17},
            {"name": "Заставнюк В. В.", "group": 14, "id": 18}
        ]
    },
    "28_05_2024": {
        "chk": {"name": "Буряк К. С.", "group": 11, "id": 19},
        "dn1": {"name": "Безнос О. С.", "group": 12, "id": 20},
        "dn2": {"name": "Щербатюк М. О.", "group": 13, "id": 21},
        "dng": {"name": "Андрощук Є. С.", "group": 14, "id": 22}
    },
    "29_05_2024": {
        "chk": {"name": "Бакай Р. Р.", "group": 11, "id": 23},
        "dn1": {"name": "Юзвенко Є. О.", "group": 12, "id": 24},
        "dn2": {"name": "Бойчук О. В.", "group": 13, "id": 25},
        "dng": {"name": "Братко Д. В.", "group": 14, "id": 26},
        "chnk27": {"name": "Дергаусов О. С.", "group": 11, "id": 27},
        "pchnk271": {"name": "Дергачов С. О.", "group": 12, "id": 28},
        "pchnk272": {"name": "Заставнюк В. В.", "group": 13, "id": 29},
        "pchnk273": {"name": "Здунюк К. О.", "group": 14, "id": 30},
        "schp": {"name": "Зубков І. О.", "group": 15, "id": 31},
        "chp": [
            {"name": "Йосипчук О. В.", "group": 11, "id": 32},
            {"name": "Кириченко Б. В.", "group": 12, "id": 33},
            {"name": "Книш П. М.", "group": 13, "id": 34},
            {"name": "Кошмяков А. Д.", "group": 14, "id": 35},
            {"name": "Крутько Д. М.", "group": 15, "id": 36},
            {"name": "Кукало Д. В.", "group": 11, "id": 37},
            {"name": "Мануйленко М. Г.", "group": 12, "id": 38},
            {"name": "Мельник І. В.", "group": 13, "id": 39},
            {"name": "Мороз І. О.", "group": 14, "id": 40}
        ]
    },
    "30_05_2024": {
        "chk": {"name": "Найдьон М. А.", "group": 11, "id": 41},
        "dn1": {"name": "Петрашевський Н. С.", "group": 12, "id": 42},
        "dn2": {"name": "Сивенко Є. О.", "group": 13, "id": 43},
        "dng": {"name": "Струтинська А. О.", "group": 14, "id": 44}
    },
    "31_05_2024": {
        "chk": {"name": "Шевченко Ю. С.", "group": 11, "id": 45},
        "dn1": {"name": "Бузак З. Т.", "group": 12, "id": 46},
        "dn2": {"name": "Венцківський С. В.", "group": 13, "id": 47},
        "dng": {"name": "Гапоненко Є. О.", "group": 14, "id": 48},
        "chnk27": {"name": "Гашинський В. В.", "group": 11, "id": 49},
        "pchnk271": {"name": "Гетманська А. В.", "group": 12, "id": 50},
        "pchnk272": {"name": "Данканич Д. Р.", "group": 13, "id": 51},
        "pchnk273": {"name": "Йовенко А. П.", "group": 14, "id": 52},
        "schp": {"name": "Карпенко А. О.", "group": 15, "id": 53},
        "chp": [
            {"name": "Козубенко О. С.", "group": 11, "id": 54},
            {"name": "Комендант С. Ю.", "group": 12, "id": 55},
            {"name": "Корж Я. А.", "group": 13, "id": 56},
            {"name": "Лужецька А. В.", "group": 14, "id": 57},
            {"name": "Максименко К. Р.", "group": 15, "id": 58},
            {"name": "Мартинюк В. О.", "group": 11, "id": 59},
            {"name": "Медвецька А. Ю.", "group": 12, "id": 60},
            {"name": "Мірошніченко М. В.", "group": 13, "id": 61},
            {"name": "Мялькіна А. Р.", "group": 14, "id": 62}
        ]
    },
    "01_06_2024": {
        "chk": {"name": "Науменко А. В.", "group": 11, "id": 63},
        "dn1": {"name": "Олейников В. Д.", "group": 12, "id": 64},
        "dn2": {"name": "Руденок В. С.", "group": 13, "id": 65},
        "dng": {"name": "Смага С. О.", "group": 14, "id": 66}
    },
    "02_06_2024": {
        "chk": {"name": "Срібний Р. Р.", "group": 11, "id": 67},
        "dn1": {"name": "Толок К. А.", "group": 12, "id": 68},
        "dn2": {"name": "Черниш В. О.", "group": 13, "id": 69},
        "dng": {"name": "Щербаченко Д. Ю.", "group": 14, "id": 70},
        "chnk27": {"name": "Юзвенко К. Р.", "group": 11, "id": 71},
        "pchnk271": {"name": "Белеля А. М.", "group": 12, "id": 72},
        "pchnk272": {"name": "Ботвинко К. Ю.", "group": 13, "id": 73},
        "pchnk273": {"name": "Букатар І. Д.", "group": 14, "id": 74},
        "schp": {"name": "Волошин Д. В.", "group": 15, "id": 75},
        "chp": [
            {"name": "Геращенко А. О.", "group": 11, "id": 76},
            {"name": "Гімарі А. А.", "group": 12, "id": 77},
            {"name": "Денчик І. В.", "group": 13, "id": 78},
            {"name": "Ємяшев Д. В.", "group": 14, "id": 79},
            {"name": "Заровний Є. А.", "group": 15, "id": 80},
            {"name": "Клевко А. П.", "group": 11, "id": 81},
            {"name": "Кортилісець Д. І.", "group": 12, "id": 82},
            {"name": "Костюкевич О. Р.", "group": 13, "id": 83},
            {"name": "Литвиненко В. О.", "group": 14, "id": 84}
        ]
    }
}
if __name__ == "__main__":
    app = QApplication(sys.argv)
    table_widget = QTableWidget()
    fill_schedule_table(table_widget, arr)
    table_widget.show()
    sys.exit(app.exec_())
