import os
import sys
import random
import math
import re
import time
import numpy as np
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from keras.backend import clear_session

from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log

import custom

def load_model():
    # Root directory of the project
    ROOT_DIR = os.path.abspath("")

    # Import Mask RCNN
    sys.path.append(ROOT_DIR)  # To find local version of the library
    # Directory to save logs and trained model
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")

    # You can download this file from the Releases page
    # https://github.com/matterport/Mask_RCNN/releases
    BALLON_WEIGHTS_PATH = "mrcnn/mask_rcnn_object_0010.h5"  # TODO: update this path

    config = custom.CustomConfig()
    CUSTOM_DIR = os.path.join(ROOT_DIR, "dataset")

    # changes for inferencing.
    class InferenceConfig(config.__class__):
        # Run detection on one image at a time
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1

    config = InferenceConfig()
    config.display()

    # Device to load the neural network on.
    # Useful if you're training a model on the same
    # machine, in which case use CPU and leave the
    # GPU for training.
    DEVICE = "/gpu:0"  # /cpu:0 or /gpu:0

    # Inspect the model in training or inference modes
    # values: 'inference' or 'training'
    # TODO: code for 'training' test mode not ready yet
    TEST_MODE = "inference"


    # Load validation dataset
    dataset = custom.CustomDataset()
    dataset.load_custom(CUSTOM_DIR, "val")

    # Must call before using the dataset
    dataset.prepare()

    print("Images: {}\nClasses: {}".format(len(dataset.image_ids), dataset.class_names))

    with tf.device(DEVICE):
        model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR,
                                  config=config)

    weights_path = "mrcnn/mask_rcnn_object_0010.h5"
    # Load weights
    print("Loading weights ", weights_path)
    model.load_weights(weights_path, by_name=True)
    return model,dataset,config

def get_ax(rows=1, cols=1, size=16):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.

    Adjust the size attribute to control how big to render images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size * cols, size * rows))
    return ax


def visualize_image(file_path,model,dataset,config):
    # image_id = random.choice(dataset.image_ids)
    # image, image_meta, gt_class_id, gt_bbox, gt_mask = \
    #     modellib.load_image_gt(dataset, config, image_id, use_mini_mask=False)
    # info = dataset.image_info[image_id]
    # print("image ID: {}.{} ({}) {}".format(info["source"], info["id"], image_id,
    #                                        dataset.image_reference(image_id)))
    #
    # # Run object detection
    # results = model.detect([image], verbose=1)
    #
    # # Display results
    # ax = get_ax(1)
    # r = results[0]
    # visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
    #                             dataset.class_names, r['scores'], ax=ax,
    #                             title="Predictions")
    # log("gt_class_id", gt_class_id)
    # log("gt_bbox", gt_bbox)
    # log("gt_mask", gt_mask)
    #
    # plt.savefig('random.jpg', bbox_inches='tight', pad_inches=-0.5, orientation='landscape')
    import matplotlib.image as mpimg
    image1 = mpimg.imread(file_path)
    # Run object detection
    print(len([image1]))
    results1 = model.detect([image1], verbose=1)

    # Display results
    ax = get_ax(1)
    r1 = results1[0]
    visualize.display_instances(image1, r1['rois'], r1['masks'], r1['class_ids'],
                                dataset.class_names, r1['scores'], ax=ax,
                                title="Predictions1")
    plt.savefig('b.jpg', bbox_inches='tight', pad_inches=-0.5, orientation='landscape')
    # clear_session()  # clears session to allow multiple images being processed