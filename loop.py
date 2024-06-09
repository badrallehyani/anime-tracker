import os, json, time

import logging
log_file_name = os.path.join( os.path.dirname(__file__), 'log.log' )
logging.basicConfig(filename=log_file_name, format='%(asctime)s - %(message)s', level=logging.INFO)

conf_file_name = os.path.join( os.path.dirname(__file__), 'conf.json' )
conf = json.load(open(conf_file_name, "r"))

SLEEP_BETWEEN_CHECKS = int(conf.get("sleep_between_checks"))
SLEEP_BETWEEN_ANIMES = int(conf.get("sleep_between_animes"))

from updater import update

while True:
    try:
        newly_added = update(SLEEP_BETWEEN_ANIMES)
    except Exception as e:
        logging.error(e)
        break
    
    if newly_added:
        logging.info("newly_added:" + str(newly_added))
    else:
        logging.info('nothing new')
    time.sleep(SLEEP_BETWEEN_CHECKS)
