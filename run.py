from threading import Thread
import json, requests, os, urllib, time

with open("config.json", "r") as f:
    config = json.load(f)

def getJSON(url):
    try:
        data = requests.get(url=url).json()
        # if data['code'] and data['code'] != 200:
        #     print("Invalid request given, please try again\n")
        return data
    except requests.exceptions.Timeout:
        data = requests.get(url=url).json()
    except requests.exceptions.TooManyRedirects:
        print("Invalid link given")
    except requests.exceptions.RequestException as e:
        print (e)
        input()

def UserReplays(username, mode):
    print('Starting to download all replays from %s' % username)
    url = 'https://ripple.moe/api/v1/users/scores/best?name={}&mode={}&token={}'.format(username, mode, config["token"])
    data = getJSON(url)
    newpath = os.getcwd() + "/" + username
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    try:
        for score in data['scores']:
            songName = score['beatmap']['song_name']
            scoreId = score['id']
            nastyCharacters = ["\/", "\\", "<", ">", "?", ":", "*", "|", "\"", "/"]
            for char in nastyCharacters:
                songName = songName.replace(char, " ")
            directory = os.path.join(os.getcwd() + "/" + username)
            fullfilename = directory + "/" + username + " - " + songName + '.osr'
            try:
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                urllib.request.install_opener(opener)
                url = 'https://ripple.moe/web/replays/' + str(scoreId)
                local = str(fullfilename)
                urllib.request.urlretrieve(url, local)
            except Exception as e:
                print("ERROR: Could not download file: " + songName + ".osr", e)
                input()
        print("Downloading replays are done.")
        return
    except Exception as e:
        print("Can't download replays because the user doesn't have any scores for this mode.", e)
        input()

def LeaderBoardReplays(beatmapid, mode):
    scores = getJSON('https://ripple.moe/api/v1/scores?b=%s' % beatmapid)
    newpath = os.getcwd() + "/" + beatmapid
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    nastyCharacters = ["\/", "\\", "<", ">", "?", ":", "*", "|", "\"", "/"]
    # aa
    try:
        for score in scores['scores']:
            scoreSetter = score['user']['username']
            scoreId = score['id']
            directory = os.path.join(os.getcwd() + "/" + beatmapid)
            fullfilename = directory + "/" + scoreSetter + '.osr'
            try:
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve('https://ripple.moe/web/replays/' + str(scoreId), str(fullfilename))
            except Exception as e:
                print("ERROR: Could not download file: " + scoreSetter + ".osr", e)
        print("Download Complete.")
        return
    except Exception as e:
        print(e)
        input()

def UserReplaysWithDifficulty(username, mode):
    print('Starting to download all replays by %s with difficulty' % username)
    data = getJSON('https://ripple.moe/api/v1/users/scores/best?name={}&mode={}&token={}'.format(username, mode, config["token"]))
    newpath = os.getcwd() + "/" + username + "/beatmaps/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    nastyCharacters = ["\/", "\\", "<", ">", "?", ":", "*", "|", "\"", "/"]
    for score in data['scores']:
        songName = score['beatmap']['song_name']
        for char in nastyCharacters:
            songName = songName.replace(char, " ")
        beatmap_md5 = score['beatmap_md5']
        url2 = getJSON('https://ripple.moe/api/get_beatmaps?h=' + beatmap_md5)
        directory = os.path.join(os.getcwd() + "/" + username + "/beatmaps/")
        fullfilename = directory + "/" + songName + '.osu'
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve('http://osu.ppy.sh/osu/' + url2[0]["beatmap_id"], str(fullfilename))
    print("Downloading beatmaps are done.")
    return

print("""
Functions:
    1. Download replays from leader board
    2. Download replays from user
    3. Download replays from user with difficultly's
Mode:
    1. osu!
    2. Taiko
    3. CTB
    4. Mania
""")

option = int(input('Select an function: '))
if option == 1:
    beatmapid = input('Please enter beatmapid: ')
    mode = int(input('Please enter mode: '))
    Thread(target=LeaderBoardReplays, args=(beatmapid, mode-1, )).start()
elif option == 2:
    username = input('Please enter username: ')
    mode = int(input('Please enter mode: '))
    Thread(target=UserReplays, args=(username, mode-1,)).start()
elif option == 3:
    username = input('Please enter username: ')
    mode = int(input('Please enter mode: '))
    Thread(target=UserReplays, args=(username, mode-1, )).start()
    Thread(target=UserReplaysWithDifficulty, args=(username, mode-1, )).start()
else:
    print('Sorry this option is not valid.')