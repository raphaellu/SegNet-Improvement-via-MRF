import numpy as np
import matplotlib.pyplot as plt
import os.path
import json
import scipy
import argparse
import math
import pylab
from sklearn.preprocessing import normalize
caffe_root = '/root/caffe-segnet/' 			# Change this to the absolute directoy to SegNet Caffe
import sys
sys.path.insert(0, caffe_root + 'python')

import caffe

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





# Import arguments
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=True)
parser.add_argument('--weights', type=str, required=True)
parser.add_argument('--iter', type=int, required=True)
args = parser.parse_args()

caffe.set_mode_gpu()
caffe.set_device(3)

net = caffe.Net(args.model,
                args.weights,
                caffe.TEST)


for i in range(0, args.iter):
	
	print i	
	net.forward()
	#for x in net.blobs:
 	#    print x 
	#    print net.blobs[x].data
	#    print "============="
	image = net.blobs['data'].data
	print dir(net.blobs['data'])
	label = net.blobs['label'].data
	
	predicted = net.blobs['prob'].data
	image = np.squeeze(image[0,:,:,:])
	output = np.squeeze(predicted[0,:,:,:])
	ind = np.argmax(output, axis=0)

	r = ind.copy()
	g = ind.copy()
	b = ind.copy()
	r_gt = label.copy()
	g_gt = label.copy()
	b_gt = label.copy()

	Sky = [128,128,128]
	Building = [128,0,0]
	Pole = [192,192,128]
	Road_marking = [255,69,0]
	Road = [128,64,128]
	Pavement = [60,40,222]
	Tree = [128,128,0]
	SignSymbol = [192,128,128]
	Fence = [64,64,128]
	Car = [64,0,128]
	Pedestrian = [64,64,0]
	Bicyclist = [0,128,192]
	Unlabelled = [0,0,0]

	label_colours = np.array([Sky, Building, Pole, Road, Pavement, Tree, SignSymbol, Fence, Car, Pedestrian, Bicyclist, Unlabelled])
	label_colours_rd = np.array([Sky, Building, Pole, Road_marking, Road, Pavement, Tree, SignSymbol, Fence, Car, Pedestrian, Bicyclist, Unlabelled])
	for l in range(0,11):
		r_gt[label==l] = label_colours[l,0]
		g_gt[label==l] = label_colours[l,1]
		b_gt[label==l] = label_colours[l,2]
	
	for l in range(0,12):
		r[ind==l] = label_colours_rd[l,0]
		g[ind==l] = label_colours_rd[l,1]
		b[ind==l] = label_colours_rd[l,2]
	
	rgb = np.zeros((ind.shape[0], ind.shape[1], 3))
	rgb[:,:,0] = r/255.0
	rgb[:,:,1] = g/255.0
	rgb[:,:,2] = b/255.0
	rgb_gt = np.zeros((ind.shape[0], ind.shape[1], 3))
	rgb_gt[:,:,0] = r_gt/255.0
	rgb_gt[:,:,1] = g_gt/255.0
	rgb_gt[:,:,2] = b_gt/255.0

	image = image/255.0

	image = np.transpose(image, (1,2,0))
	output = np.transpose(output, (1,2,0))
	image = image[:,:,(2,1,0)]

	plt.figure()	
	plt.imshow(rgb)

	plt.figure()
	plt.imshow(rgb_gt)
#	plt.show()        

	make_image(rgb_gt, "/home/data/dataset/SegNet/Scripts/gt_train/" + str(i))
	#make_image(rgb, "/home/data/dataset/SegNet/Scripts/predictions/" + str(i))


print 'Success!'

