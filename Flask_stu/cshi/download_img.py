import requests
import os


# url = 'http://localhost:7011/AfterImages/T_202493013471821980.jpg'

def download_img(url='http://115.231.97.229:6009/AfterImages/T_202493013471821980.jpg'):
    # url = url
    respone = requests.get(url)
    # print(respone.content)

    desktop_path = os.path.expanduser("~\Desktop")+'\\11.jpg'

    with open(desktop_path, 'wb') as f:
        f.write(respone.content)
    
    return desktop_path


print(download_img())

