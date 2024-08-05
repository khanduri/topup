
clear_db:
	mysql -uroot -e "DROP DATABASE IF EXISTS skeleton;"
	mongo skeleton-dev --eval "db.dropDatabase();"

create_db:
	mysql -uroot -e "CREATE DATABASE skeleton;"

db_upgrade:
	python manage.py db upgrade

reinit_db:
	$(MAKE) clear_db
	$(MAKE) create_db
	$(MAKE) db_upgrade
