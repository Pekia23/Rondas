class Config:
    SECRET_KEY = '773e2996b970504daadaf2625cfc07187e23035e4686aa8dade5bcb2ca190d13'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST ='localhost'
    MYSQL_USER ='root'
    MYSQL_PASSWORD =''
    MYSQL_DB='rondas'

config = {
    'development':DevelopmentConfig
}