import glob
import os.path
from datetime import datetime

import glob
import os.path
from datetime import datetime

def get_data(path):
    genericCounter=0
    try:
        file_type = '*.jpg'
        files = glob.glob(path + file_type)
        if files is not None:
            max_file = max(files, key=os.path.getctime)
            print(max_file)
            a = max_file.split('\\')
            print(a)
            s = a[-1].split('_')
            s1 = s[-1].split('.')
            genericCounter = int(s1[0])
        return  genericCounter
    except:
        return genericCounter

