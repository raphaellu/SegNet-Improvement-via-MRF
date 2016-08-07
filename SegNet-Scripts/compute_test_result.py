from PIL import Image
from math import sqrt
import os

# a dictionary contains all possible labels and their rgb values.
color_set = {"sky": (128,128,128), "building": (128,0,0), "pole" : (192,192,128), "road_marking":(255,69,0), "road" : (128,64,128), 
             "pavement":(60,40,222), "tree":(128,128,0), "signSymbol": (192,128,128), "fence":(64,64,128), "car":(64,0,128),
             "pedestrian": (64,64,0) , "bicyclist":(0, 128, 192), "unlabelled":(11,11,11)}

def select_match(x):
    """select the closest label for a (r,g,b) value
       PARAMETER(s)
            x: a rgb value in form of (R,G,B,A)
       RETURN
            a rgb value in form of (R,G,B)
       EXAMPLE
            input (128,126,129,255) will output (128,128,128)"""
    global color_set
    r = x[0]
    g = x[1]
    b = x[2]
    most_matched = ()
    min_v = 99999
    # calculates the distance of input rgb with any possible rgb
    # d = sqrt( (x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2 )
    for color in color_set:
        d = sqrt((r-color_set[color][0])**2 + (g-color_set[color][1])**2 + (b-color_set[color][2])**2)
        if min_v > d:
            min_v = d
            most_matched = color_set[color]
    return most_matched


def calculate_data(iter, gt_path, pred_path):
    """select the closest label for a (r,g,b) value
       PARAMETER(s)
            iter: the number of total images to calculate accuracy with
            gt_path: folder path of ground truth images
            pred_path: folder path of output images
       RETURN
            an array [global accuracy, class average accuracy, MIOU accuracy, 
                      class dictionary]
            (class dictionary is a dictionary containing all separate average 
            accuracy for each class)
       """

    ######## for calculating global accuracy #########
    total_px = 0   # total number of pixels
    correct_px = 0  # number of correctly predicted pixels 

    ######## for calculating class average accuracy #########
    c_total_px = {} # total number of pixels for each label
    c_correct_px = {}   # number correctly predicted pixels for each label (for class avg acc)

    ######## for calculating MIOU accuracy ########
    miu_total = {} 

    ######## iterating all images ########
    for i in range(0, iter): 
        gt_im = Image.open(gt_path + str(i) + ".png")
        pred_im = Image.open(pred_path + str(i) + ".png")
        gt_pix = gt_im.load()
        pred_pix = pred_im.load()
    
        (width, height) = gt_im.size
        for w in range(0, width):
            for h in range(0, height):
            gt_color = gt_pix[w,h]
            pred_color = pred_pix[w,h]
      
            if gt_color == pred_color:    
                if c_correct_px.get(gt_color) != None:
                    c_correct_px[gt_color] += 1       # count the correctly predicted pixel for each label 
                else:
                    c_correct_px[gt_color] = 1
                correct_px += 1       # count the correct predicted pixel for global acc
            else: # increase the miu_total pred_color counter 
                if miu_total.get(pred_color) != None:
                    miu_total[pred_color] += 1
                else:
                    miu_total[pred_color] = 1


            if c_total_px.get(gt_color) != None:
                c_total_px[gt_color] += 1       # count the total pixels for each color
            else:
                c_total_px[gt_color] = 1
            total_px += 1           # count the total pixels for global acc
        
            # count the MIOU total number of pixels for each label
            # if the color is predicted correctly, increase the total number by 1
            # otherwise both gt_color and pred_color counter will be increased by 1 (thus total by 2)
            # therefore, gt_color counter will be increased by 1 anyways, and pred_color counter will
            # only be increased if gt_color != pred_color
            if miu_total.get(gt_color) != None:
                miu_total[gt_color] += 1
            else:
                miu_total[gt_color] = 1

    class_num = 0
    class_acc_tot = 0
    miu_acc_tot = 0

    every_class = []
    # calculate the class average acc
    for color in c_total_px:
    class_ct = 0
    class_num += 1
    class_tot = c_total_px[color]    
    miu_tot = miu_total[color]

    if c_correct_px.get(color) != None :
        class_ct = c_correct_px[color]
    class_acc_tot += float(class_ct)/float(class_tot)
        every_class.append((color, float(class_ct)/ float(class_tot)))
        miu_acc_tot += float(class_ct)/float(miu_tot)
    
    for c in every_class:
    print str(c[0]) + " " + str(c[1])

    # print "Global acc = " + str(float(correct_px)/float(total_px)) + " Class average acc = " + str(float(class_acc_tot)/float(class_num)) + " Mean Int over Union = " + str(float(miu_acc_tot)/float(class_num))
    return [[(float(correct_px)/float(total_px)) , (float(class_acc_tot)/float(class_num)), (float(miu_acc_tot)/float(class_num))], every_class]

if __name__ == '__main__':
    calculate_data(233, 'gt/', 'predictions/')
    # calculate_data(233, 'gt/', 'before_opt/')
    # calculate_data(233, 'gt/', 'after_opt/')
