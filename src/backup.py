import logging

def backup():
    from os import environ
    import redis
    from rq import Queue

    redis_url = environ['REDISTOGO_URL']

    q = Queue(connection=redis.from_url(redis_url))
    q.enqueue(backup_internal)


def backup_internal():
    import logging
    from src.Configuration.Configure import Configuration
    from configparser import ConfigParser
    import gzip
    from sh import pg_dump

    logging.info('Backupping')

    if Configuration().determine_env() == 'LocalTest':
        logging.info('LocalTestMode: local backup')
        config = ConfigParser()
        config.read_file(open('.config/config.ini'))
        host = config['DB']['host']
        user = config['DB']['username']
        db = config['DB']['name']
        with gzip.open('backup.gz', 'wb') as backup:
            pg_dump('--column-inserts', '-h', host, '-U', user, db, '-p', '5432', _out=backup)
        return
    else:
        logging.info('Remote Backup')
        host, user, db, port = db_url_parser()

        with gzip.open('backup.gz', 'wb') as backup:
            pg_dump('--column-inserts', '-h', host, '-U', user, db, '-p', port, _out=backup)
        dropbox_upload('backup.gz')
        return


def db_url_parser():
    from os import environ

    logging.info('Parsing db url')

    db_url = environ['DATABASE_URL']
    list = db_url.split('/')[2:]
    user = list[0].split(':')[0]
    port = list[0].split(':')[2]
    host = list[0].split('@')[1].split(':')[0]
    password = list[0].split(':')[1].split('@')[0]
    db = list[1]

    logging.info('db url parsed')
    return host, user, db, port


def dropbox_upload(backup_file):
    from datetime import date
    from dropbox import Dropbox
    from dropbox.exceptions import AuthError, ApiError
    from dropbox.files import WriteMode
    from os import environ, system

    backup_path = '/backup' + str(date.today()) + '.gz'
    dbx = Dropbox(environ['DROPBOX_API_KEY'])
    logging.info('Uploading ' + backup_file + ' to Dropbox as ' + backup_path)

    try:
        dbx.users_get_current_account()
    except AuthError:
        logging.ERROR('Invalid dropbox token, cannot authenticate')
        return

    remove_old_backups(dbx)

    with open(backup_file, 'rb') as backup:
        try:
            logging.info('Uploading ' + backup_file + ' to Dropbox as ')
            dbx.files_upload(backup.read(), backup_path, mode=WriteMode('overwrite'))
            logging.info('Backup succeded!')
            system('rm', backup_file)
            return
        except ApiError as err:
            if err.error.is_path() and err.error.get_path().reason.is_insufficient_space():
                logging.Error('No free space available to Dropbox, cannot backup')
                system('rm', backup_file)
                return
            elif err.user_message_text:
                logging.ERROR('Cannot backup: ' + err.user_message_text)
                return
            else:
                logging.ERROR(err)
                return

def remove_old_backups(dbx):
    from datetime import date
    try:
        current_year = date.today().year
        dbx.files_delete('/backup' + date.today().replace(year=current_year-1) + '.gz')
        logging.warning('Removed old backup')
        return
    except:
        logging.info('No backup older than a year to be removed')
        return
