import requests
import glob
from io import BytesIO
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import cognitive_face as CF
import locale
import math
import json

subscription_key = 'c44df6b56edb48e28b330a4178fefa4b'
assert subscription_key

locale.getdefaultlocale()

class AdUnit:
    name = "Advertiser"
    age = "adult"
    gender = "male"
    facialHair = "no"
    glasses = "no"
    bald = "no"
    eyeMakeup = "no"
    lipMakeup = "no"
    hat = "no"



face_api_url = 'https://uksouth.api.cognitive.microsoft.com/face/v1.0/detect'
image_url = 'https://scontent-lhr3-1.xx.fbcdn.net/v/t1.0-9/44052524_2378544642162045_3114233859516923904_n.jpg?_nc_cat=103&_nc_ht=scontent-lhr3-1.xx&oh=ee0a7aa4eee6496c190d51808615bff3&oe=5D841C98'

headers = { 'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream' }
    
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,facialHair,glasses,hair,makeup,accessories',
}


CF.Key.set('be41b43be574458a82f07a8c601793ea')
CF.BaseUrl.set('https://uksouth.api.cognitive.microsoft.com/face/v1.0/')



ageGuess = "adult"
genderGuess = "male"
facialHairGuess = "no"
glassesGuess = "no"
hairGuess = "no"
lipMakeupGuess = "no"
eyeMakeupGuess = "no"
hatGuess = "no"

adUnits = []



#Load in ad data
adlabels = []

def parseData():
    
    with open("adlabels.txt", "r") as labeltext:
    
        for line in labeltext:
            adlabels.append(line)
#end parsedata

parseData()

adlabelCounter = 0


adlabelsSize = len(adlabels)
print("Ad labels size: {0}".format(adlabelsSize))

for x in range(0, adlabelsSize, 9):


        newAd = AdUnit()
        
        newAd.name = adlabels[x].strip()
        newAd.age = adlabels[x+1].strip()
        newAd.gender = adlabels[x+2].strip()
        newAd.facialHair = adlabels[x+3].strip()
        newAd.glasses = adlabels[x+4].strip()
        newAd.bald = adlabels[x+5].strip()
        newAd.eyeMakeup = adlabels[x+6].strip()
        newAd.lipMakeup = adlabels[x+7].strip()
        newAd.hat = adlabels[x+8].strip()

        adUnits.append(newAd)
   



#finished loading ads
#start getting passer-by details
    
base_image = open("testimage.jpg", "rb").read()

totalFacesCount = 0



response = requests.post(face_api_url, params=params, headers=headers, data=base_image)
d3 = json.dumps(json.loads(response.text))
alldata = response.json()
print(d3)
    
numfaces = len(alldata) #GET FACES NUM FROM API
print("Face count: {0}".format(numfaces))
   
   
    
for facenum in range(numfaces):
    totalFacesCount += 1    
    data = alldata[facenum]
    
    #print("Age: {0}".format(data['faceAttributes']['age']))
    
    if data['faceAttributes']['age'] < 18:
        ageGuess = "child"
    if data['faceAttributes']['age'] >= 18 and data['faceAttributes']['age'] < 60:
        ageGuess = "adult"
    if data['faceAttributes']['age'] >= 60:
        ageGuess = "elderly"

    print(ageGuess)
    
    predictedString = str(data['faceAttributes']['gender'])
    
    predictedString.strip()
    print("{0}".format(predictedString))
    genderGuess = data['faceAttributes']['gender']

    
    totalBeardNum = data['faceAttributes']['facialHair']['moustache']
    + data['faceAttributes']['facialHair']['beard']
    + data['faceAttributes']['facialHair']['sideburns']
    
    if totalBeardNum > 0.6:
        print("Has facial hair")
        facialHairGuess = "yes"
    else:
        facialHairGuess = "no"
        print("No facial hair")
       

    if data['faceAttributes']['glasses'] == "NoGlasses":
          print("No glasses")
          glassesGuess = "no"
    else:
          print("Has glasses")
          glassesGuess = "yes"



    predictedFloat = float(data['faceAttributes']['hair']['bald'])
      
    if predictedFloat >= 0.7:
        print("Bald")
        hairGuess = "yes"
    else:
        print("Not Bald")
        hairGuess = "no"

      
     
    predictedFloat = str(data['faceAttributes']['makeup']['lipMakeup'])
      
    if predictedFloat == "True":
        print("Lip Makeup")
        lipMakeupGuess = "yes"
    else:
        print("No Lip Makeup")
        lipMakeupGuess = "no"
         

      
    predictedString = str(data['faceAttributes']['makeup']['eyeMakeup'])
   
    if predictedString == "True":
        print("Eye Makeup")
        eyeMakeupGuess = "yes"
    else:
        print("No Eye Makeup")
        eyeMakeupGuess = "no"

         
      

    predictedString = str(data['faceAttributes']['accessories'])
    if predictedString != "[]":
        print("Has an accessory on")
        print(str(data['faceAttributes']['accessories'][0]))
        print(str(data['faceAttributes']['accessories'][0]['type']))
        if str(data['faceAttributes']['accessories'][0]['type']) == "headwear": 
            print("Has hat on")
            hatGuess = "yes"
        else:
            print("No hat on")
            hatGuess = "no"

    else:
        print("No hat on")
        hatGuess = "no"



#end of for each face loop

correctAds = []


for adunit in adUnits:
    adPoints = 0
    
    if adunit.age == ageGuess:
        adPoints += 1
        
        
    if adunit.age != ageGuess and adunit.age != "null":
        adPoints = -1000

        

    if adunit.gender == genderGuess:
        adPoints += 1
    
        
    if adunit.gender != genderGuess and adunit.gender != "null":
        adPoints = -1000



    if adunit.facialHair == facialHairGuess:
        adPoints += 1
        

        
    if adunit.facialHair != facialHairGuess and adunit.facialHair != "null":
        adPoints = -1000



    if adunit.glasses == glassesGuess:
        adPoints += 1
        
        
    if adunit.glasses != glassesGuess and adunit.glasses != "null":
        adPoints = -1000



    if adunit.bald == hairGuess:
        adPoints += 1
        
        
    if adunit.bald != hairGuess and adunit.bald != "null":
        adPoints = -1000



    if adunit.eyeMakeup == eyeMakeupGuess:
        adPoints += 1
        
        
    if adunit.eyeMakeup != eyeMakeupGuess and adunit.eyeMakeup != "null":
        adPoints = -1000




    if adunit.lipMakeup == lipMakeupGuess:
        adPoints += 1
        
        
    if adunit.lipMakeup != lipMakeupGuess and adunit.lipMakeup != "null":

        adPoints = -1000



    if adunit.hat == hatGuess:
        adPoints += 1
        
        
    if adunit.hat != hatGuess and adunit.hat != "null":
        adPoints = -1000


    if adPoints >= 0:
        print("Current best: {0}".format(adunit.name)) 
        correctAds.append(adunit)     
        
    
correctAd = AdUnit()
correctAdsLength = len(correctAds)
import random

randNum = random.randint(0,correctAdsLength-1)

print(randNum)

for ad in correctAds:
    correctAd = correctAds[randNum]

    
print("\n")
print(correctAd.name)




        
      
