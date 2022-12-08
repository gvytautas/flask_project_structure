"""
-flask-application-deployment
-linux server
-nginx (reverse proxy)
-gunicorn (WSGI Web Server Gateway Interface)
-supervisor
"""
from flask_project import app

if __name__ == '__main__':
    app.run(host='0.0.0.0')
