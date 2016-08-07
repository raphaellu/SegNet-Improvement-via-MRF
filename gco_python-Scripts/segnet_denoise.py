from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from pygco import cut_simple, cut_from_graph
from math import *
import sys
from data import pairwise_relation 

sys.path.append('/home/data/dataset/SegNet/Scripts/') # modify the SegNet path accordingly

from compute_test_result import calculate_data 

# for generating pairwise potentials weights table
# dictionary key is rgb value of the label 
# dictionary value is the index of that label in the table
color_set = {
str([128,64,128]) : 0, 
str([128,0,0]) : 1, 
str([192,192,128]) : 2, 
str([128,128,128]) : 3, 
str([60,40,222]) : 4, 
str([128,128,0]) : 5, 
str([192,128,128]) : 6, 
str([64,64,128]) : 7, 
str([64,0,128]) : 8,
str([64,64,0]) : 9, 
str([0, 128, 192]) : 10 
}

# a reversed version of color_set
color_set_str = {
"0": [128,64,128], 
"1": [128,0,0], 
"2" : [192,192,128], 
"3" : [128,128,128], 
"4" : [60,40,222], 
"5" : [128,128,0], 
"6" : [192,128,128], 
"7" : [64,64,128], 
"8" : [64,0,128],
"9" : [64,64,0], 
"10" : [0, 128, 192]
}

# 1 - turn on optimization; 0 - turn off optimization
unaries_opt = 0     
pairwise_opt = 1

def select_match(x, unc_w):
    """takes in a RGB value and returns an array of potentials for that pixel
       PARAMETER(s):
          x : a rgb value in the form of (R,G,B,A)
          unc_w : uncertainty weight
       RETURN:
          res : an array of potentials for one pixel
              eg. if the pixel is labeled as sky (rgb value is [128,128,128]), its
                  potential array (unoptimized) is [0.0, 0.0, 0.0, 10.0, 0.0, 0.0, 0.0,
                  0.0, 0.0, 0.0, 0.0] - the index representing 'sky' has value of 10.0 
                  and all other indexes have values of 0.0
            """
    global unaries_opt, color_set
    r = x[0]
    g = x[1]
    b = x[2]
    most_matched = color_set[str([r,g,b])]
    res = [0.0 for x in range(0, 11)]
    if unaries_opt == 1 :  # check if unary opt flag is on
        res[most_matched] =  10. + 10. * unc_w 
    else:
        res[most_matched] = 10.
    return res

def compute_unaries(img_pred, img_uncert):
    """compute unary potentials
       PARAMETER(s):
          img_pre : numpy array of prediction image's pixels
          img_uncert : numpy array of uncertainty image's pixels (grayscaled)
       RETURN:
          unaries : unary potentials matrix for the whole image"""
    unaries = np.resize(img_pred, (img_pred.shape[0], img_pred.shape[1], 11))
    for x in xrange(img_pred.shape[0]):
        for y in xrange(img_pred.shape[1]):
            unc = img_uncert[x][y] # grayscale intensity, ranging from 0 to 255
            unc_w = unc/255.
            res =  select_match(img_pred[x][y], unc_w)
            unaries[x][y] = res
    return unaries

def correct_color(o_res):
    """convert form [R,G,B] to [R,G,B, 255] for data processing
       PARAMETER(s):
          o_res : a matrix (numpy array) where each element contains only 1 integer (label number)
                  eg. sky is 3, tree is 5.
       RETURN:
          n_res : a new matrix (numpy array) where each element is a rgb value in the form of 
                  [R,G,B,255]
    """
    global color_set
    n_res = np.zeros((o_res.shape[0], o_res.shape[1], 4))
    for x in xrange(o_res.shape[0]):
        for y in xrange(o_res.shape[1]):
            n_res[x][y] = color_set_str[str(o_res[x][y])] + [255] 
    return n_res

def img_denoise(unaries_weight, pairwise_weight, img_nu):
    """apply MRF filter on top of CNN outputs
       PARAMETER(s):
          unaries_weight: unary potentials weight (recommended: 800)
          pairwise_weight: pairwise potentials weight (recommended: -1000)
          img_nu: the image to process. (All test images are named as <int>.png,
                  refer to function "compute_all" to see how img_nu is used) 
       RETURN:
          no return value
    """
    img_prediction = np.asarray(Image.open("before_opt/"+ str(img_nu)  + ".png"))
    # open uncertainty image and grayscale it
    img_uncertain = np.asarray(Image.open("uncertainty/" + str(img_nu) + ".png").convert('L'))

    unaries = (10000* unaries_weight * (compute_unaries(img_prediction, img_uncertain) / -10.)).astype(np.int32)
    pairwise = np.eye(unaries.shape[2])*10000 * pairwise_weight
   
    # pairwise potentials matrix optimization, if its optimization is turned on.
    if pairwise_opt == 1: 
        for h in range(0, pairwise.shape[0]):
            for w in range(0, pairwise.shape[1]):
                if h == w:
                    base = pairwise[h][w]
            for w in range(0, pairwise.shape[1]):
                # pairwise_relation is the pairwise potentials weights table imported from data.py
                pairwise[h][w] = base * pairwise_relation[h][w]              
    pairwise = pairwise.astype(np.int32)

    ###### cut_simple is from gco_python library. It is the main logic of applying MRF 
    # simply pass in unary potentials matrix and pairwise potentials matrix to use this function
    ######
    result = cut_simple(unaries, pairwise) 
    result = correct_color(result).astype(np.uint8)   # converts label number into RGB value

    # display images before and after optimization 
    """
    plt.subplot(121, xticks=(), yticks=())
    plt.imshow(img_prediction, interpolation='nearest')
    plt.subplot(122, xticks=(), yticks=())
    plt.imshow(result, interpolation='nearest')
    plt.show()
    """
    make_image(result, "after_opt/" + str(img_nu) + ".png") # save optimized images

def make_image(data,outputname):
    """takes in a numpy array and a file path, saves as an image
       PARAMETER(s):
          data : a numpy array of pixels for an image
          outputname : output file path 
       RETURN:
          no return value
    """
    fig = plt.figure()
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(data, aspect = 'normal')
    plt.savefig(outputname, dpi = 75)

def compute_all(iter, unaries_weight, pairwise_weight):
    """integrates all methods together: denosies each image; calculates global accuracy,
       class avg accuracy and MIOU accuracy; calculates the accuracy improvements
       PARAMETER(s):
          iter : total number of images to process
          unaries_weight: unary potentials weight (recommended: 800)
          pairwise_weight: pairwise potentials weight (recommended: -1000)
       RETURN:
          no return value
    """
    for i in range(0, iter):
        print (str(1+i) + "/" + str(iter))
        img_denoise(unaries_weight, pairwise_weight, i)
    before = calculate_data(iter, "gt/", "before_opt/")
    after = calculate_data(iter, "gt/", "after_opt/")
    # print a string in the form of "<iter> <unary weight> <pairwise weight> <global accuracy improvment> <class average accuracy improvement> <MIOU accuracy improvement>
    print (str(iter) + " "  + str(unaries_weight) + " " + str(pairwise_weight) + " " + str(after[0][0] - before[0][0]) + " " + str(after[0][1] - before[0][1]) + " " + str(after[0][2] - before[0][2]))

# compute_all(233, 800, -1000) 
