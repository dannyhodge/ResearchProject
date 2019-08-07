import requests
import json
import glob
from io import BytesIO
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import cognitive_face as CF
import locale
import requests
from io import BytesIO
from PIL import Image, ImageDraw
import json
import math

subscription_key = 'c44df6b56edb48e28b330a4178fefa4b'
assert subscription_key

locale.getdefaultlocale()


face_api_url = 'https://uksouth.api.cognitive.microsoft.com/face/v1.0/detect'
image_url = 'https://scontent-lhr3-1.xx.fbcdn.net/v/t1.0-9/44052524_2378544642162045_3114233859516923904_n.jpg?_nc_cat=103&_nc_ht=scontent-lhr3-1.xx&oh=ee0a7aa4eee6496c190d51808615bff3&oe=5D841C98'


ageAccuracy = 0
genderAccuracy = 0
facialHairAccuracy = 0
glassesAccuracy = 0
hairAccuracy = 0
lipMakeupAccuracy = 0
eyeMakeupAccuracy = 0
hatAccuracy = 0

image_list = []
image_paths = []
labels = []

for filename in glob.glob('testimages/*.jpg'): #assuming gif
    image_data = open(filename, "rb").read()
    image_list.append(image_data)
   # print("Path: {0}".format(filename))
    image_paths.append(filename)
    

headers = { 'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream' }
    
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,facialHair,glasses,hair,makeup,accessories',
}
#'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',

#response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})



CF.Key.set('be41b43be574458a82f07a8c601793ea')
CF.BaseUrl.set('https://uksouth.api.cognitive.microsoft.com/face/v1.0/')


def parseData():
    
    with open("testimages/labels.txt", "r") as labeltext:
    
        for line in labeltext:
            labels.append(line)
            #print(line)

def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

parseData()



counter = 0
    
#for img in image_list:
    
   # response = requests.post(face_api_url, params=params, headers=headers, data=img)
 #   print(response.json())
  #  faces = CF.face.detect(image_paths[counter])
                          
  #  image = Image.open(BytesIO(img))

  #  draw = ImageDraw.Draw(image)
 #   for face in faces:
 #       draw.rectangle(getRectangle(face), outline='red')
 #       print(faces)
  #  image.show()
 #   counter = counter + 1

counter = 0

totalFacesCount = 0

for img in image_list:
    labelimage = counter * 10
    response = requests.post(face_api_url, params=params, headers=headers, data=img)

   # if labels[labelimage][2] == '-':      
   #     print("Image: {0}".format(labels[labelimage][1]))
