from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QApplication, QVBoxLayout, QLabel, QWidget, \
    QComboBox
from PyQt5.QtCore import Qt
import sys
import datetime
from PyQt5.QtCore import QDate

import random


def select_victim(type):
    global result_dict
    selected_candidates = []
    print(type)
    if type in ["chk", "chnk27"]:
        # Выбор сержантов и старшин
        selected_candidates = [(key, data['naryad'], data['group'])
                               for key, data in result_dict.items()
                               if data['position'] in ["сержант", "старшина"]]

    elif type in ["dn1", "dn2", "pchnk271", "pchnk272", "pchnk273"]:
        # Выбор курсантов-мужчин
        selected_candidates = [(key, data['naryad'], data['group'])
                               for key, data in result_dict.items()
                               if data['position'] == "курсант" and data['sex'] == "Чоловік"]

    elif type == "dng":
        # Выбор курсантов-женщин
        selected_candidates = [(key, data['naryad'], data['group'])
                               for key, data in result_dict.items()
                               if data['position'] == "курсант" and data['sex'] == "Жінка"]


    elif type in ["chp1", "chp2", "chp3", "chp4", "chp5", "chp6", "chp7", "chp8", "chp9"]:
        # Выбор курсантов, исключая сержантов и старшин
        selected_candidates = [(key, data['chepe'], data['group'])
                               for key, data in result_dict.items()
                               if data['position'] == "курсант"]

    elif type == "schp":
        # Выбор курсантов-мужчин, исключая женщин
        selected_candidates = [(key, data['chepe'], data['group'])
                               for key, data in result_dict.items()
                               if data['position'] == "курсант" and data['sex'] != "Жінка"]

    # Поиск минимального значения naryad
    if selected_candidates:
        min_naryad = min(selected_candidates, key=lambda x: x[1])[1]
        min_candidates = [(key, group) for key, naryad, group in selected_candidates if naryad == min_naryad]

        # Случайный выбор кандидата с минимальным значением naryad
        selected_candidate = random.choice(min_candidates)

        # Обновление naryad и chepe выбранного кандидата
        if type in ["chp", "schp"]:
            result_dict[selected_candidate[0]]['chepe'] += 1
        else:
            result_dict[selected_candidate[0]]['naryad'] += 1


        return selected_candidate

    return None



def change_schedule_group(selected_group,role,db_manager,change_date):
    query =f"""
    INSERT INTO data_table (date, {role + '_id'}, {role + '_group'})
    VALUES ('{change_date}', NULL, {selected_group})
    ON DUPLICATE KEY UPDATE
    {role + '_id'} = NULL, {role + '_group'} = {selected_group};
    """
    print(query)
    db_manager.execute_script(query)
import datetime

import datetime

def update_schedule_id(curr_id, role, db_manager, change_date):
    sb_exclude_minus = ""
    date_obj = datetime.datetime.strptime(change_date, "%Y-%m-%d")

    if date_obj.weekday() == 5:
        if role != "schp":
            sb_exclude_minus = ", naryad_sb = naryad_sb - 1"
        else:
            sb_exclude_minus = ", chepe_sb = chepe_sb - 1"
    print(role)
    if role in ["pchnk271", "pchnk272", "pchnk273", "chnk27"]:
        place_kurs = "nk"
    elif role in ["dn1", "dn2", "dng", "chk"]:
        place_kurs = "kurs"

    if role != "schp":
        chng_minus = f"{place_kurs} = {place_kurs} - 1, naryad = naryad - 1"
    else:
        chng_minus = "chepe = chepe - 1"

    if curr_id is not None:
        script = f"""
            UPDATE data_table 
            SET {role}_id = NULL, {role}_group = NULL
            WHERE `date` = '{change_date}';
            UPDATE kurs 
            SET {chng_minus}{sb_exclude_minus} 
            WHERE id = {curr_id};
        """
        print(script)
        db_manager.execute_script(script)



