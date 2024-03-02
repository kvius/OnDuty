
def decorator(func):
    def inner(*args,**kwargs)
        try:
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database)

            with connection.cursor() as cursor:
                result = func(*args, *kwargs)

        except Exception as e:
            print(e)
        finally:
            if connection:
                connection.close()
    return inner