import os
class Config:
    SECRET_KEY = 'mastermind'
    TEMPLATES_AUTO_RELOAD = True

    # Configuration Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'vainqueurkalema035@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '00Kalema'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

