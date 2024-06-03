import json, time
import logging
logging.basicConfig(filename="log.log", format='%(asctime)s - %(message)s', level=logging.INFO)
#
from nyaasi import Nyaasi
from aria2_helpers.torrent_download_manager import create_download_manager

conf = json.load(open("conf.json", "r"))

DATA_FILE_NAME = conf.get("data_file_name")
SLEEP_TIME = int(conf.get("sleep_time"))
ARIA2_XMLRPC_SERVER_URL = conf.get("aria2_xmlrpc_server_url")

DOWNLOAD_MANAGER = create_download_manager(ARIA2_XMLRPC_SERVER_URL)

def is_on() -> bool:
    return open("isOn", "r").read() == "1"

def update_data(data: dict) -> None:
    open(DATA_FILE_NAME, "w").write(json.dumps(data))

def get_data() -> dict:
    return json.load(open(DATA_FILE_NAME, "r"))

def download(urls, path):
    DOWNLOAD_MANAGER.create_new_multiple_downloads(urls, path)

while True:
    while is_on():
        data = get_data()
        anime_list = data.get("anime_list")
        data_has_changed = False

        for anime in anime_list:
            name = anime.get("name")
            keyword = anime.get("keyword")
            done = anime.get("done")
            path = anime.get("path")

            search_result = Nyaasi.search(keyword)
            result_urls = [
                (result.get("URL"), result.get("links").get("torrent_file"))
                for result in search_result
            ]
            missing = [i for i in result_urls if i[0] not in done]
            missing_urls = [i[0] for i in missing]
            missing_torrent_urls = [i[1] for i in missing]

            if(len(missing) != 0):
                data_has_changed = 1
                download(missing_torrent_urls, path)
                anime.update({"done": done + missing_urls})
        
        if(data_has_changed):
            update_data(data)
            logging.info("Updated")
        logging.info("Nothing New")

        time.sleep(SLEEP_TIME)

    logging.info("isOn: 0")
    time.sleep(SLEEP_TIME)