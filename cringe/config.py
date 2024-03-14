import pymysql
from setup import host, port, user, password, database
from shablons import scheme, big_naryad, small_naryad, DATA_COURCES, ENTER_BD
from datetime import datetime, timedelta

assigned = []
result = {}

current_date = datetime.now()
start_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day - datetime.now().weekday())
try:
    end_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day + 6 - datetime.now().weekday())
except ValueError as VAL:
    days_until_next_week = 6 - current_date.weekday()
    end_date = current_date + timedelta(days=days_until_next_week)


def date_iterator(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date.strftime("%d.%m")
        current_date += timedelta(days=1)


def assign_naryad(date, data_sources, big_naryad, small_naryad, scheme):
    naryad_set = big_naryad if data_sources[date] == "C1" else small_naryad
    print(naryad_set)

    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database)

        with connection.cursor() as cursor:

            for position, value in naryad_set.items():
                count, query_key = value
                cursor.execute(scheme[query_key])
                candidates = list(cursor.fetchall())
                filtered_candidates = [c for c in candidates if c[0] not in assigned]
                filtered_candidates.sort(key=lambda x: x[4])
                selected = filtered_candidates[:count]
                assigned.extend([s[0] for s in selected])
                result[position] = [s[0] for s in selected]
            return result
    except Exception as e:
        print(e)
    finally:
        if connection:
            connection.close()


def write_bd(data, sql_templates):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database)

        with connection.cursor() as con:
            print("[CONNECTION] Success")
            for key, value in data.items():
                if key in sql_templates:
                    for _ in range(len(value)):
                        sql_query = sql_templates[key].format(pib=repr(value[_]))
                        print("[SQl] Executing SQL query:", sql_query)
                        try:
                            con.execute(sql_query)
                            # connection.commit()
                        except Exception as cringe:
                            print(f"[SQL] SQL request sticky {cringe}")
                else:
                    print("[SQL] No SQL template for this key", key)

    except Exception as e:
        print(e)
    finally:
        if connection:
            connection.close()
            print("[CONNECTION] Connection closed")
    result.clear()


def do_duty_of_7days(result, DATA_COURCES):
    weekday = datetime.now().weekday()
    temp_time = (datetime.now().day, datetime.now().month, datetime.now().year)
    start_day = (*temp_time, weekday)[0] - weekday
    monday_of7 = f"{start_day}.0{temp_time[1]}" if datetime.now().month < 10 else f"{start_day}.{temp_time[1]}"

    if DATA_COURCES[monday_of7]:
        print(DATA_COURCES[monday_of7])
    else:
        print("[SHABLONS] update data")

    for date in date_iterator(start_date, end_date):
        print(date)
        assign_naryad(date, DATA_COURCES, big_naryad, small_naryad, scheme)
        print(result)
        write_bd(result, ENTER_BD)
    return *temp_time, weekday, start_day


print(do_duty_of_7days(result, DATA_COURCES))