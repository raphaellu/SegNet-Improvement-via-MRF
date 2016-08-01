import numpy as np
import os.path
import scipy
import argparse
import scipy.io as sio
import matplotlib
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.pyplot as plt
import cv2
import sys
# Make sure that caffe is on the python path:
caffe_root = '/root/caffe-segnet/' 			# Change this to the absolute directoy to SegNet Caffe
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
parser.add_argument('--colours', type=str, required=True)
parser.add_argument('--data', type=str, required=True)
args = parser.parse_args()

caffe.set_mode_gpu()
caffe.set_device(1)

net = caffe.Net(args.model,
                args.weights,
                caffe.TEST)

input_shape = net.blobs['data'].data.shape

label_colours = cv2.imread(args.colours).astype(np.uint8)
img_nu = 0;
with open(args.data) as f:
    for line in f:
        input_image_file, ground_truth_file = line.split()
	input_image_raw = caffe.io.load_image(input_image_file)
	ground_truth = cv2.imread(ground_truth_file, 0)

	input_image = caffe.io.resize_image(input_image_raw, (input_shape[2],input_shape[3]))
	input_image = input_image*255
	input_image = input_image.transpose((2,0,1))
	input_image = input_image[(2,1,0),:,:]
	input_image = np.asarray([input_image])
	input_image = np.repeat(input_image,input_shape[0],axis=0)

	out = net.forward_all(data=input_image)

	predicted = net.blobs['prob'].data

	output = np.mean(predicted,axis=0)
	uncertainty = np.var(predicted,axis=0)
	ind = np.argmax(output, axis=0)

	segmentation_ind_3ch = np.resize(ind,(3,input_shape[2],input_shape[3]))
	segmentation_ind_3ch = segmentation_ind_3ch.transpose(1,2,0).astype(np.uint8)
	segmentation_rgb = np.zeros(segmentation_ind_3ch.shape, dtype=np.uint8)

	gt_ind_3ch = np.resize(ground_truth,(3,input_shape[2],input_shape[3]))
	gt_ind_3ch = gt_ind_3ch.transpose(1,2,0).astype(np.uint8)
	gt_rgb = np.zeros(gt_ind_3ch.shape, dtype=np.uint8)

	cv2.LUT(segmentation_ind_3ch,label_colours,segmentation_rgb)
	cv2.LUT(gt_ind_3ch,label_colours,gt_rgb)
	
	uncertainty = np.transpose(uncertainty, (1,2,0))
	#print uncertainty
	#print uncertainty.shape[0]
	#print uncertainty.shape[1]
	#print uncertainty.shape[2]


	average_unc = np.mean(uncertainty,axis=2)
	#print average_unc
	#print uncertainty.shape[0]
	#print uncertainty.shape[1]
	#print uncertainty.shape[2]
	min_average_unc = np.min(average_unc)
	max_average_unc = np.max(average_unc)
	max_unc = np.max(uncertainty)
	#"""
	plt.imshow(input_image_raw,vmin=0, vmax=255)
	plt.figure()
	plt.imshow(segmentation_rgb,vmin=0, vmax=255)
	plt.figure()
	plt.imshow(gt_rgb,vmin=0, vmax=255)
	plt.set_cmap('bone_r')
	plt.figure()
	plt.imshow(average_unc,vmin=0, vmax=max_average_unc)
	plt.show()
	#"""
        #make_image(segmentation_rgb, "predictions/" + str(img_nu) + ".png")  
	plt.set_cmap('bone_r')
        #make_image(average_unc, "uncertainty/" + str(img_nu) + ".png")  

        img_nu += 1
	# uncomment to save results
	#scipy.misc.toimage(segmentation_rgb, cmin=0.0, cmax=255.0).save(IMAGE_FILE+'_segnet_segmentation.png')
	#cm = matplotlib.pyplot.get_cmap('bone_r') 
	#matplotlib.image.imsave(input_image_file+'_segnet_uncertainty.png',average_unc,cmap=cm, vmin=0, vmax=max_average_unc)

	print 'Processed: ', input_image_file

print 'Success!'

