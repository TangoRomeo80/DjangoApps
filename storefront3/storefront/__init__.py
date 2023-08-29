import pymysql
from .celery import celery # Import celery object from celery.py to initialize it

# Configure pymysql to work with Django
pymysql.install_as_MySQLdb()
