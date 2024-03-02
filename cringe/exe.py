import mysql.connector
from datetime import datetime, timedelta
import pprint


class NaryadScheduler:
    def __init__(self, data_sources, scheme, big_naryad, small_naryad, db_config, enter_bd):
        self.data_sources = data_sources
        self.scheme = scheme
        self.enter_bd = enter_bd
        self.big_naryad = big_naryad
        self.small_naryad = small_naryad
        self.db_config = db_config
        self.current_date = datetime.now().date()
        self.current_week_dates = self.get_current_week_dates()

    def get_current_week_dates(self):
        weekday = self.current_date.weekday()
        start_of_week = self.current_date - timedelta(days=weekday)
        current_week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
        return current_week_dates

    def main_7day(self):
        result = []
        sorted_query = None
        for date in self.current_week_dates:
            naryad_type = self.data_sources.get(date.strftime("%d.%m"), None)

            if naryad_type == "C1":
                temp = self.big_naryad
                result.append(date.strftime("%d.%m"))
                for role, (quantity, query_key) in temp.items():
                    query_result = self.get_personnel_from_database(query_key)
                    if date.isoweekday() not in [6, 7]:
                        if role in ["ЧК", "ДК", "ДЖГ"]:
                            sorted_query = sorted(query_result, key=lambda x: (x[4], x[6]))[:quantity]
                            print(f"{sorted_query}, ROLE {role}")
                            self.write_porsonnel_to_database(role, sorted_query, isodate=date)
                        elif role in ["ЧНК", "ПЧНК"]:
                            sorted_query = sorted(query_result, key=lambda x: (x[4], x[7]))[:quantity]
                            print(f"{sorted_query}, ROLE {role}")
                            self.write_porsonnel_to_database(role, sorted_query, isodate=date)
                        elif role in ["ЧП", "Ст.ЧП"]:
                            sorted_query = sorted(query_result, key=lambda x: (x[8]))[:quantity]
                            print(f"{sorted_query}, ROLE {role}")
                            self.write_porsonnel_to_database(role, sorted_query, isodate=date)
                        result.append((role, sorted_query))
                    else:
                        if role in ["ЧК", "ДК", "ДЖГ"]:
                            sorted_query = sorted(query_result, key=lambda x: (x[4], x[5], x[6]))[:quantity]
                            print(f"{sorted_query}, ROLE {role}")
                            self.write_porsonnel_to_database(role, sorted_query, isodate=date)
                        elif role in ["ПЧНК", "ЧНК"]:
                            sorted_query = sorted(query_result, key=lambda x: (x[4], x[5], x[7]))[:quantity]
                            print(f"{sorted_query}, ROLE {role}")
                            self.write_porsonnel_to_database(role, sorted_query, isodate=date)
                        elif role in ["ЧП", "Ст.ЧП"]:
                            sorted_query = sorted(query_result, key=lambda x: (x[8], x[9]))[:quantity]
                            print(f"{sorted_query}, ROLE {role}")
                            self.write_porsonnel_to_database(role, sorted_query, isodate=date)
                        result.append((role, sorted_query))

            else:
                temp = self.small_naryad
                result.append(date.strftime("%d.%m"))
                for role, (quantity, query_key) in temp.items():
                    query_result = self.get_personnel_from_database(query_key)
                    if date.isoweekday() not in [6, 7]:
                        sorted_query = sorted(query_result, key=lambda x: (x[4], x[6]))[:quantity]
                        print(f"{sorted_query}, ROLE {role}")
                        self.write_porsonnel_to_database(role, sorted_query, isodate=date)
                    else:
                        sorted_query = sorted(query_result, key=lambda x: (x[4], x[5], x[6]))[:quantity]
                        print(f"{sorted_query}, ROLE {role}")
                        self.write_porsonnel_to_database(role, sorted_query, isodate=date)
                    result.append((role, sorted_query))
                pprint.pprint(result, depth=3)
                result.clear()

    def get_personnel_from_database(self, query_key):
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()
        cursor.execute(self.scheme[query_key])
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    def write_porsonnel_to_database(self, role, query, isodate):
        isodate = isodate.isoweekday()
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()
        for i in query:
            if isodate not in [6, 7]:
                try:
                    cursor.execute(self.enter_bd[role].format(pib=repr(i[0])))
                    connection.commit()
                    print('sql request OK', role)
                except Exception as ex:
                    print(ex)
            else:
                try:
                    cursor.execute(self.enter_bd[role + "1"].format(pib=repr(i[0])))
                    connection.commit()
                    print('sql request OK', role)

                except Exception as ex:
                    print(ex)

        connection.commit()
        cursor.close()
        connection.close()

    def reset_bd(self):
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE newschema2.kurs SET `naryad` = 0, `naryad_sb` = 0, `kurs` = 0, `nk` = 0, `chepe` = 0, `chepe_sb` = 0;")
        connection.commit()
        cursor.close()
        connection.close()


