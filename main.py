import PySimpleGUIQt as sg
import shutil
from sys import exit
try:
    import requests
except ImportError:
    print('Requests must be installed. PLease run: pip install requests')
    exit()

sg.theme('Reddit')  # Add some color to the window

layout = [
    [sg.Text('Name Of Subreddit (eg. "memes")', size=(32, 1)), ],
    [sg.InputText('', size=(32,1), key='input_subredditname')],
    [sg.Text('No. of Images', size=(30, 1))],
    [sg.InputText('', size=(32,1), key='numberofimages')],
    [sg.Submit()], ]

window = sg.Window('Reddit Image Downloader', layout, icon=r'J:\Python Projects\redditimage\icon.png')
event, values = window.Read()
if event == 'Submit':
    subredditname = values['input_subredditname']
    imagelimit = int(values['numberofimages'])
        

def makeUrl(afterID, subreddit):
        newUrl = subreddit.split('/.json')[0] + "/.json?after={}".format(afterID)
        return newUrl
    

def splitUrl(imageUrl):
        if 'jpg' or 'webm' or 'mp4' or 'gif' or 'gifv' or 'png' in imageUrl:
            return imageUrl.split('/')[-1]  


def downloadImage(imageUrl, imageAmount):  
                                
        filename = splitUrl(imageUrl)
        if filename:
            r = requests.get(imageUrl, stream=True)  
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
                print("Successfully downloaded: " + imageUrl)
                imageAmount += 1
        return imageAmount


def run():
    subreddit = (f'https://www.reddit.com/r/{subredditname}')
    print(subreddit)
    limit = imagelimit
    subJson = ''
    x = 0
    while x < limit:
        if subJson:
            url = makeUrl(subJson['data']['after'], subreddit)
        else:
            url = makeUrl('', subreddit)
        subJson = requests.get(url, headers={'User-Agent': 'MyRedditScraper'}).json()
        post = subJson['data']['children']
        postCount = range(len(post))

        for i in postCount:  
            imageUrl = (post[i]['data']['url'])
            _imageUrls = []
            _imageUrls.append(imageUrl)
            x = downloadImage(_imageUrls[0], x)
            if x == limit:
                break

run()
