Add in this folder a script 'local_settings.py' with the following content 
(replacing 'username' and 'password' by your actual username and password):

    DEFAULT_FROM_EMAIL = 'username <username@gmail.com>'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'username@gmail.com'
    EMAIL_HOST_PASSWORD = 'password'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587