#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 16 18:52:51 2022

@author: mukesh
"""

import configparser
from PIL import Image
from os import path as Path
from datetime import datetime
import config_log as cf
#config_Url = configparser.ConfigParser()
#config_Url.read('config.ini')
#path = config_Url["LOG Related"]["LOG_FILE_PATH"]

#def save_image(self,img, path=''):
#    
#    '''
#    saving the
#    images into given path
#    
#    Parameters
#    -----------------
#    img : np.array
#    path: img path to save
#    ...............
#    Return 
#    ---------------------
#    None
#    '''
#    img = None
#    if img is not None:
#        now = datetime.now()
#        current_time = str(now.strftime("%y_%m_%d_%H_%M_%S"))
#        cv2.imwrite(path + current_time + ".jpg",img)
#        cf.success_log(200, "Images Saved At Given Path", "yolov4", path)
        
        
        
        
        
        
config_Url = configparser.ConfigParser()
config_Url.read('config.ini')
image_path = config_Url["LOG Related"]["image_path"] 
path = config_Url["LOG Related"]["LOG_FILE_PATH"]      
def compile_all_thread(img):
    cf.success_log(200, "thread started on {}".format(str(datetime.now())), "threadthis.compile_all_thread",path)
    pth_defect = image_path
    now = datetime.now()
    current_time = str(now.strftime("%y_%m_%d_%H_%M_%S"))
    image_pth = Path.join(pth_defect,current_time+".jpg")
    #color_coverted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    color_coverted = img
    cf.success_log(200, "image color conversion done", "threadthis.compile_all_thread",path)
    pil_image = Image.fromarray(color_coverted)
    cf.success_log(200, "cv2 image converted to pillow image", "threadthis.compile_all_thread",path)
    pil_image.save(image_pth,quality=20)
    
    
    
