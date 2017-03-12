import requests
import errno
import os
import sys
import urllib.request

# Gets the Score Ids from Ripple's API then downloads the corresponding replays
def getReplays(username, mode):

    url = "https://ripple.moe/api/v1/users/scores/best?name=" + username + "&mode=" + str(mode)
    data = getJSON(url)

    # Check if username directory exists, create if it doesn't.
    newpath = os.getcwd() + "/" + username
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

            # Download Replay
            try:
                # Create Opener w/ headers
                opener=urllib.request.build_opener()
                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                urllib.request.install_opener(opener)

                # URL & File path
                url = 'https://ripple.moe/web/replays/' + str(scoreId)                
                local = str(fullfilename)

                # Download
                urllib.request.urlretrieve(url, local)
                print("Downloading Replay: " + songName + ".osr...")
            except Exception as e:
                print("ERROR: Could not download file: " + songName + ".osr", e)
                sys.exit(1)
        print("Download Complete.")
        return
    except Exception as e:
        print("\nCan't download replays because the user doesn't have any scores for this mode.", e)
        sys.exit(1)
        

# Get Game Mode from the user
def getMode():

    mode = input("\nSelect the game mode you'd like to download replays for\n1. osu!\n2. Taiko\n3. CTB\n4. Mania\n\nGame Mode: ")

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
        print (e)
        sys.exit(1)


# Main Execution
username = input("Enter a Ripple username to start downloading replays: ")
url = 'https://ripple.moe/api/v1/users?name=' + username
userStats = getJSON(url)
getMode()