#    else:
  #      print("Image: {0}{1}".format(labels[labelimage][1],labels[labelimage][2]))
    d3 = json.dumps(json.loads(response.text))
    alldata = response.json()
    print(d3)
    
    numfaces = len(alldata) #GET FACES NUM FROM API
  #  print("numfaces")
    print(numfaces)
 #   
   
    
    for facenum in range(numfaces):
      totalFacesCount += 1
      print("Total faces count: {0}".format(totalFacesCount))
      tempLabelNum = labels[labelimage][3]
      if tempLabelNum == '-':
          tempLabelNum = int(labels[labelimage][4])
      else:
          tempLabelNum = int(labels[labelimage][3])
          
      
  
      
      if facenum != tempLabelNum-1:
       # print("Label num: ")
      #  print(labels[labelimage])
    #    print("FACE NOT FOUND, MUST BE OBSCURED, MOVE ONTO NEXT LABEL")
        counter = counter + 1
        labelimage = counter * 10

     # print("Label num: ")
  #    print(labels[labelimage])
      
    #  print("Face number: {0}".format(facenum))
      data = alldata[facenum]
 
        
      print("Age: ")
      print("Actual {0}".format(labels[labelimage+2]))
      print("API estimation: {0}".format(data['faceAttributes']['age']))
    #  print("Just num: {0}".format(labels[labelimage+2][5:]))
    
      #print(labelimage)
      #print(labels[labelimage])
      numAge = labels[labelimage+2][5:-1]
      
      ageDiff = float(data['faceAttributes']['age']) - float(numAge)
      ageDiff = ageDiff * ageDiff
      ageDiff = math.sqrt(ageDiff)
      print("Age diff: {0}".format(ageDiff))
      if ageDiff <= 5:
          print("AGE CORRECT")
          ageAccuracy += 1
      else:
          print("AGE NOT CORRECT")


      
      print("\n")

      print("Gender")


      labelledString = str(labels[labelimage+1][8:-1])
      labelledString.strip()

      predictedString = str(data['faceAttributes']['gender'])
      predictedString.strip()

      print("{0}".format(labelledString))
      print("{0}".format(predictedString))
      if labelledString == predictedString:
          print("GENDER CORRECT")
          genderAccuracy += 1
      else:
          print("GENDER NOT CORRECT")
   

      print("Facial Hair")
   #   print("Actual {0}".format(labels[labelimage+3]))
      totalBeardNum = data['faceAttributes']['facialHair']['moustache'] + data['faceAttributes']['facialHair']['beard'] + data['faceAttributes']['facialHair']['sideburns']
   #   print("BEARD TOTAL NUM:")
   #   print(totalBeardNum)
      hasFacialHair = " "
      if totalBeardNum > 0.6:
          hasFacialHair = "yes"
          print("Has facial hair")
      else:
          hasFacialHair = "no"
          print("Has NO facial hair")

      labelledString = str(labels[labelimage+3][12:-1])
      labelledString.strip()

  #    print("Predicted facialhair: {0}".format(hasFacialHair))
   #   print(labels[labelimage+3][12:])
      if hasFacialHair == labelledString:
          print("FACIAL HAIR CORRECT")
          facialHairAccuracy += 1
     # else:
          print("FACIAL HAIR NOT CORRECT")

      print("\n")
        
      print("Glasses")
    #  print("Actual {0}".format(labels[labelimage+4]))
      labelledString = str(labels[labelimage+4][9:-1])
      labelledString.strip()
      glassesPrediction = " "
      if data['faceAttributes']['glasses'] == "NoGlasses":
          print("no glasses")
          glassesPrediction = "no"
      else:
          print("has glasses")
          glassesPrediction = "yes"

      if glassesPrediction == labelledString:
          print("Glasses correct")
          glassesAccuracy += 1
      else:
         print("ERROR ERROR GLASSES INCORRECT")
         
     # print("API estimation: {0}".format(data['faceAttributes']['glasses']))
   #   print("\n")




     

      print("Hair")

      print("Actual {0}".format(labels[labelimage+6]))
      labelledString = str(labels[labelimage+6][6:-1])
      labelledString.strip()
      predictedFloat = float(data['faceAttributes']['hair']['bald'])
      
      hairPrediction = " "
      if predictedFloat >= 0.7:
          print("Bald")
          hairPrediction = "yes"
      else:
          print("Not Bald")
          hairPrediction = "no"

      if hairPrediction == labelledString:
          print("Hair correct")
          hairAccuracy += 1
      else:
         print("Hair INCORRECT")
         
    
      print("\n")

      
      
      print("Lip Makeup")

      print("Actual {0}".format(labels[labelimage+8]))
      labelledString = str(labels[labelimage+8][11:-1])
      labelledString.strip()
      predictedFloat = str(data['faceAttributes']['makeup']['lipMakeup'])
      
      lipPrediction = " "
      if predictedFloat == "True":
          print("Lip Makeup is true")
          lipPrediction = "yes"
      else:
          print("Lip Makeup is false")
          lipPrediction = "no"

      if lipPrediction == labelledString:
          print("Lip Makeup correct")
          lipMakeupAccuracy += 1
      else:
         print("Lip Makeup INCORRECT")
         
    
      print("\n")

      print("Eye Makeup")

      print("Actual {0}".format(labels[labelimage+7]))
      labelledString = str(labels[labelimage+7][11:-1])
      labelledString.strip()
      predictedString = str(data['faceAttributes']['makeup']['eyeMakeup'])
    #  print("PredictedString for eye makeup: {0}".format(predictedString))
      lipPrediction = " "
      if predictedString == "True":
          print("Eye Makeup is true")
          lipPrediction = "yes"
      else:
          print("Eye Makeup is false")
          lipPrediction = "no"

      if lipPrediction == labelledString:
          print("Eye Makeup correct")
          eyeMakeupAccuracy += 1
      else:
         print("Eye Makeup INCORRECT")
         
    
      print("\n")





      print("Hat")
      
      print("Actual {0}".format(labels[labelimage+9]))
      labelledString = str(labels[labelimage+9][5:-1])
      labelledString.strip()
      predictedString = str(data['faceAttributes']['accessories'])
      print("PredictedString for hat: {0}".format(predictedString))
      hatPrediction = " "
      if predictedString != "[]":
          print("Has an accessory on")
          print(str(data['faceAttributes']['accessories'][0]))
          print(str(data['faceAttributes']['accessories'][0]['type']))
          if str(data['faceAttributes']['accessories'][0]['type']) == "headwear": 
              print("Has hat on")
              hatPrediction = "yes"
          else:
              print("No hat on")
              hatPrediction = "no"

      else:
          print("No hat on")
          hatPrediction = "no"
          print(labelledString)
          print(hatPrediction)
      if hatPrediction == labelledString:
          print("Hat correct")
          hatAccuracy += 1
      else:
         print("Hat INCORRECT")

   
         
    
      print("\n")



     
      
      counter = counter + 1
      labelimage = counter * 10
    #  print("Counter: {0}".format(counter))
      #print("Label Image: {0}".format(labelimage))      
ageAccuracy = ageAccuracy / totalFacesCount
print("Age accuracy: {0}".format(ageAccuracy))       

genderAccuracy = genderAccuracy / totalFacesCount
print("Gender accuracy: {0}".format(genderAccuracy))

facialHairAccuracy = facialHairAccuracy / totalFacesCount
print("Facial Hair accuracy: {0}".format(facialHairAccuracy))

glassesAccuracy = glassesAccuracy / totalFacesCount
print("Glasses accuracy: {0}".format(glassesAccuracy))

hairAccuracy = hairAccuracy / totalFacesCount
print("Hair accuracy: {0}".format(hairAccuracy))

lipMakeupAccuracy = lipMakeupAccuracy / totalFacesCount
print("Lip Makeup accuracy: {0}".format(lipMakeupAccuracy))

eyeMakeupAccuracy = eyeMakeupAccuracy / totalFacesCount
print("Eye Makeup accuracy: {0}".format(eyeMakeupAccuracy))

hatAccuracy = hatAccuracy / totalFacesCount
print("Hat accuracy: {0}".format(hatAccuracy))

