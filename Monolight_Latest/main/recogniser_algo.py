from concurrent.futures import thread
import PIL
from cv2 import threshold
from main.models import UserProfile
from django.contrib.auth.models import User
import dlib
import cv2 as cv
import numpy as np
import urllib
# For downloading file
# import os
# import bz2
# import gdown

# Downloading file if doesn't exist
# def unzip_bz2_file(zipped_file_name):
#     zipfile = bz2.BZ2File(zipped_file_name)
#     data = zipfile.read()
#     newfilepath = data[:-4] #discard .bz2 extension
#     open(newfilepath, 'wb').write(data)
 
# def download_file(url):
#     output = url.split("/")[-1]
#     gdown.download(url, output, quiet=False)
 
# if os.path.isfile('shape_predictor_5_face_landmarks.dat') != True:
#     print("shape_predictor_5_face_landmarks.dat is going to be downloaded")
#     url = "http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2"
#     output = download_file(url)
#     unzip_bz2_file(output)
 
# if os.path.isfile('dlib_face_recognition_resnet_model_v1.dat') != True:
#     print("dlib_face_recognition_resnet_model_v1.dat is going to be downloaded")
#     url = "http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2"
#     output = download_file(url)
#     unzip_bz2_file(output)


detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")


# def recognizer(to_match, orignal_url):

#     response = urllib.request.urlopen(to_match)

#     with open('./media/temp/image.jpg', 'wb') as f:
#         f.write(response.file.read())

#     img1 = dlib.load_rgb_image("./media/temp/image.jpg")
#     #img2 = dlib.load_rgb_image(f"./media/temp/image.jpg")
#     img2 = dlib.load_rgb_image(f"./{str(orignal_url)}")

#     # Detection
#     img1_detection = detector(img1, 1)
#     img2_detection = detector(img2, 1)
#     print(f'image1_dete {img1_detection}')
#     print(f'image2_dete {img2_detection}')
#     try:
#         img1_shape = sp(img1, img1_detection[0])
#         img2_shape = sp(img2, img2_detection[0])
#     except:
#         return False
#     print(f'image1_dete {img1_shape}')
#     # Alignment
#     img1_aligned = dlib.get_face_chip(img1, img1_shape)
#     img2_aligned = dlib.get_face_chip(img2, img2_shape)

#     img1_rep = np.array(facerec.compute_face_descriptor(img1_aligned))
#     img2_rep = np.array(facerec.compute_face_descriptor(img2_aligned))
#     distance = findEuclideanDistance(img1_rep, img2_rep)
#     threshold = 0.6 
#     if distance < threshold: return True
#     else: return False

def get_distance(orignal_url):
    img2 = dlib.load_rgb_image(f"./{str(orignal_url)}")
    img2_detection = detector(img2, 1)
    img2_shape = sp(img2, img2_detection[0])
    img2_aligned = dlib.get_face_chip(img2, img2_shape)
    img2_rep = np.array(facerec.compute_face_descriptor(img2_aligned))
    return img2_rep

def recognizer():

    img1 = dlib.load_rgb_image("./media/temp/image.jpg")
    #img2 = dlib.load_rgb_image(f"./media/temp/image.jpg")

    # Detection
    img1_detection = detector(img1, 1)
    # print(f'image1_dete {img1_detection}')
    # print(f'image2_dete {img2_detection}')
    try:
        img1_shape = sp(img1, img1_detection[0])
    except:
        return False
    # print(f'image1_dete {img1_shape}')
    # Alignment
    img1_aligned = dlib.get_face_chip(img1, img1_shape)
    img1_rep = np.array(facerec.compute_face_descriptor(img1_aligned))

    all_users = UserProfile.objects.all()
    i = 0
    threshold = {}
    for _user in all_users:
        img2_rep = get_distance(_user.image.url)
        threshold[i] = findEuclideanDistance(img1_rep, img2_rep)
        i += 1
        # threshold = 0.6
        # if distance < threshold: 
        #     return _user
    
    minVal = min(threshold.values())
    idx, *_ = [key for key in threshold.keys() if threshold[key] == minVal] 
    if minVal < 0.5:
        return all_users[idx]
    return False


def findEuclideanDistance(s_rep, t_rep):
    euclidean_distance = s_rep - t_rep
    euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
    euclidean_distance = np.sqrt(euclidean_distance)
    return euclidean_distance


