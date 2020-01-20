import logging
from os import environ, path
from src.db_manager import DB_Manager
from configparser import ConfigParser


class Configuration():

    def determine_env(self):
        if "TOKEN" in environ:
            logging.info("Running in production mode")
            return "Production"
        else:
            logging.info("Running in local test mode")
            return "LocalTest"

    def configure_production(self):
        db_url = environ['DATABASE_URL']
        return DB_Manager(db_url)

    def configure_local_test(self):
        config = ConfigParser()
        if not path.isfile('.config/config.ini'):
            self.first_local_config(config)
        config.read_file(open('.config/config.ini'))
        db_url = "postgres://" + config['DB']['username'] + (":" + config['DB']['password'] if config['DB']['password'] != '' else '') + "@" + config['DB']['host'] + "/" + config['DB']['name']
        return DB_Manager(db_url)

    def first_local_config(self, config):
        print("This is the first time you run this bot in LocalTest mode, let's config the environment:")
        config['DB'] = {}
        config['DB']['username'] = input('Database username: ')
        config['DB']['password'] = input('Database password: ')
        config['DB']['host'] = input('Database host: ')
        config['DB']['name'] = input('Database name: ')
        with open('.config/config.ini', 'w') as configfile:
            config.write(configfile)
        print("Cool! You have configured the environment!")
        print("Configuration file saved on .config/config.ini")

    def configure(self):
        env = self.determine_env()
        if env == 'Production':
            return self.configure_production()
        elif env == 'LocalTest':
            return self.configure_local_test()
        else:
            logging.error('Something went wrong on configuration')