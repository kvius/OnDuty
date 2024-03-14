from database import DatabaseManager
import pymysql
from _datetime import datetime, timedelta
from shablons import scheme, big_naryad, small_naryad, DATA_COURCES, ENTER_BD

host = "localhost"
user = "root"
password = "72943618"
database = "newschema2"


class Algorithm(DatabaseManager):
    __assigned = []
    __result = {}

    # def __init__(self, host, user, password, db_name):
    #     super().__init__(host, user, password, db_name)
    #     self.current_date = datetime.now()
    #     self.start_date = datetime(datetime.now().year, datetime.now().month,
    #                                datetime.now().day - datetime.now().weekday())
    #     self.end_date = self.get_end_date()

    def __init__(self, scheme, big_naryad, small_naryad, data_sources, enter_bd, host, port, user, password,
                 db_name):
        super().__init__(host, user, password, db_name)
        self.current_date = datetime.now()
        self.start_date = datetime(datetime.now().year, datetime.now().month,
                                   datetime.now().day - datetime.now().weekday())
        self.end_date = self.get_end_date()
        self.scheme = scheme
        self.big_naryad = big_naryad
        self.small_naryad = small_naryad
        self.data_sources = data_sources
        self.enter_bd = enter_bd
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name

    def assign_naryad(self, cursor):
        naryad_set = big_naryad if self.data_sources[self.current_date] == "C1" else small_naryad
        print(naryad_set)

        for position, value in naryad_set.items():
            count, query_key = value
            cursor.execute(scheme[query_key])
            candidates = list(cursor.fetchall())
            filtered_candidates = [c for c in candidates if c[0] not in self.__assigned]
            filtered_candidates.sort(key=lambda x: x[4])
            selected = filtered_candidates[:count]
            self.__assigned.extend([s[0] for s in selected])
            self.__result[position] = [s[0] for s in selected]
        return self.__result

    def decorator(self, func):
        def inner(*args):
            try:
                connection = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.db_name)

                with connection.cursor() as cursor:
                    result = func(self, cursor, *args)
                    return result
            except Exception as e:
                print(e)
            finally:
                if connection:
                    connection.close()

        return inner

    @decorator
    def assign_naryad(self, cursor):
        naryad_set = big_naryad if self.data_sources[self.current_date] == "C1" else small_naryad
        print(naryad_set)

        for position, value in naryad_set.items():
            count, query_key = value
            cursor.execute(scheme[query_key])
            candidates = list(cursor.fetchall())
            filtered_candidates = [c for c in candidates if c[0] not in self.__assigned]
            filtered_candidates.sort(key=lambda x: x[4])
            selected = filtered_candidates[:count]
            self.__assigned.extend([s[0] for s in selected])
            self.__result[position] = [s[0] for s in selected]
        return self.__result

    def get_end_date(self):
        try:
            end_date = datetime(datetime.now().year, datetime.now().month,
                                datetime.now().day + 6 - datetime.now().weekday())
            return end_date
        except ValueError as VAL:
            days_until_next_week = 6 - self.current_date.weekday()
            end_date = self.current_date + timedelta(days=days_until_next_week)
            return end_date

    def date_iterator(self):
        current_date = self.start_date
        while current_date <= self.end_date:
            yield current_date.strftime("%d.%m")
            current_date += timedelta(days=1)


a = Algorithm(scheme, big_naryad, small_naryad, DATA_COURCES, ENTER_BD, host=host, user=user, password=password,
              db_name=database)
a.connect()
print(a.execute_query("SELECT * FROM newschema2.kurs WHERE `rank` = 'с-т';"))
a.close()

a.assign_naryad()
