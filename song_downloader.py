import os
import json
import requests
from bs4 import BeautifulSoup
from terminaltables import AsciiTable

def give_options(data):
    tabledata = [['S No.', 'Track Title', 'Track length']]
    cont = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
    # print(len(cont))
    ids = []
    for i in range(0,min(len(cont),10)):
        try:
            title = cont[i]["videoRenderer"]["title"]["runs"][0]["text"]
            length = cont[i]["videoRenderer"]["lengthText"]["simpleText"]
            video_id = cont[i]["videoRenderer"]["videoId"]
            ids.append(video_id)
            tabledata.append([str(i), title, length])
        except:
            pass
    table = AsciiTable(tabledata)
    print(table.table)
    idx=0
    idx = int(input("Which track do you prefer?. Enter S.no: "))
    return ids[idx]

    
# artist= ""
# song = "needa padadani"
# Scraping YouTube for the song link
query = None
# if artist == "":
#     query = song
# elif song == "":
#     query = artist
# else:
    # query = artist+"+"+song
query = input("Which song do you want to download?: ") 
page = requests.get("https://www.youtube.com/results?search_query="+query)
soup = BeautifulSoup(page.text,'html.parser')
body = soup.findAll('script')
for bd in body:
    y = str(bd)
    if 'window["ytInitialData"]' not in y:
        continue
    # print(y)
    ind1 = y.rfind('"responseContext')
    ind2 = y.rfind('window["ytInitialPlayerResponse"]')
    y = y[ind1-1:ind2-1].strip()[:-1]
    data = json.loads(y)
    chosen_id = give_options(data)
    break

os.system('youtube-dl -x --audio-format mp3 --audio-quality 0 --output "%(title)s.%(ext)s" https://www.youtube.com/watch?v='+chosen_id)

print ("\nSong Downloaded!")


    


