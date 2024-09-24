import requests
import os


url = 'https://pic3.zhimg.com/v2-5fb13110e1de13d4c11e6e7f5b8026da_r.jpg'

def download_img(url='https://pic3.zhimg.com/v2-5fb13110e1de13d4c11e6e7f5b8026da_r.jpg'):
    # url = url
    respone = requests.get(url)
    # print(respone.content)

    desktop_path = os.path.expanduser("~/Desktop")+'/1.jpg'

    with open(desktop_path, 'wb') as f:
        f.write(respone.content)
    
    return desktop_path


print(download_img())

