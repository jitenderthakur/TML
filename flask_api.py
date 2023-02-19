
from mask_rcnn_ import mask_rcnn_module 
import configparser
from flask import Flask,request
import argparse
import cv2
import numpy as np
from keras import backend as K
from collections import Counter
import base64
import pandas as pd
from sqlalchemy import create_engine
from ConnectDb import push_into_db


config_Url = configparser.ConfigParser()
config_Url.read('config.ini')
image_save_path = config_Url["LOG Related"]["image_path"]
ip = config_Url["ip address"]["ip"]
port = config_Url["ip address"]["port"]

app = Flask(__name__)

mask_rcnn = mask_rcnn_module()

#Connection to DataBase and Engine Created.
db=push_into_db()

 
#flask api    
@app.route('/tml_upload', methods=["POST"])
def predict_tml_upload():
    if request.method =="POST":

        r=request
        img= r.json['image']
        timestamp=r.json['timestamp']
        count= r.json['generic_count']
        img_name= r.json['img_name']

        print(count)
        # convert string of image data to uint8
        jpg_original=base64.b64decode(img)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)
        print(img.shape)
#         print(count)
#         algo8_python_logger.info({"message": " Frames from upload folder Received"})
#         algo8_python_logger.info({"timestamp": timestamp,"count":count,"img_name":img_name})
   
#         algo8_python_logger.info({"message": "frames process into  model"})
        ycrcb_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb) # equalize the histogram of the Y channel
        ycrcb_img[:, :, 0] = cv2.equalizeHist(ycrcb_img[:, :, 0]) # convert back to RGB color-space from YCrCb
        equalized_img = cv2.cvtColor(ycrcb_img, cv2.COLOR_YCrCb2BGR)
        results = mask_rcnn.object_detect(equalized_img)
        print(results)
        #defect count
        defect= Counter(results['class_ids'])
        under_size=defect[1]
        over_size=defect[2]
        normal_size=16-(under_size+over_size)

        img_name=mask_rcnn.save_image(image_save_path)
        
        column_names=['timeStamp','ImageName','MoldCount','UnderSize','OverSize','NormalSize']
        values=[timestamp,img_name,count,under_size,over_size,normal_size]
        
        #push data into db
        try:
            db.run(column_names,values)
        except Exception as e:
            print(e)

#         algo8_python_logger.info({"message": " Data Successfully Pushed INTO DB"})
        
        K.clear_session()   
            
    return ''
    
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask api exposing mask-rcnn model")
    parser.add_argument("--port", default=port, type=int, help="port number")
    args = parser.parse_args()

      # force_reload = recache latest code
    app.run(host=ip, port=args.port,debug=True)

