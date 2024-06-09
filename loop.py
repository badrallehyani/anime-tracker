import logging, time
logging.basicConfig(filename="log.log", format='%(asctime)s - %(message)s', level=logging.INFO)

conf = json.load(open("conf.json", "r"))

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
