import os


class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'ae5a3af4630a7a0eb5eef70d997f5ca0'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    #MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_USERNAME = "noreply.statusapp@gmail.com"
    #MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_PASSWORD = "Parola1234#"
