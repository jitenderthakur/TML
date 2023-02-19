
from baumer_module import baumer_camera
from datetime import datetime
import configparser

import cv2
from report_creation import one_hr_df_pdf
import numpy as np

import logging as lg

from datetime import datetime
from hist_data_img import get_data

# from mail_service import mail_camera_status
logger = lg.basicConfig(filename = "log_files/"+"Log_tml"+str(datetime.now().date())+".log", 
                        level = lg.INFO, 
                        format = '%(asctime)s %(message)s')
algo8_python_logger = lg.getLogger()


#config_Url = configparser.ConfigParser()
#config_Url.read('config.ini')
#ip = config_Url["Setting"]["IP"]
#exp = config_Url["Setting"]["Exposure"]
#exp = int(exp)
#obj = baumer_camera(ip,exp)

obj = baumer_camera()



first_event=True
prev_day=''

path = 'C:\\Users\\HP\\Desktop\\Mukesh\\tml_pipeline\\img\\*'
genericCounter = get_data(path)

report=True
frame_count=0
while True:

    ret,imgarray = obj.grabImage()
    
    if ret:
        print("images Received")
        
        frame_count=0
        #print(imgarray)
        algo8_python_logger.info({"message": "image Received"})
 
        
        now = datetime.now()
        current_time = str(now.strftime("%y_%m_%d_%H_%M_%S"))
        current_day = now.day
        
        if first_event == True:
            print("First event identified!")
            algo8_python_logger.info({"message": "First event identified!"})
            prev_day = current_day
            first_event = False
        
        if current_day != prev_day:
            genericCounter = 0
            prev_day=current_day
        
        if report==True:
            report_time = datetime.now()
            report=False
            
            
            
        genericCounter+=1
        
        cv2.imwrite('C:\\Users\\HP\\Desktop\\Mukesh\\tml_pipeline\\img\\tml_'+current_time+'_'+str(genericCounter)+".jpg",imgarray)
        print("image saved")
        
        algo8_python_logger.info({"message": "saved image in folder"})
     
    else:
        print("image not found")
        frame_count=+1
       
        
        if report==False and frame_count>250:
            #run the report
            print('report creation started')
            try:
                algo8_python_logger.info({"message": "report creation started"})
                one_hr_df_pdf(report_time)
                algo8_python_logger.info({"message": "report creation completed"})
                report=True
            
            except Exception as e:
                print(e)
                algo8_python_logger.info({"error": e})
                
                
            
            
        