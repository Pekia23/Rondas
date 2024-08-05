# config.py
import os

class Config:
    SECRET_KEY = '773e2996b970504daadaf2625cfc07187e23035e4686aa8dade5bcb2ca190d13'
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = './flask_session_files'  # Directorio para almacenar las sesiones
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'flask_'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'rondas'

config = {
    'development': DevelopmentConfig
}
