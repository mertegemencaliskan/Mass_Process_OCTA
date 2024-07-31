import cv2
import numpy as np
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image 
import sys 
import os 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors


import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
def show_n_images(imgs,  titles = None, enlarge = 5, cmap = None):
    
    if (cmap != None):
        plt.set_cmap(cmap);
    
    n = len(imgs);
    gs1 = gridspec.GridSpec(1, n);
    
    fig1 = plt.figure(figsize=(8*len(imgs),8));
    for i in range(n):

        ax1 = fig1.add_subplot(gs1[i]);

        ax1.imshow(imgs[i], interpolation='none');
        if (titles is not None):
            ax1.set_title(titles[i], fontsize=25)

    plt.show();


import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
def show_n_images_ver(imgs,  titles = None, enlarge = 5, cmap = None):
    
    if (cmap != None):
        plt.set_cmap(cmap);
    
    n = len(imgs);
    gs1 = gridspec.GridSpec(n,1);
    
    fig1 = plt.figure(figsize=(8*len(imgs),8)); 

    for i in range(n):

        ax1 = fig1.add_subplot(gs1[i]);

        ax1.imshow(imgs[i], interpolation='none');
        if (titles is not None):
            ax1.set_title(titles[i], fontsize=25)
    plt.tight_layout()
    plt.show();

im = plt.imread('/Users/mertegemencaliskan/Downloads/Screenshot 2024-04-22 at 9.57.00 PM.png')

hsv_im = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)
lower_blue = np.array([78, 50, 100])
upper_blue = np.array([100, 255, 230])
mask = cv2.inRange(hsv_im, lower_blue, upper_blue)
res = cv2.bitwise_and(im,im,mask)
mask3 = np.repeat(mask[:,:,np.newaxis], 4, axis=2)/255
masked_im = im*mask3/255.
show_n_images([res[20:80,100:300], masked_im[20:80,100:300]])