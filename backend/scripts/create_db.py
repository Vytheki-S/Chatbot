import pymysql


def ensure_database_exists():
	connection = pymysql.connect(
		host='localhost',
		user='root',
		password='2003',
		autocommit=True,
	)
	with connection.cursor() as cursor:
		cursor.execute(
			"CREATE DATABASE IF NOT EXISTS EventAura CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
		)
	print("MySQL database 'EventAura' ensured.")


def drop_and_create_database():
	connection = pymysql.connect(
		host='localhost',
		user='root',
		password='2003',
		autocommit=True,
	)
	with connection.cursor() as cursor:
		cursor.execute("DROP DATABASE IF EXISTS EventAura;")
		cursor.execute(
			"CREATE DATABASE EventAura CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
		)
	print("MySQL database 'EventAura' dropped and recreated.")


if __name__ == "__main__":
	drop_and_create_database()


