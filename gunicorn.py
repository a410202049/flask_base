# -*- coding:utf-8 -*-
__author__ = 'kerry'

from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_script.commands import ShowUrls

app = create_app('local')
manager = Manager(app=app)
migrate = Migrate(app=app, db=db)


def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command("showurls", ShowUrls())

@manager.option('-h', '--host', dest='host', default='127.0.0.1')
@manager.option('-p', '--port', dest='port', type=int, default=5000)
@manager.option('-w', '--workers', dest='workers', type=int, default=4)
@manager.option('-t', '--timeout', dest='timeout', type=int ,default=90)
def gunicorn(host, port, workers,timeout):
    """Start the Server with Gunicorn"""
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            return {
                'bind': '{0}:{1}'.format(host, port),
                'workers': workers,'timeout' : timeout

            }

        def load(self):
            return app

    application = FlaskApplication()
    return application.run()


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()