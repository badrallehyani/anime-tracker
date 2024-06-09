import json, time

from nyaasi import Nyaasi
from aria2_helpers.torrent_download_manager import create_download_manager

conf = json.load(open("conf.json", "r"))
DATA_FILE_NAME = conf.get("data_file_name")

ARIA2_XMLRPC_SERVER_URL = conf.get("aria2_xmlrpc_server_url")
DOWNLOAD_MANAGER = create_download_manager(ARIA2_XMLRPC_SERVER_URL)

def update_data(data: dict) -> None:
    open(DATA_FILE_NAME, "w").write(json.dumps(data))

def get_data() -> dict:
    return json.load(open(DATA_FILE_NAME, "r"))

def download(urls, path):
    DOWNLOAD_MANAGER.create_new_multiple_downloads(
        urls, path,
        options = {
                'seed-time': '0',
                'dir': path,
                'pause': 'false',
                'rpc-save-upload-metadata':'false'
        }
    )

def update(sleep_time) -> list:
    # returns a list of newly added files
    
    data = get_data()
    anime_list = data.get("anime_list")
    data_has_changed = False
    newly_added = []
    
    for anime in anime_list:
        name = anime.get("name")
        keyword = anime.get("keyword")
        done = anime.get("done")
        path = anime.get("path")

        search_result = Nyaasi.search(keyword)
        missing = [ i for i in search_result if i.get('URL') not in done ]
        missing_urls = [i.get('URL') for i in missing]
        missing_torrent_urls = [i.get('links').get('torrent_file') for i in missing]

        if missing:
            newly_added += missing
            data_has_changed = True
            
            download(missing_torrent_urls, path)
            anime.update({"done": done + missing_urls})

        time.sleep(sleep_time)

    if data_has_changed:
        update_data(data)

    return newly_added

if __name__ == '__main__':
    print(update(10), flush=True)
