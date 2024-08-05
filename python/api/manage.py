from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import url_for
from src import create_app, db


app = create_app()
migrate = Migrate(app, db)


manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = "{:50s} {:20s} {}".format(rule.endpoint, methods, url)
        output.append(line)

    for line in sorted(output):
        print(line)


if __name__ == '__main__':
    manager.run()
