import psycopg2

# Строка подключения к базе данных PostgreSQL
conn_string = "host='bxml7wtus4yekwz4icln-postgresql.services.clever-cloud.com' port = '50013' dbname='bxml7wtus4yekwz4icln' user='uoognc3we7m8fex8zn9b' password='yF7GoBpVaphGxFaXZpoeL9ixj6dFw2'"

# Подключение к базе данных
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

# Чтение содержимого SQL файла
with open("D:\pg_schema.sql", 'r') as sql_file:
    sql = sql_file.read()

# Выполнение SQL запросов из файла
cursor.execute(sql)
conn.commit()

# Закрытие соединения
cursor.close()
conn.close()