def change_schedule_id(curr_id,new_id,role,db_manager,change_date):
    print(role)
    sb_exclude_plus,sb_exclude_minus = "",""
    date_obj = datetime.datetime.strptime(change_date, "%Y-%m-%d")
    print(date_obj.weekday())
    if date_obj.weekday() == 5:

        if role != "schp":
            sb_exclude_plus = ", naryad_sb = naryad_sb + 1"
            sb_exclude_minus = ", naryad_sb = naryad_sb - 1"
        else:
            sb_exclude_plus = ", chepe_sb = chepe_sb + 1"
            sb_exclude_minus = ", chepe_sb = chepe_sb - 1"
        print("Суббота!!!")
    sb_exclude= ""
    print(curr_id,new_id,role,type,db_manager,change_date)
    if role in ["pchnk271","pchnk272","pchnk273","chnk27"]:
        place_kurs="nk"
    elif role in ["dn1","dn2","dng","chk"]:
        place_kurs="kurs"

    if role != "schp":
        chng_plus= f"{place_kurs} = {place_kurs} + 1 ,naryad = naryad + 1";
        chng_minus= f"{place_kurs} = {place_kurs} - 1 ,naryad = naryad - 1";
    else:
        chng_plus =f"chepe = chepe +1"
        chng_minus =f"chepe = chepe -1"
    """
    query = f"UPDATE data_table SET {role+place} = new_id WHERE `date` == change_date"
    query2 = f"UPDATE kurs SET {place_kurs} = {place_kurs} + 1 ,naryad = naryad + 1{sb_exclude_plus} WHERE id = {new_id};"
    query3= f"UPDATE kurs SET {place_kurs} = {place_kurs} -1  ,naryad = naryad - 1{sb_exclude_minus} WHERE id = {curr_id};"
    """
    if curr_id != None:
        if_not_NULL=f"UPDATE kurs SET {chng_minus}{sb_exclude_minus} WHERE id = {curr_id};"
    else:
        if_not_NULL = ""
    script = f"""
        UPDATE data_table SET {role + "_id"} = {new_id} WHERE `date` = '{change_date}';
        UPDATE kurs SET {chng_plus}{sb_exclude_plus} WHERE id = {new_id};
        {if_not_NULL}
        
    """
    print(script)
    #print(place_kurs, place,query3,query2,query)
    db_manager.execute_script(script)
def show_chp_details(details):
    global result_dict
    """
    Функция для отображения окна с людьми из ключа "chp".
    """
    chp_widget = QWidget()
    chp_layout = QVBoxLayout()

    for key, person in details.items():
        name_label = QLabel(f"<a>{result_dict[person['id']]['pib']} (группа {person['group']})</a>")
        name_label.setTextFormat(Qt.RichText)
        name_label.setProperty('id', person['id'])
        name_label.setProperty('group', person['group'])
        name_label.setProperty('name', result_dict[person['id']]['pib'])
        name_label.linkActivated.connect(lambda _, p=person: cell_clicked(None, None, None, None, p))
        chp_layout.addWidget(name_label)

    chp_widget.setLayout(chp_layout)

    msg = QMessageBox()
    msg.setWindowTitle("CHP Details")
    msg.layout().addWidget(chp_widget)
    msg.exec_()


def person_clicked(person):
    global result_dict
    """
    Обрабатывает нажатие на имя человека и выводит его данные.
    """
    msg = QMessageBox()
    msg.setWindowTitle("Person Details")
    msg.setText(f"Name: {person['name']}\nID: {result_dict[person['id']]['pib']}\nGroup: {person['group']}")
    msg.exec_()


def call_fill(schedule_table,db_manager,root,new_date):
    fill_schedule_table(schedule_table,db_manager,root,new_date)

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



def select_ids(result_dict, type):
    names_with_ids = []

    if type in ["chk", "chnk27"]:
        # Select sergeants and warrant officers
        names_with_ids = [key for key, data in result_dict.items()
                          if data['position'] in ["сержант", "старшина"]]

    elif type in ["dn1", "dn2", "pchnk271", "pchnk272", "pchnk273"]:
        # Select male cadets
        names_with_ids = [key for key, data in result_dict.items()
                          if data['position'] == "курсант" and data['sex'] == "Чоловік"]

    elif type == "dng":
        # Select female cadets
        names_with_ids = [key for key, data in result_dict.items()
                          if data['position'] == "курсант" and data['sex'] == "Жінка"]

    elif type == "chp":
        # Select cadets, excluding sergeants and warrant officers
        names_with_ids = [key for key, data in result_dict.items()
                          if data['position'] == "курсант"]

    elif type in ["schp"]:
        # Select male cadets, excluding women
        names_with_ids = [key for key, data in result_dict.items()
                          if data['position'] == "курсант" and data['sex'] != "Жінка"]

    # Group by 'naryad'
    grouped_names_with_ids = {}
    for key in names_with_ids:
        naryad = result_dict[key]['naryad']
        if naryad not in grouped_names_with_ids:
            grouped_names_with_ids[naryad] = []
        grouped_names_with_ids[naryad].append(key)

    return grouped_names_with_ids

