"""
Configuración de la aplicación Flask para PythonAnywhere.
Este archivo debe llamarse flask_app.py para que PythonAnywhere lo reconozca automáticamente.
"""
from app import app as application

# PythonAnywhere busca una variable llamada 'application'
if __name__ == '__main__':
    application.run()