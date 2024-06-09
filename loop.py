import logging, time
logging.basicConfig(filename="log.log", format='%(asctime)s - %(message)s', level=logging.INFO)

SLEEP_BETWEEN_ANIMES = 20
SLEEP_BETWEEN_CHECKS = 1800 # 30minutes

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
