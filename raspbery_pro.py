# importing laibrary
import cv2 
import face_recognition as fr 
import numpy as np 
import os 
import RPi.GPIO as GPIO 
import time


#################################################
#connect servo to raspbery py gpio pin numer3
servoPIN = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50) 
p.start(2)
##################################################


##################################################
#reading image from folder and read names in imgas
path = "/home/pi/Downloads/New"
images = []
classNmes = []
myList = os.listdir(path)
for cl in myList:
    cur = cv2.imread(f'{path}/{cl}')
    images.append(cur)
    classNmes.append(os.path.splitext(cl)[0])
print(classNmes)
###################################################


###################################################
#give our image to face_recogntion model to encoded theim
def finden(images):
    encodelist =[]
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodE = fr.face_encodings(img)[0]
        encodelist.append(encodE)
    return encodelist
####################################################    


####################################################
#encodeing image in the data
encodel = finden(images)
print("encoding is complite")
#####################################################


#####################################################
#open the camera
cap = cv2.VideoCapture(0)
while True:
    suc ,img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
######################################################


######################################################
#use face_recognation model to recognaize the face in the camera
    fasescur = fr.face_locations(imgS)
    encodecur = fr.face_encodings(imgS,fasescur)
#######################################################


#######################################################
#compre the face that located in the camera with face in the data
    for encodedf,faceloc in zip(encodecur,fasescur):
        mathis=fr.compare_faces(encodel,encodedf)
        facedis=fr.face_distance(encodel,encodedf)
        print(facedis)
        mathiindex= np.argmin(facedis)
#######################################################        


######################################################
#make servo move 90 dgree when camera recoginze the face        
        for i in facedis:
            if .6 > i > .4:
                print("unlocked")
                p.ChangeDutyCycle(7)
                time.sleep(10)
                p.ChangeDutyCycle(2)
                time.sleep(.5)
                p.stop()
                GPIO.cleanup()
######################################################                    
            

######################################################
#print the name of face that recognaized
        if mathis[mathiindex]:
            name = classNmes[mathiindex].upper()
            print (name)
#####################################################


#####################################################
#draw rectngle on the face in the camera
            y1,x2,y2,x1 = faceloc
            y1, x2, y2, x1 =y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
######################################################


######################################################            
#show window and break it
    cv2.imshow("wepcam",img)
    if cv2.waitKey(1)==ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
#######################################################    



