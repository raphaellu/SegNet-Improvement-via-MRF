# SegNet-Improvement-via-MRF

##Explanation
This repository only serves as a storage for all customized scripts I wrote during my research.

Note that file paths in this repository do not match the actual paths they are in use. Download [this SegNet repository](https://github.com/alexgkendall/SegNet-Tutorial) for original codes.

Refer to inline comments in files for more details. 

##Dependencies 
The following dependencies are required to run pre-configured docker image (remote access):

* X-11
* docker

To remotely access the computer with GPU support, __enable X forwarding first__, then
use this docker image by using the following command: `nvidia-docker run -it --net=host --rm -e DISPLAY=$DISPLAY -v "$HOME/.Xauthority:/root/.Xauthority:rw" yasumat/caffe-segnet:cython /bin/bash`

Other dependencies:

* [SegNet](https://github.com/alexgkendall/SegNet-Tutorial) 
* [gco_python](https://github.com/amueller/gco_python)

##Documentation:
`report_v3.1.pdf`: Report of this research. Not completed yet but should be informative enough.

###Main files that may be reused:
1.`SegNet-Scripts/compute_test_result.py`: calculates global accuracy, class average accuracy and MIOU accuracy for a set of outputs.
```python
# Place this file in SegNet/Scripts:
# Usage:
    from compute_test_result import calculate_data
    result = calculate_data(233, "ground_truth_images/", "prediction_images/") 
```

2.`SegNet-Scripts/test_bayesian_segnet.py`: modified version which saves prediction images and uncertainty images in two folders.
```shell
# Place this file in SegNet/Scripts (replace the original test_bayesian_segnet.py):
# Usage: (check official tutorial as well: http://mi.eng.cam.ac.uk/projects/segnet/tutorial.html)
    python /SegNet/Scripts/test_bayesian_segnet.py --model /SegNet/Models/bayesian_segnet_inference.prototxt --weights /SegNet/Models/Inference/test_weights.caffemodel --colours /SegNet/Scripts/camvid11.png --data /SegNet/CamVid/test.txt  # Test Bayesian SegNet
    python /SegNet/Scripts/test_bayesian_segnet.py --model /SegNet/Models/bayesian_segnet_basic_inference.prototxt --weights /SegNet/Models/Inference/test_weights.caffemodel --colours /SegNet/Scripts/camvid11.png --data /SegNet/CamVid/test.txt  # Test Bayesian SegNet Basic
# ground truth images will be saved in gt/ 
# prediction images will be saved in precitions/
# uncertainty images will be saved in uncertainty/ 
```

3.`SegNet-Scripts/test_segmentation_camvid.py`: modified version which saves prediction images in a folder.
```shell
# Place this file in SegNet/Scripts (replace the original test_segmentation_camvid.py):
# Usage:
    python /SegNet/Scripts/test_segmentation_camvid.py --model /SegNet/Models/segnet_inference.prototxt --weights /SegNet/Models/Inference/test_weights.caffemodel --iter 233  # Test SegNet
    python /SegNet/Scripts/test_segmentation_camvid.py --model /SegNet/Models/segnet_basic_inference.prototxt --weights /SegNet/Models/Inference/test_weights.caffemodel --iter 233  # Test SegNetBasic
# ground truth images will be saved in gt/ 
# prediction images will be saved in precitions/
```

4.`gco_python-Scripts/segnet_denoise.py`: applies pairwise MRF on top of CNN outputs.
```python
# Place this file in gco_python/ :
# Usage:
    from segnet_denoise import compute_all
    compute_all(233, 800, -1000) # 233:number of images to optimize, 800:unary potential weight, -1000:pairwise potential weight
    
# please change line 9 accordingly in order to import compute_test_result.py
# based on your own need, you can change the file paths for :
# 1. unoptimized output images and uncertainty images accordingly in line 115 & 117
# 2. saved optimized output images in line 147 
# 3. ground truth images as input in line 177 & 178 
```



__dependencies of `4. gco_python-Scripts/segnet_denoise.py`:__

1. `gco_python-Scripts/data.py`: stores the pairwise potentials weight matrix. 
2. `gco_python-Scripts/find_num_of_pairs.py`: produces data in `data.py` (counts num of all possible pairs on images then generated the pairwise potentials weight matrix.)
```shell
# Usage:
    python find_num_of_pairs
# you will need to change the file path for ground truth images on line 48 accordingly.
```

_*More details about how to use this matrix are mentioned in `gco_python-Scripts/find_num_of_pairs.py`._



###The following files are NOT important: 
__these files were highly customized for specific purpose so they may not be useful in other projects:__

1. `install_dep.sh`: installs some dependencies for testing purpose while using docker.
2. `SegNet-Scripts/add_roadmark_to_233_pics.py`: adds roadmarks to ground truth images in test dataset. 
3. `SegNet-Scripts/check_233_pics.py`: simply displays two corresponding images sequentially. 
4. `SegNet-Scripts/check_233_pics_0_232.py`: simply displays two corresponding images sequentially, with measure of model uncertainty.
5. `SegNet-Scripts/check_how_many_colors.py`: prints the number of different colors on uncertainty images. can be customized to check any image.
6. `SegNet-Scripts/invert_bayesian_color.py`: converts weirdly-colored outputs of modified webdemo model into normally-colored outputs.
7. `SegNet-Scripts/rename.sh`: renames all files in a folder to `number.png`. `number` starts from 0. 
8. `SegNet-Scripts/run_test.sh`: a simple script to run my time-consuming tests overnight.
9. `gco_python-Scripts/data_prev.py`: stores the experimental pairwise potentials weight matrices. (with rgb optimization) Deprecated since improvements were low.
10. `note.txt`: my random notes.
