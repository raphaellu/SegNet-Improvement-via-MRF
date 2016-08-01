from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from pygco import cut_simple, cut_from_graph
from math import *
import sys
from data import pairwise_relation 

sys.path.append('/home/data/dataset/SegNet/Scripts/')

from compute_test_result import calculate_data 


#color_set = {"sky": (128,128,128), "building": (128,0,0), "pole" : (192,192,128), "road_marking":(255,69,0), "road" : (128,64,128), 
#            "pavement":(60,40,222), "tree":(128,128,0), "signSymbol": (192,128,128), "fence":(64,64,128), "car":(64,0,128),
#            "pedestrian": (64,64,0) , "bicyclist":(0, 128, 192), "unlabelled":(0,0,0) }

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


unaries_opt = 0
pairwise_opt = 0

def select_match(x, unc_w):
    global unaries_opt
    """select the most matched label for a (r,g,b) value"""
    global color_set
    r = x[0]
    g = x[1]
    b = x[2]
    #if str([r,g,b]) == str([255,69,0]):
	#print " asdasdasdasd"
    most_matched = color_set[str([r,g,b])]
    """
    min_v = 99999
    for color in color_set:
        d = sqrt((r-color_set[color][0])**2 + (g-color_set[color][1])**2 + (b-color_set[color][2])**2)
        if min_v > d:
            min_v = d
            most_matched = color
    """
    res = [0.0 for x in range(0, 11)]
    if unaries_opt == 1 : 
        res[most_matched] =  10. + 10. * unc_w 
    else:
        res[most_matched] = 10.
    #if most_matched == 2:
    #	res[most_matched] = 100.
    return res

def compute_unaries(img_pred, img_uncert):
    
    unaries = np.resize(img_pred, (img_pred.shape[0], img_pred.shape[1], 11))
    for x in xrange(img_pred.shape[0]):
	for y in xrange(img_pred.shape[1]):
	    unc = img_uncert[x][y]
	    unc_w = (unc[0]/3.+ unc[1]/3.+ unc[2]/3.) /255.
	    res =  select_match(img_pred[x][y], unc_w)
            unaries[x][y] = res
            #print res
    #print unaries
    return unaries

def correct_color(o_res):
    global color_set
    n_res = np.zeros((o_res.shape[0], o_res.shape[1], 4))
    for x in xrange(o_res.shape[0]):
        for y in xrange(o_res.shape[1]):
            n_res[x][y] = color_set_str[str(o_res[x][y])] + [255] 
    return n_res

def img_denoise(unaries_weight, pairwise_weight, img_nu):
    img_prediction = np.asarray(Image.open("before_opt/"+ str(img_nu)  + ".png"))
    img_uncertain = np.asarray(Image.open("uncertainty/" + str(img_nu) + ".png"))
 
    unaries = (10000* unaries_weight * (compute_unaries(img_prediction, img_uncertain) / -10.)).astype(np.int32)
    #print unaries
    pairwise = np.eye(unaries.shape[2])*10000
	

    pairwise = (pairwise_weight * pairwise)
    if pairwise_opt == 1:
        for h in range(0, pairwise.shape[0]):
            for w in range(0, pairwise.shape[1]):
                if h == w:
                    base = pairwise[h][w]
            for w in range(0, pairwise.shape[1]):
                pairwise[h][w] = base * pairwise_relation[h][w]
    pairwise = pairwise.astype(np.int32)
    #print pairwise
    result = cut_simple(unaries, pairwise)
    #print result
    result = correct_color(result).astype(np.uint8)
    #"""
    plt.subplot(121, xticks=(), yticks=())
    plt.imshow(img_prediction, interpolation='nearest')
    plt.subplot(122, xticks=(), yticks=())
    plt.imshow(result, interpolation='nearest')
    plt.show()
    #"""
    make_image(result, "after_opt/" + str(img_nu) + ".png")

def make_image(data,outputname):
    	# data = mpimg.imread(inputname)[:,:,0]
    	#data = np.arange(1,10).reshape((3, 3))
    	fig = plt.figure()
    	#fig.set_size_inches(1, 1)
    	ax = plt.Axes(fig, [0., 0., 1., 1.])
    	ax.set_axis_off()
    	fig.add_axes(ax)
    	#plt.set_cmap('hot')
    	ax.imshow(data, aspect = 'normal')
    	plt.savefig(outputname, dpi = 75)

def compute_all(iter, unaries_weight, pairwise_weight):
    for i in range(0, iter):
        print (str(1+i) + "/" + str(iter))
    	img_denoise(unaries_weight, pairwise_weight, i)
    before = calculate_data(iter, "gt/", "before_opt/")
    after = calculate_data(iter, "gt/", "after_opt/")
    print (str(iter) + " "  + str(unaries_weight) + " " + str(pairwise_weight) + " " + str(after[0][0] - before[0][0]) + " " + str(after[0][1] - before[0][1]) + " " + str(after[0][2] - before[0][2]))
    for i in range(0, len(after[1])):
	print (str(before[1][i][0]) + " " + str(before[1][i][1])) 	
	print (str(after[1][i][0]) + " " + str(after[1][i][1]))   	


#a = 500
#while ( a< 2000) : 
#    compute_all(3, a, -1000)
#    a += 50

compute_all(1, 800, -1000) 
pairwise_opt = 1
compute_all(1, 800, -1000) 
#compute_all(5, 750, -1000) 

#pairwise_opt = 0
#a = 500
#while ( a< 2000) : 
#    compute_all(233, a, -1000)
#    a += 50

#compute_all(3, 5, -10)
#compute_all(1, 10, -8)
#pairwise_opt = 0
#compute_all(1, 10, -8)
#compute_all(3, 10, -12)

#compute_all(5, 10, -15)
#unaries_opt = 1
#compute_all(5, 10, -15)