# Example usage:
data_sources = {
    "26.02": "C0",
    "27.02": "C1",
    "28.02": "C2",
    "29.02": "C0",
    "01.03": "C1",
    "02.03": "C0",
    "03.03": "МК"
}

scheme = {
    "get_sergant": "SELECT * FROM newschema2.kurs WHERE `rank` = 'с-т';",
    "get_kursant_boy": "SELECT * FROM newschema2.kurs WHERE `rank` = 'сол.' AND `sex` = 'Чоловік';",
    "get_girl": "SELECT * FROM newschema2.kurs WHERE `rank` = 'сол.' AND `sex` = 'Жінка';"
}

big_naryad = {
    "ЧК": (1, "get_sergant"),
    "ДК": (2, "get_kursant_boy"),
    "ДЖГ": (1, "get_girl"),
    "ЧНК": (1, "get_sergant"),
    "ПЧНК": (3, "get_kursant_boy"),
    "Ст.ЧП": (1, "get_kursant_boy"),
    "ЧП": (9, "get_kursant_boy")
}
small_naryad = {
    "ЧК": (1, "get_sergant"),
    "ДК": (2, "get_kursant_boy"),
    "ДЖГ": (1, "get_girl")
}

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '72943618',
    'database': 'newschema2'
}
ENTER_BD = {
    "ЧК": "UPDATE newschema2.kurs SET `kurs` = `kurs` + 1,`naryad` = `naryad` + 1 WHERE `pib` = {pib};",
    "ДК": "UPDATE newschema2.kurs SET `kurs` = `kurs` + 1,`naryad` = `naryad` + 1 WHERE `pib` = {pib};",
    "ДЖГ": "UPDATE newschema2.kurs SET `kurs` = `kurs` + 1,`naryad` = `naryad` + 1 WHERE `pib` = {pib};",
    "ЧНК": "UPDATE newschema2.kurs SET `nk` = `nk` + 1,`naryad` = `naryad` + 1 WHERE `pib` = {pib};",
    "ПЧНК": "UPDATE newschema2.kurs SET `nk` = `nk` + 1,`naryad` = `naryad` + 1 WHERE `pib` = {pib};",
    "Ст.ЧП": "UPDATE newschema2.kurs SET `chepe` = `chepe` + 1 WHERE `pib` = {pib};",
    "ЧП": "UPDATE newschema2.kurs SET `chepe` = `chepe` + 1 WHERE `pib` = {pib};",

    # субота
    "ЧК1": "UPDATE newschema2.kurs SET `kurs` = `kurs` + 1,`naryad` = `naryad` + 1,`naryad_sb` = `naryad_sb` + 1 WHERE `pib` = {pib};",
    "ДК1": "UPDATE newschema2.kurs SET `kurs` = `kurs` + 1,`naryad` = `naryad` + 1,`naryad_sb` = `naryad_sb` + 1  WHERE `pib` = {pib};",
    "ДЖГ1": "UPDATE newschema2.kurs SET `kurs` = `kurs` + 1,`naryad` = `naryad` + 1,`naryad_sb` = `naryad_sb` + 1  WHERE `pib` = {pib};",
    "ЧНК1": "UPDATE newschema2.kurs SET `nk` = `nk` + 1,`naryad` = `naryad` + 1,`naryad_sb` = `naryad_sb` + 1  WHERE `pib` = {pib};",
    "ПЧНК1": "UPDATE newschema2.kurs SET `nk` = `nk` + 1,`naryad` = `naryad` + 1,`naryad_sb` = `naryad_sb` + 1  WHERE `pib` = {pib};",
    "Ст.ЧП1": "UPDATE newschema2.kurs SET `chepe` = `chepe` + 1,`chepe_sb` = `chepe_sb` + 1  WHERE `pib` = {pib};",
    "ЧП1": "UPDATE newschema2.kurs SET `chepe` = `chepe` + 1,`chepe_sb` = `chepe_sb` + 1  WHERE `pib` = {pib};"

}

scheduler = NaryadScheduler(data_sources, scheme, big_naryad, small_naryad, db_config, ENTER_BD)
scheduler.main_7day()
# scheduler.reset_bd()
