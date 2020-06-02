# init the config

from . import config
from .component import mymysql

mymysql.init(config.app_conf["mysql"])
