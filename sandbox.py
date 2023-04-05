import os

BASE_DIR_DB = os.path.join(os.path.expanduser("~"), "OneDrive - Biocentric Living pty ltd", "MusicDB","MusicDB-DEV", "db.sqlite3") #OneDrive - Biocentric Living pty ltd\MusicDB\MusicDB-DEV

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR_DB,
    }
}