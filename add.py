import json

conf = json.load(open("conf.json", "r"))
DATA_FILE_NAME = conf.get("data_file_name")

if __name__ == "__main__":
    name = input("Anime Name: ")
    keyword = input("Keyword: ")
    path = input("Path: ")

    data = json.load(open(DATA_FILE_NAME, 'r'))

    new_anime_list = data.get("anime_list")
    new_anime_list.append({
        "name": name,
        "keyword": keyword,
        "done": [],
        "path": path
    })
    
    data.update({"anime_list": new_anime_list})

    open(DATA_FILE_NAME, 'w').write(json.dumps(data))
