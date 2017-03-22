import requests
import errno
import os
import sys
import urllib.request


# Downloads top 50 beatmap replays to the beatmap Id's folder
def getBeatmapReplays(scores, beatmapId):

    # Check if beatmapId directory exists, create if it doesn't.
    newpath = os.getcwd() + "/" + beatmapId 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    # Download Replays
    try:
        for score in scores['scores']:
            scoreSetter = score['user']['username']
            scoreId = score['id']

            # Specify file path
            directory = os.path.join(os.getcwd() + "/" + beatmapId)
            fullfilename = directory + "/" + scoreSetter + '.osr'

            # Download
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
                print("Downloading Replay: " + scoreSetter + ".osr...")        
            except Exception as e:
                print("ERROR: Could not download file: " + scoreSetter + ".osr", e)
                sys.exit(1)     
                      
        print("Download Complete.")
        return
    except Exception as e:
        print(e)
        sys.exit(1)


# Used to grab the beatmap scores from Ripple's api
def getBeatmapScoresJSON(url):
    try:
        data = requests.get(url=url).json()   
        if data['code'] and data['code'] != 200 or data['scores'] is None:
            print("\nSorry, that beatmap either doesn't exist or isn't ranked.\n")
            sys.exit(1)
        # Return Beatmap JSON
        return data
    except requests.exceptions.Timeout:
        data = requests.get(url=url).json()
    except requests.exceptions.TooManyRedirects:
        print("Invalid link given")
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)    


beatmapId = input("Enter a beatmapId to start downloading Ripple Replays: ")
url = 'https://ripple.moe/api/v1/scores?b=' + beatmapId
beatmapScores = getBeatmapScoresJSON(url)
getBeatmapReplays(beatmapScores, beatmapId)

