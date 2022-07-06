################ Henri Lahousse ################
# face id, recognize face, detect emotion
# 05/31/2022

# libraries
from deepface import DeepFace      # for face recognision !! NEEDS AT LEAST TENSORFLOW 1.9 !!
import cv2                         
import names
import numpy as np
from picamera import PiCamera     
from datetime import datetime      

camera = PiCamera()

database = []  # database, contains list of faces
em = ["angry", "disgust", "fear", "happy", "sad", "suprised", "neutral"] # list emotion that are detectable

def take_pic():                                                       
    now = datetime.now()                                               # actual time

    img = camera.capture(r'DIR\image{}.jpg'.format(now))               # link actual time with taken picture
    return img

def fi():
    while True:
        image = take_pic()                                             # takes a picture
        analys = DeepFace.analyze(image, actions=['emotion'])          # analyses photo on emotions (possibilities: age, gender, race, emotion)

        value = list(analys['emotion'].values())                       # value emotion
        maxi = max(list(value))                                        # highest detected emotion

        emo_hgh = [i for i, j in enumerate(value) if j == maxi]        # searches highest value

        p = 0                                                          # randem letter for loop
        while p < len(em):                                             # while p is smaller than the lenght of the list
            if emo_hgh[0] == p:                                        
                print("host is ", em[p])                               # print state host
            p += 1

        res = []

        def face_id(db, pic):                                          # authtenticating user
            id = DeepFace.verify(db, pic)                              # vergelijkt een foto uit de database en een nieuwe foto

            result = str(id)                                           

            if "True" in result:                                       # if True is somewhere in the text
                res.append(1)                                          # append list with 1

            else:                                                      
                res.append(0)                                          # append list with 0

        len_db = len(database)                                         
        n = 0                                                          # randem letter
        while n < len_db:                                              # while n is smaller then len_db
            face_id(database[n], image)                                # stays cheching image with database
            n += 1                                                     

        print("database matches: ", res)

        if all(v == 0 for v in res):                                   # if there is no result 
            rand_name = names.get_full_name()                          # generates randem name
            print("vindt geen match --> genereert naam: ", rand_name)
            rand_name = image                                          # adds randem name and image to database
            database.append(rand_name)
            #print(rand_name)


fi()
