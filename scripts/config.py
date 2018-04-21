import os
import sys
import json
import logging.config

from configparser import ConfigParser

logger = logging.getLogger(__name__ + ".config_server")
BASE_PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SERVER_CONFIG_FILE = os.path.join(BASE_PROJECT_FOLDER, "server_cfg.ini")
LOGGING_CONFIG_FILE = os.path.join(BASE_PROJECT_FOLDER, "logger_config.json")


if os.path.exists(LOGGING_CONFIG_FILE):
    with open(LOGGING_CONFIG_FILE, "rt") as log_file:
            logging.config.dictConfig(json.load(log_file))
else:
    logging.basicConfig(level=logging.INFO)

if os.path.exists(SERVER_CONFIG_FILE):
        config_parser = ConfigParser()
        config_parser.read(SERVER_CONFIG_FILE   )
else:
    logger.error("Config file dosen't exist")
    sys.exit(1)

DATABASE_CONFIG = {
    str(option) : str(config_parser.get("database_config", option)) for option in \
            config_parser.options("database_config")
}
