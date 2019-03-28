import keras
import pickle
from videotest import VideoTest

import sys
sys.path.append("..")
from ssd import SSD300 as SSD

input_shape = (300,300,3)

# Change this if you run with other classes than VOC
# class_names = ["background", "beansprouts", "carrot", "daikon", "enoki", "greenpepper", "shimeji"];
class_names = ["background", "Asparagus", "Apple", "Broccoli", "Beansprouts", "Beaf", "Celery", "Carrot", "Cabbage", "Cucumber", "Chicken", "Daikon", "Egg", "Enoki", "Firefly_Squid", "Greenpepper", "Leek", "Milk", "Mushroom", "Onion", "Pumpkin", "Orange", "Pork", "Paprika", "Spinach", "Shimeji", "Squid", "Tomato", "Shimeji", "Turnip", "Ume"];
NUM_CLASSES = len(class_names)

model = SSD(input_shape, num_classes=NUM_CLASSES)

# Change this path if you want to use your own trained weights
model.load_weights('..\checkpoints\weights.29-6.89.hdf5') 
        
vid_test = VideoTest(class_names, model, input_shape)

# To test on webcam 0, remove the parameter (or change it to another number
# to test on that webcam)
# vid_test.run(0)
vid_test.run('C:\\Users\\eisuke takahashi\\Desktop\\VID_20190310_230824.mp4')

