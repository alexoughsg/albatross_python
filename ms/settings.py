
DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'cloud'
DATABASE_USER = 'root'
DATABASE_PASSWORD = ''
DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = '3306'
DATABASE_OPTIONS = {
   "init_command": "SET storage_engine=INNODB",
}

INSTALLED_APPS = (
    'albatross.ms',
    'south'
)

import logging
import logging.config
cfgfile="/Users/alex.ough/Projects/Python/github/albatross/ms/logging.cfg"
logging.config.fileConfig(cfgfile)