def select_names(result_dict, selected_group, type):
    names_with_ids = []

    if type in ["chk", "chnk27"]:
        # Select sergeants and warrant officers
        names_with_ids = [(key, f"{data['pib']} ({data['kurs']}+{data['nk']} = {data['naryad']})")
                          for key, data in result_dict.items()
                          if data['group'] == selected_group and data['position'] in ["сержант", "старшина"]]

    elif type in ["dn1", "dn2","pchnk271", "pchnk272", "pchnk273"]:
        # Select male cadets
        names_with_ids = [(key, f"{data['pib']} ({data['kurs']}+{data['nk']} = {data['naryad']})")
                          for key, data in result_dict.items()
                          if data['group'] == selected_group and data['position'] == "курсант" and data['sex'] == "Чоловік"]

    elif type == "dng":
        # Select female cadets
        names_with_ids = [(key, f"{data['pib']} ({data['kurs']}+{data['nk']} = {data['naryad']})")
                          for key, data in result_dict.items()
                          if data['group'] == selected_group and data['position'] == "курсант" and data['sex'] == "Жінка"]

    elif type == "chp":
        # Select cadets, excluding sergeants and warrant officers
        names_with_ids = [(key, f"{data['pib']} ({data['kurs']}+{data['nk']} = {data['naryad']})")
                          for key, data in result_dict.items()
                          if data['group'] == selected_group and data['position'] == "курсант"]

    elif type in ["schp"]:
        # Select male cadets, excluding women
        names_with_ids = [(key, f"{data['pib']} ({data['kurs']}+{data['nk']} = {data['naryad']})")#tut chp zamenu
                          for key, data in result_dict.items()
                          if data['group'] == selected_group and data['position'] == "курсант" and data['sex'] != "Жінка"]

    return names_with_ids


def get_data(date_list, start_of_week, end_of_week, db_manager):
    rows = db_manager.execute_query(f'''
    SELECT * FROM data_table WHERE date BETWEEN "{start_of_week}" AND "{end_of_week}"
    ''')
    print(rows, start_of_week, end_of_week)

    # Обработка данных и заполнение отсутствующих дат
    empty_structure = {
        "chk": {"group": None, "id": None},
        "dn1": {"group": None, "id": None},
        "dn2": {"group": None, "id": None},
        "dng": {"group": None, "id": None},
        "chnk27": {"group": None, "id": None},
        "pchnk271": {"group": None, "id": None},
        "pchnk272": {"group": None, "id": None},
        "pchnk273": {"group": None, "id": None},
        "schp": {"group": None, "id": None},
        "chp": {
            f"chp{x}": {"group": None, "id": None} for x in range(1, 10)
        }
    }

    # Обработка данных и заполнение отсутствующих дат
    data_dict = {date: empty_structure for date in date_list}

    for row in rows:
        data_dict[row[0]] = {
            "chk": {"group": row[1], "id": row[2]},
            "dn1": {"group": row[3], "id": row[4]},
            "dn2": {"group": row[5], "id": row[6]},
            "dng": {"group": row[7], "id": row[8]},
            "chnk27": {"group": row[9], "id": row[10]},
            "pchnk271": {"group": row[11], "id": row[12]},
            "pchnk272": {"group": row[13], "id": row[14]},
            "pchnk273": {"group": row[15], "id": row[16]},
            "schp": {"group": row[17], "id": row[18]},
            "chp": {
                f"chp{x}": {"group": row[2 * x + 17], "id": row[2 * x + 18]} for x in range(1, 10)
            }
        }

    # Преобразование в формат JSON
    return data_dict


def fill_database(date,db_manager,key):
    print(date,db_manager,key)


import datetime


