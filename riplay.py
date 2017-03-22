from threading import Thread
import json, requests, os, urllib, time

# Open config.json to get token (used for downloading replays of banned players) - Only for Community Managers
with open("config.json", "r") as f:
    config = json.load(f)

# Gets JSON from a given beatnap
def getJSON(url):
    try:
        data = requests.get(url=url).json()
        return data   
    except requests.exceptions.Timeout:
        data = requests.get(url=url).json()
    except requests.exceptions.TooManyRedirects:
        print("Invalid link given")
    except requests.exceptions.RequestException as e:
        print (e)

# Downloads replays ONLY from a given user
def UserReplays(username, mode):
    print('Starting to download all replays from %s' % username)

    # Get data from Ripple API
    url = 'https://ripple.moe/api/v1/users/scores/best?name={}&mode={}&token={}'.format(username, mode, config["token"])
    data = getJSON(url)

    # Create path with the player's username if it doesn't already exist.
    newpath = os.getcwd() + "/" + username
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    
    try:
        for score in data['scores']:

            # Get required data from API
            songName = score['beatmap']['song_name']
            scoreId = score['id']

            # Replace any nasty characters in the song's name - Error prevention
            nastyCharacters = ["\/", "\\", "<", ">", "?", ":", "*", "|", "\"", "/"]
            for char in nastyCharacters:
                songName = songName.replace(char, " ")

            # Specify the full file path
            directory = os.path.join(os.getcwd() + "/" + username)
            fullfilename = directory + "/" + username + " - " + songName + '.osr'

            try:

                # Create opener w/ headers    
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                urllib.request.install_opener(opener)

                url = 'https://ripple.moe/web/replays/' + str(scoreId)
                local = str(fullfilename)

                # Download Replay
                urllib.request.urlretrieve(url, local)
                print("Downloading " + songName + ".osr...")

            except Exception as e:
                print("ERROR: Could not download file: " + songName + ".osr", e)

        print("Downloading replays is complete!")
        return
    except Exception as e:
        print("Can't download replays because the user doesn't have any scores for this mode.", e)


# Gets the top 50 replays of a given beatmap
def LeaderBoardReplays(beatmapid, mode):

    # Get data from Ripple API
    scores = getJSON('https://ripple.moe/api/v1/scores?b=%s' % beatmapid)

    # Create path if it doesn't exist
    newpath = os.getcwd() + "/" + beatmapid
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    try:
        for score in scores['scores']:
            # Get required data
            scoreSetter = score['user']['username']
            scoreId = score['id']

            # Specify file path
            directory = os.path.join(os.getcwd() + "/" + beatmapid)
            fullfilename = directory + "/" + scoreSetter + '.osr'

            try:
                # Opener w/ headers
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                urllib.request.install_opener(opener)

                # Download Replay
                urllib.request.urlretrieve('https://ripple.moe/web/replays/' + str(scoreId), str(fullfilename))
                print("Downloading " + scoreSetter + ".osr...")
            except Exception as e:
                print("ERROR: Could not download file: " + scoreSetter + ".osr", e)
        print("Download Complete.")
        return
    except Exception as e:
        print(e)


# Downloads a given user's top 50 replays + the .osu files as well
def UserReplaysWithDifficulty(username, mode):

    # Get Data from API
    print('Starting to download all replays by %s with the .osu files' % username)
    data = getJSON('https://ripple.moe/api/v1/users/scores/best?name={}&mode={}&token={}'.format(username, mode, config["token"]))
    
    # Create path if doesn't exist
    newpath = os.getcwd() + "/" + username + "/beatmaps/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # specify all nasty characters
    nastyCharacters = ["\/", "\\", "<", ">", "?", ":", "*", "|", "\"", "/"]

    for score in data['scores']:

        # Get the song's name and remove the nasty characters from it
        songName = score['beatmap']['song_name']
        for char in nastyCharacters:
            songName = songName.replace(char, " ")

        # Get beatmap_md5 from the given beatmap
        beatmap_md5 = score['beatmap_md5']
        url2 = getJSON('https://ripple.moe/api/get_beatmaps?h=' + beatmap_md5)

        # Specify file path
        directory = os.path.join(os.getcwd() + "/" + username + "/beatmaps/")
        fullfilename = directory + "/" + songName + '.osu'

        # Opener w/ headers
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        # Get .osu file
        urllib.request.urlretrieve('http://osu.ppy.sh/osu/' + url2[0]["beatmap_id"], str(fullfilename))
        print("Downloading " + songName + ".osu...")
    print("Downloading beatmaps complete!")
    return


# Main Execution
print("""
Options:
    1. Download the top 50 replays from a beatmap
    2. Download the top 50 replays from a given user
    3. Download the top 50 replays from a given user + .osu files
Game Mode:
    1. osu!
    2. Taiko
    3. CTB
    4. Mania
""")

# Get option from user
option = int(input('Select an option to begin: '))

if option == 1:
    beatmapid = input('Enter a beatmapId (/b/) to begin: ')
    mode = int(input('Game Mode: '))
    Thread(target=LeaderBoardReplays, args=(beatmapid, mode-1, )).start()

elif option == 2:
    username = input('Enter a username to begin: ')
    mode = int(input('Game Mode: '))
    Thread(target=UserReplays, args=(username, mode-1,)).start()

elif option == 3:
    username = input('Enter a username to begin: ')
    mode = int(input('Gane Mode: '))
    Thread(target=UserReplays, args=(username, mode-1, )).start()
    Thread(target=UserReplaysWithDifficulty, args=(username, mode-1, )).start()

else:
    print('Invalid option. Try again.')