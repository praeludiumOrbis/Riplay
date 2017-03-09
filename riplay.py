import requests
import errno
import os
import sys
import urllib

# Gets the Score Ids from Ripple's API then downloads the corresponding replays
def getReplays(username, mode):

    url = "https://ripple.moe/api/v1/users/scores/best?name=" + username + "&mode=" + str(mode)
    data = getJSON(url)

    # Check if username directory exists, create if it doesn't.
    newpath = r'/' + os.getcwd() + "/" + username 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # Download each score and store inside the username's folder
    try:
        for score in data['scores']:
            songName = score['beatmap']['song_name']
            scoreId = score['id']

            # Replace any "/" characters in the song name with " " 
            songName = songName.replace("/", " ")

            # Specify file path
            directory = os.path.join(os.getcwd() + "/" + username)
            fullfilename = directory + "/" + username + " - " + songName + '.osr'

            # Download Reokat
            try:
                urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
                downloadUrl = 'https://ripple.moe/web/replays/' + str(scoreId)

                urllib.urlretrieve(downloadUrl, str(fullfilename))
                print("Downloading Replay: " + songName + ".osr...")

            except Exception,e:
                print("ERROR: Could not download file: " + songName + ".osr")
                sys.exit(1)

        print("Download Complete.")
        # Might take a while, but download the beatmap and save the .osu file as well
        return
    except Exception,e:
        print("\nCan't download replays because the user doesn't have any scores for this mode.")
        sys.exit(1)
        

# Get Game Mode from the user
def getMode():

    mode = raw_input("\nSelect the game mode you'd like to download replays for\n1. osu!\n2. Taiko\n3. CTB\n4. Mania\n\nGame Mode: ")


    mode = int(mode)
    # Check for invalid mode
    if mode < 1 or mode > 4:
        print("\nInvalid choice given, please try again.")
        getMode()
    # Mode number for the Ripple API is 1 less than the options given in the mode input
    return getReplays(username, mode - 1)


# Gets JSON then calls a given function afterwards
def getJSON(url):

    try:
        data = requests.get(url=url).json()   
        if data['code'] and data['code'] != 200:
            print("Invalid request given, please try again\n")
            main()
        return data
    except requests.exceptions.Timeout:
        data = requests.get(url=url).json()
    except requests.exceptions.TooManyRedirects:
        print("Invalid link given")
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)


# Main Execution
username = raw_input("Enter a Ripple username to start downloading replays: ")
url = 'https://ripple.moe/api/v1/users?name=' + username
userStats = getJSON(url)
getMode()





