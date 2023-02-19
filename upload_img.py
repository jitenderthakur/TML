import json
import re
import glob
import time
import os
import base64
import json
import cv2
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict
import requests
import numpy as np
import cv2
from datetime import datetime

        
def remove_img(path, img_name):
    # this fxn will remove the images from the folder   
    # check if file exists or not
    if os.path.exists(path + '/' + img_name) is True:
        os.remove(path + '/' + img_name)
        return True
    
def tml_img_detail(name_tml):
    name_tml=name_tml.split('_')
    now = str(datetime.now().year)
    name_tml[1]=now
    date=" ".join(str(x) for x in name_tml[1:4]).replace(' ','-')
    time= " ".join(str(x) for x in name_tml[4:7]).replace(' ',':')
    timestamp=date+' '+time
    count=int(name_tml[7].split('.')[0])
    return timestamp,count



def upload_tml_img(files_path,url,headers):
    # this fxn will upload the images from folder to the SAP
   
    """file_path: path where all the images are stored
    url: url of api
    headers = {'content-type' : image/jpeg}
    """
    
    name_list = os.listdir(files_path)
    
    full_list = [os.path.join(files_path,i) for i in name_list]
    
    # sort files according to datetime
    time_sorted_list = sorted(full_list, key=os.path.getmtime)

    # want just the filenames sorted, simply remove the dir from each
    sorted_filename_list = [ os.path.basename(i) for i in time_sorted_list]
    
    #reverse the list 
    files=list(reversed(sorted_filename_list))
    

    for path in files:

        if (str(path).endswith('png')) or (str(path).endswith('jpg')):
            path = files_path+'/'+path
            
            #storing image names
            image_names=path.split('/')[-1]
            #storing img in cv_img
            cv_img= cv2.imread(path)
            
        
        if len(cv_img)!=0:
            jpg_img = cv2.imencode('.jpg', cv_img)[1]
            #converting img to b64 format
            b64_string = base64.b64encode(jpg_img).decode('utf-8')

            #feteching data from image name
            timestamp,count=tml_img_detail(image_names)
            img_name=image_names
            print('---------------------uploading image ---------------------------------------')

            try:
    #             data={'count':count,'image':img_encoded}
    #             print(data)
                response = requests.request('POST',url,data=json.dumps({'timestamp':str(timestamp),
                                                                        'generic_count':str(count),
                                                                        'img_name':str(img_name),
                                                                        'image':b64_string}),headers=headers)
                print(response)

                #if frame is not saved 
                if response.status_code == 200:
                    print('y')
                    #delete the image from folder after uploading it 
                    remove_img(files_path,img_name)
            except requests.HTTPError as exception:
                print(exception)
                continue
        

#every after 15mins all the frames that are stored in folder will be uploaded on SAP
content_type = 'application/json'
headers = {'Content-Type' : content_type}


addr = 'http://localhost:5000'
tml_url = addr + '/tml_upload'

tml_files_path='C:/Users/HP/Desktop/Mukesh/tml_pipeline/img/'


#start the timer
start= time.perf_counter()
while True:
    if (time.perf_counter() -start)>1:
        print('uploading')
        #upload all the images from the folder 
        upload_tml_img(tml_files_path,tml_url,headers)
        print('done')
        #start the timmer again
        start= time.perf_counter() 