def iterate_missing_data(data_dict, date_list, db_manager, result_dict, root):
    print(date_list)
    # Define the keys to skip if checkboxes are not checked
    keys_to_skip = ["pchnk271", "pchnk272", "pchnk273", "chnk27", "schp"]  # Removed "chp" as it's now a dictionary

    # Map checkboxes to their indices
    checkbox_mapping = {
        0: root.check_1,
        1: root.check_2,
        2: root.check_3,
        3: root.check_4,
        4: root.check_5,
        5: root.check_6,
        6: root.check_7
    }

    for idx, (date, entries) in enumerate(data_dict.items()):
        # Check if the corresponding checkbox is checked
        if not checkbox_mapping[idx].isChecked():
            # If the checkbox is not checked, skip the specific keys for this date
            entries = {k: v for k, v in entries.items() if k not in keys_to_skip}
            # Also, skip keys inside the 'chp' dictionary
            if 'chp' in entries:
                entries['chp'] = {k: v for k, v in entries['chp'].items() if k not in keys_to_skip}

        # Building the query parts
        columns = ["`date`"]
        values = [f"'{date}'"]
        updates = []
        nk_queries = []

        for role, value in entries.items():
            if isinstance(value, dict) and role != "chp":
                if value["id"] is None:
                    person = select_victim(role)
                    id = person[0]
                    group = person[1]
                    columns.extend([f"{role + '_id'}", f"{role + '_group'}"])
                    values.extend([f"{id}", f"{group}"])
                    updates.extend([f"{role + '_id'} = {id}", f"{role + '_group'} = {group}"])

                    # Add exclusion logic for nk update
                    sb_exclude_plus = ""
                    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
                    if date_obj.weekday() == 5:  # Check if it's Saturday
                        if role != "schp":
                            sb_exclude_plus = ", naryad_sb = naryad_sb + 1"
                        else:
                            sb_exclude_plus = ", chepe_sb = chepe_sb + 1"

                    place_kurs = "nk" if role in ["pchnk271", "pchnk272", "pchnk273", "chnk27"] else "kurs"
                    chng_plus = f"{place_kurs} = {place_kurs} + 1 ,naryad = naryad + 1" if role not in ["schp","chp1", "chp2", "chp3", "chp4", "chp5", "chp6", "chp7", "chp8", "chp9"] else "chepe = chepe + 1"
                    nk_queries.append(f"UPDATE kurs SET {chng_plus}{sb_exclude_plus} WHERE `id` = '{id}'")

            elif isinstance(value, dict) and role == "chp":
                for sub_role, sub_value in value.items():
                    if sub_value["id"] is None:
                        person = select_victim(sub_role)
                        id = person[0]
                        group = person[1]
                        columns.extend([f"{sub_role + '_id'}", f"{sub_role + '_group'}"])
                        values.extend([f"{id}", f"{group}"])
                        updates.extend([f"{sub_role + '_id'} = {id}", f"{sub_role + '_group'} = {group}"])

                        # Add exclusion logic for nk update
                        sb_exclude_plus = ""
                        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
                        if date_obj.weekday() == 5:  # Check if it's Saturday
                            if sub_role != "schp":
                                sb_exclude_plus = ", naryad_sb = naryad_sb + 1"
                            else:
                                sb_exclude_plus = ", chepe_sb = chepe_sb + 1"

                        place_kurs = "nk" if sub_role in ["pchnk271", "pchnk272", "pchnk273", "chnk27"] else "kurs"
                        chng_plus = f"{place_kurs} = {place_kurs} + 1 ,naryad = naryad + 1" if sub_role not in ["schp","chp1", "chp2", "chp3", "chp4", "chp5", "chp6", "chp7", "chp8", "chp9"] else "chepe = chepe + 1"
                        nk_queries.append(f"UPDATE kurs SET {chng_plus}{sb_exclude_plus} WHERE `id` = '{id}'")

        # Construct the final query
        insert_query = f"INSERT INTO data_table ({', '.join(columns)}) VALUES ({', '.join(values)})"
        update_query = f"ON DUPLICATE KEY UPDATE {', '.join(updates)}"

        query = f"{insert_query} {update_query};"

        print(query)
        db_manager.execute_script(query)

        # Execute nk update queries
        for nk_query in nk_queries:
            print(nk_query)
            db_manager.execute_script(nk_query)


