import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json, sys, json
import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw
import cv2
import base64
import os
import time

def is_male(attr):
    if attr == 'male':
        return True



def recogn(KEY, img_url):
    CF.Key.set(KEY)
    BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
    CF.BaseUrl.set(BASE_URL)
    detected = CF.face.detect(img_url)
    print (detected)
    return detected
    
   

imageFiles = os.listdir("images")
faceIds = []
images = []

basedir = "images/"
key = "c7cce2e49cb84d7bbe09a5b75535468a"

notdetected = 0
for i,url in enumerate(imageFiles):
    try:
        detected = recogn(key, basedir+url)
        if len(detected) > 0:
            faceIds.append(detected[0]['faceId'])
            images.append(url)
        else:
            notdetected+=1
        
    except:
        pass
    time.sleep(3)


#print (faceIds)

subscription_key = key
uri_base = 'https://westcentralus.api.cognitive.microsoft.com'
headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
}

#body = {'url': url}
body = {'faceIds': faceIds}

response = requests.request('POST', uri_base + '/face/v1.0/group', json=body, data=None, headers=headers, params=None)
parsed = json.loads(response.text)

groups = parsed['groups']
mess = parsed['messyGroup']

for i,group in enumerate(groups):
    directory = "groups/"+str(i)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for j,faceId in enumerate(group):
        ind = faceIds.index(faceId)

        imageToCopy = "images/"+str(images[ind])
        print("imageTocopy: "+str(imageToCopy))
        img = cv2.imread(imageToCopy,1)
        cv2.imwrite(directory+"/"+images[ind], img)
        
    

directory = "groups/Mess"
if not os.path.exists(directory):
    os.makedirs(directory)
for j,faceId in enumerate(mess):
    ind = faceIds.index(faceId)

    imageToCopy = "images/"+str(images[ind])
    print("imageTocopy: "+str(imageToCopy))
    img = cv2.imread(imageToCopy,1)
    cv2.imwrite(directory+"/"+images[ind], img)
        
print("not detected: "+str(notdetected))
print(parsed)


