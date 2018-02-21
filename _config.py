import os

# grab the folder where this project lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'csv.db'
SECRET_KEY = 'my_precious'
DATABASE_PATH = os.path.join(basedir, DATABASE)
