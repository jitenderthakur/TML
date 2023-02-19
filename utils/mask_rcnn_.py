from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from mrcnn.visualize import display_instances
from mrcnn.config import Config
from mrcnn.model import MaskRCNN
import configparser
import ast
import cv2
from datetime import datetime

# define the test configuration
class TestConfig(Config):
    """
    Configuration for Mask-rcnn
    GPU_COUNT : int
    NUM_CLASSES : int
    """
    config_Url = configparser.ConfigParser()
    config_Url.read('config.ini')
    NUM_CLASS = config_Url["Config"]["NUM_CLASSES"]
    NAME = "test"
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 1 + 2

class mask_rcnn_module:
    
    def object_detect(self,img):
        """
        Parameters 
        --------------
        img : np.ndarray
        -------------------
        Returns
        -------------------
        img : np.ndarray 
            With bboxes drawn on the image
        """
        
        config_Url = configparser.ConfigParser()
        config_Url.read('config.ini')
        WEIGHTS_PATH = config_Url["Config"]["WEIGHTS_PATH"]
        class_names = ast.literal_eval(config_Url.get("Config", "class_names"))
        print(class_names)
        # define the model
        rcnn = MaskRCNN(mode='inference', model_dir='./', config=TestConfig())
        # load coco model weights
        rcnn.load_weights(WEIGHTS_PATH, by_name=True)
        # load photograph
#         img = load_img(img)
#         img = img_to_array(img)
#         print("shape",img.shape)
        # make prediction
        results = rcnn.detect([img], verbose=0)
        # get dictionary for first prediction
        r = results[0]
#         print(r)
#         print("class_ids:",r['class_ids'])
#         print("class_names:",class_names)
        # show photo with bounding boxes, masks, class labels and scores
        output = display_instances(img, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])
#         print("output",output)
        self.current_frame = output
        return r
    #mask_rcnn('elephant.jpg') 
    def save_image(self, path=''):      
        if self.current_frame is not None: 
            now = datetime.now()
            current_time = str(now.strftime("%y_%m_%d_%H_%M_%S"))
            output_name=current_time+".jpg"
            cv2.imwrite(path+output_name, self.current_frame)
            return output_name
         
class Context:
    """
    # How to Use this Module
    # To Run this Module will have to follow following steps:
    # Steps 1:
        Import module (from mask_rcnn_ import mask_rcnn_module )

    # Step 2:
        Update the WEIGHTS_PATH ,class_names in config.ini file
        
    # step 3:
        Now load the images and call the function.

        Examples:
            path = glob.glob('/home/mukesh/Documents/algo8/Modules/model_inference/input/*')
            obj = mask_rcnn_module()
            while True:
                 for img in path:
                     obj.object_detect(img)
                     obj.save_image('/home/mukesh/Desktop/Scripts/')
                 break
    """
    
 