def fill_schedule_table(schedule_table: QTableWidget, db_manager, root, cur_date):
    """
    Заполняет таблицу schedule_table данными из массива arr с включением групп.

    :param schedule_table: QTableWidget, таблица для заполнения
    :param db_manager: объект для управления базой данных
    :param root: объект корневого интерфейса
    :param cur_date: текущая дата
    """
    if not cur_date:
        cur_date = db_manager.get_cur_date()

    week_dates, start_of_week, end_of_week = get_week_boundaries(cur_date)
    start_view = start_of_week.strftime('%m.%d')
    end_view = end_of_week.strftime('%m.%d')

    try:
        root.schedule_button_l.clicked.disconnect()
        root.schedule_button_r.clicked.disconnect()
        root.calculate_schedule.clicked.disconnect()
    except TypeError:
        pass

    arr = get_data(week_dates, start_of_week, end_of_week, db_manager)
    schedule_table.setHorizontalHeaderLabels(week_dates)

    # Выполните запрос и получите результаты
    results = db_manager.execute_query(
        "SELECT id, pib, `group`, naryad, kurs, nk, sex, `position`, chepe FROM kurs ORDER BY naryad")
    global result_dict

    # Преобразуйте результаты в словарь
    result_dict = {
        row[0]: {
            'pib': row[1],
            'group': row[2],
            'naryad': row[3],
            'kurs': row[4],
            'nk': row[5],
            'sex': row[6],
            'position': row[7],
            'chepe': row[8]
        }
        for row in results
    }

    root.schedule_date_l.setText(f"{start_view}-{end_view}")



    # Reconnect the signals to the slots
    root.schedule_button_l.clicked.connect(
        lambda: call_fill(schedule_table, db_manager, root, start_of_week - datetime.timedelta(days=1)))
    root.schedule_button_r.clicked.connect(
        lambda: call_fill(schedule_table, db_manager, root, end_of_week + datetime.timedelta(days=1)))
    root.calculate_schedule.clicked.connect(
        lambda: iterate_missing_data(arr, week_dates, db_manager, result_dict, root))

    # Вывод результата для проверки
    # for key, value in result_dict.items():
    #     print(f"id: {key}, data: {value}")

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
                    item.setData(Qt.UserRole + 4, roles.get("chp", {}))  # Store CHP details for later use
                schedule_table.setItem(row, col, item)
            row += 1
        col += 1


def render_cell_text(value, role):
    global result_dict
    """
    Renders the cell text based on the data.
    """
    if role == "cp" and isinstance(value, list):
        return ", ".join(f"{person['name']} (группа {person['group']})" for person in value)
    elif isinstance(value, dict):
        if value['group']==None:
            return f""
        elif value['id']==None:
            return f"(группа {value['group']})"
        else:
            return f"{result_dict[value['id']]['pib']} (группа {value['group']})"
    else:
        return str(value)


def cell_clicked(row, col, schedule_table, db_manager,root, person=None):

    """
    Обрабатывает нажатие на ячейку таблицы и выводит данные ячейки.
    """
    column_name = schedule_table.horizontalHeaderItem(col).text()
    if person:
        person_id = person['id']
        person_group = person['group']
        person_type = 'chp'
    else:
        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers == Qt.ControlModifier
        alt_pressed = modifiers == Qt.AltModifier
        shift_pressed = modifiers == Qt.ShiftModifier

        item = schedule_table.item(row, col)
        print(root.role_data["group"],str(item.data(Qt.UserRole + 2)),root.role_data["role"],"senioradmin")
        print(root.role_data["group"] != str(item.data(Qt.UserRole + 2)))
        x=0
        if root.role_data["group"]== str(item.data(Qt.UserRole + 2)) :
            x=1
        if root.role_data["role"] == "senioradmin":
            x=1
        if x != 1:
            return
        if not item:
            return

        person_id = item.data(Qt.UserRole + 1)
        person_group = item.data(Qt.UserRole + 2)
        type_n = item.data(Qt.UserRole + 3)

        # Place the column name into the 5th data slot
        item.setData(Qt.UserRole + 5, column_name)

        if ctrl_pressed:
            handle_ctrl_click(row, col, schedule_table, person_group, db_manager)
            return
        elif alt_pressed and person_group is not None:
            handle_alt_click(row, col, schedule_table, person_group, db_manager)
            return
        elif shift_pressed:
            delete_data(row, col, schedule_table, db_manager)
            return
        elif type_n == "schp":
            chp_details = item.data(Qt.UserRole + 4)
            show_chp_details(chp_details)
            return


