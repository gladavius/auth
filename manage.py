from flask_script import Manager
from project.server import app, db, models

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
