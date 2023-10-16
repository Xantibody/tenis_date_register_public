import configparser

class UtilService:
    def create_conf():
        conf = configparser.ConfigParser()
        conf.read('tenis_date_register/config/config.ini')
        return conf