def delete_data(row, col, schedule_table, db_manager):
    """
    Удаляет данные в указанной ячейке таблицы и обновляет базу данных.
    """
    item = schedule_table.item(row, col)
    if item:
        person_id = item.data(Qt.UserRole + 1)
        role = item.data(Qt.UserRole + 3)
        column_name = schedule_table.horizontalHeaderItem(col).text()
        update_schedule_id(person_id,role,db_manager,column_name)
        # Удаление данных из базы данных
        #db_manager.delete_data(person_id, column_name)

        # Очистка данных ячейки
        item.setData(Qt.UserRole + 1, None)
        item.setData(Qt.UserRole + 2, None)
        item.setData(Qt.UserRole + 3, None)
        item.setData(Qt.UserRole + 4, None)
        item.setData(Qt.UserRole + 5, None)
        item.setText("")


def handle_ctrl_click(row, col, schedule_table, current_group,db_manager):
    """
    Handles the Ctrl click event to display a combo box for group selection.
    """
    combo_box = QComboBox()
    groups = ["Группа 11", "Группа 12", "Группа 13", "Группа 14", "Группа 15"]
    combo_box.addItems(groups)

    combo_box.setCurrentIndex(current_group - 1 if current_group else 0)
    schedule_table.setCellWidget(row, col, combo_box)

    def on_group_selected(index,db_manager):
        selected_group = combo_box.currentIndex() + 11
        schedule_table.removeCellWidget(row, col)
        item = schedule_table.item(row, col)
        item.setData(Qt.UserRole + 2, selected_group)
        item.setData(Qt.UserRole + 1, None)  # Clear ID

        role = item.data(Qt.UserRole + 3)
        change_date = item.data(Qt.UserRole + 5)
        change_schedule_group(selected_group,role, db_manager, change_date)

        item.setText(render_cell_text({"group": selected_group,"id":None}, item.data(Qt.UserRole + 3)))

    combo_box.activated.connect(lambda index: on_group_selected(index, db_manager))


def handle_alt_click(row, col, schedule_table, selected_group,db_manager):
    """
    Handles the Alt click event to display a combo box for name selection.
    """
    global result_dict
    # Получаем текущую группу из ячейки
    item = schedule_table.item(row, col)
    curr_id = item.data(Qt.UserRole + 1)
    selected_group = item.data(Qt.UserRole + 2)

    # Фильтруем людей по текущей группе
    ids = select_ids(result_dict, item.data(Qt.UserRole + 3))
    print(ids)
    names_with_ids = select_names(result_dict, selected_group, item.data(Qt.UserRole + 3))

    # Создаем и заполняем комбо-бокс
    combo_box = QComboBox()
    for id_, name in names_with_ids:
        combo_box.addItem(name, id_)
    combo_box.view().setMinimumSize(175, 150)  # ширина, высота

    # Устанавливаем комбо-бокс в ячейку
    schedule_table.setCellWidget(row, col, combo_box)

    def on_name_selected(index,db,id):
        selected_id = combo_box.currentData()
        selected_name = combo_box.currentText()
        print(id,selected_id)
        ###СЮДА print(db)


        schedule_table.removeCellWidget(row, col)
        item = schedule_table.item(row, col)

        role= item.data(Qt.UserRole + 3)
        change_date = item.data(Qt.UserRole + 5)
        change_schedule_id(id,selected_id,role,db_manager,change_date)

        item.setData(Qt.UserRole + 1, selected_id)
        item.setText(render_cell_text({"id": selected_id, "group": selected_group}, item.data(Qt.UserRole + 3)))
    combo_box.activated.connect(lambda index: on_name_selected(index, db_manager,curr_id))




if __name__ == "__main__":
    app = QApplication(sys.argv)
    table_widget = QTableWidget()
    fill_schedule_table(table_widget)
    table_widget.show()
    sys.exit(app.exec_())
