# -*- coding: utf-8 -*-
"""
Created on Sun Apr 3 14:58:52 2022
@author: Mukesh Kumar
@ Description: Baumera Camera for grabbing images
"""
#from sap import upload_img_from_fold ,remove_img
from __future__ import print_function

import cv2

import json
import base64
#from PIL import Image

import numpy as np
import sys
import time
import os
import neoapi
import logging as lg
from datetime import datetime
import traceback
import time
import configparser
config_Url = configparser.ConfigParser()
config_Url.read('config.ini')
ip = config_Url["Setting"]["IP"]
exp = config_Url["Setting"]["Exposure"]
exp = int(exp)
logger = lg.basicConfig(filename = "log_files/"+"Log_"+str(datetime.now().date())+".log", 
                        level = lg.INFO, 
                        format = '%(asctime)s %(message)s')
algo8_python_logger = lg.getLogger()

algo8_python_logger.info({"message": "Baumera Camera Started"})
result = 0
class baumer_camera:
    def __init__(self):
        '''
        Initialize  cameras and define paths
        
        Returns
        -------
        None.
        '''
        try:
            #use neoapi to connect with camera
            algo8_python_logger.info({"message": "Use neoapi to connect with camera"})
            self.camera = neoapi.Cam()
            #camera ip address
            algo8_python_logger.info({"message": "camera IP Address"})
            self.camera.Connect(ip)  #"192.168.1.23"
            # camera.Connect()
            self.camera.f.ExposureTime.Set(exp)  #14000
            self.current_frame = None
            
        except (neoapi.NeoException, Exception) as exc:
            algo8_python_logger.error({"error": exc}) 
            print('error: ', exc)
            print("camera is not Connected")
            print(dir(self.camera))

    def grabImage(self,path=''):
        '''
        Raises
        ------
        Exception
            DESCRIPTION.
        '''               
                     
        # Grabbing the images and send it to api      
        if self.camera.IsConnected():     
            algo8_python_logger.info({"message": "Camera Start Grabbbing Images"})
                    
            t1 = time.time()
            img = self.camera.GetImage();
            if not img.IsEmpty():
                t2 = time.time()
                algo8_python_logger.info({"Time taken to read frame :":t2-t1})
                imgarray = img.GetNPArray() 
                self.current_frame = imgarray
                return  True, self.current_frame 
            else:
                return False, self.current_frame  
        else:

            algo8_python_logger.info({"message": "Camera is not Connected"})
            return False, None
    def save_image(self,path=''):
        if self.current_frame is not None:
            now = datetime.now()
            current_time = str(now.strftime("%y_%m_%d_%H_%M_%S"))
            algo8_python_logger.info({"message": "Saving Images"})
            cv2.imwrite(path+current_time+".jpg",self.current_frame)





# from baumer import baumer_camera
# from datetime import datetime
# obj = baumer_camera()
# while True:

#     ret,imgarray = obj.grabImage()
#     if ret:
#         print("images Received")
#         #print(imgarray)
#         now = datetime.now()
#         current_time = str(now.strftime("%y_%m_%d_%H_%M_%S"))
#         obj.save_image("C:\\Users\\MBFLOG\\Desktop\\Tml_images\\26_April_data\\")
#         print("image saved")
#     else:
#         print("image not found")
#         #break