import json

import os
import requests

esAddr = "http://192.168.0.102:9200/"
indexName = "tmdb"
mappingFolder = "./mapping"
headers = {"Content-Type": "application/json", "Accept": "application/json"}


def extract():
    f = open('./tmdb.json')
    if f:
        return json.loads(f.read())
    return {}


def reindex(settings, movieDict=None):
    resp = requests.delete(esAddr + indexName)  # D
    data = json.dumps(settings, indent=4, sort_keys=True)
    print("settings:\n%s" % data)
    resp = requests.put(esAddr + indexName,
                        headers=headers, json=settings)

    print(
        "Response for createing the index with the settings and mappings. %s" % resp.text)

    bulkMovies = ""
    movieDict = movieDict or {}
    for id, movie in movieDict.items():
        addCmd = {
            "index": {
                "_index": indexName,
                "_type": "_doc",
                "_id": movie["id"]
            }
        }
        bulkMovies += json.dumps(addCmd) + "\n" + json.dumps(movie) + "\n"

    print("Start ingesting data......")
    resp = requests.post("%s/_bulk" % esAddr,
                         headers={"content-type": "application/json"},
                         data=bulkMovies)
    # print resp.content


def select_mapping():
    print(
        "\r\n>> Please select the mapping file. Choose 0 for empty mapping\r\n")
    mappingList = os.listdir(mappingFolder)
    print(
        "[0] empty mapping. It will use dynamic mapping with default settings")
    for idx, mappingItem in enumerate(mappingList):
        print("[%d] %s" % (idx + 1, mappingItem))
    userInput = input()
    try:
        selectIndex = int(userInput)
    except ValueError:
        selectIndex = -1

    if selectIndex == -1 or selectIndex > len(mappingList) + 1:
        print('\033[31mPlease provide a valid integer \033[0m')
        msg = "from 0 to %d." % (len(mappingList))
        print(msg)
        exit()
    if selectIndex == 0:
        print("return empty")
        return {}
    mappingName = mappingList[selectIndex - 1]
    fileName = "%s/%s" % (mappingFolder, mappingName)
    f = open(fileName)
    mapping = {}
    if f:
        mapping = json.loads(f.read())
    return mapping


def main():
    movieDict = extract()
    mapping = select_mapping()
    reindex(settings=mapping, movieDict=movieDict)
    print("Done for ingesting TMDB data into Elasticsearch")


if __name__ == "__main__":
    main()
