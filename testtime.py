import requests
import glob
from io import BytesIO
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import cognitive_face as CF
import locale
import math
import json
import time


start = time.time()

subscription_key = 'c44df6b56edb48e28b330a4178fefa4b'
assert subscription_key

locale.getdefaultlocale()

face_api_url = 'https://uksouth.api.cognitive.microsoft.com/face/v1.0/detect'
CF.Key.set('be41b43be574458a82f07a8c601793ea')
CF.BaseUrl.set('https://uksouth.api.cognitive.microsoft.com/face/v1.0/')
headers = { 'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream' }
    
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,facialHair,glasses,hair,makeup,accessories',
}
base_image = open("testimage.jpg", "rb").read()


response = requests.post(face_api_url, params=params, headers=headers, data=base_image)

print("Time took to execute entire script: {0}".format(time.time()-start))
