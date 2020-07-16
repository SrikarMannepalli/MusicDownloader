''' Automatic Song download '''
import os
import json
import requests
from bs4 import BeautifulSoup
from terminaltables import AsciiTable


def give_options(video_data):
    ''' get the video_id of the video user needs downloaded '''
    tabledata = [['S No.', 'Track Title', 'Track length']]
    content_check = video_data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
        "sectionListRenderer"]["contents"][0]

    # bypass ads
    ind = 0
    if 'promotedSparklesTextSearchRenderer' in str(content_check):
        ind = 1

    content = video_data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
        "sectionListRenderer"]["contents"][ind]["itemSectionRenderer"]["contents"]
    
    ids = []
    for i in range(0, min(len(content), 10)):
        # try except to get out of did you mean renders and encountering playlists and stuff
        try:
            title = content[i]["videoRenderer"]["title"]["runs"][0]["text"]
            length = content[i]["videoRenderer"]["lengthText"]["simpleText"]
            video_id = content[i]["videoRenderer"]["videoId"]
            ids.append(video_id)
            tabledata.append([len(ids)-1, title, length])
        except BaseException:
            pass
    table = AsciiTable(tabledata)
    print(table.table)
    idx = 0
    idx = int(input("Which track do you prefer?. Enter S.no: "))
    return ids[idx]


query = input("Which song do you want to download?: ")
page = requests.get("https://www.youtube.com/results?search_query=" + query)
soup = BeautifulSoup(page.text, 'html.parser')
body = soup.findAll('script')
for bd in body:
    y = str(bd)
    if 'window["ytInitialData"]' not in y:
        continue
    ind1 = y.rfind('"responseContext')
    ind2 = y.rfind('window["ytInitialPlayerResponse"]')
    y = y[ind1 - 1:ind2 - 1].strip()[:-1]
    data = json.loads(y)
    chosen_id = give_options(data)
    break

os.system(
    'youtube-dl -x --audio-format mp3 --audio-quality 0 --output "%(title)s.%(ext)s" https://www.youtube.com/watch?v=' +
    chosen_id)

print("\nSong Downloaded!")
