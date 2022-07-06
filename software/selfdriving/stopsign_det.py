import cv2
from cam import dl, pic


def stp(pic):
   img = cv2.imread(pic)
   #img_gray = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)   
   img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


   stop_data = cv2.CascadeClassifier('/home/pi/Documents/stop_data.xml')

   found = stop_data.detectMultiScale(img_gray, minSize=(20, 20))

   amount_found = len(found)
     
   dl()

   return amount_found

def safe():
    pic()
    return stp("stop.jpg")

safe()
#print(safe())
