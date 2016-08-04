# SegNet-Improvement-via-MRF

##Usage
Note that file paths in this repository do not reflect the actual paths they are in SegNet. this repository serves as a storage for all customized scripts I wrote during my research.

Refer to inline comments in files for more details. 


####The following files are main files that may be reused:
1. `SegNet-Scripts/compute_test_result.py`: calculates global accuracy, class average accuracy and MIOU accuracy for a set of outputs.
2. `SegNet-Scripts/test_bayesian_segnet.py`: modified version which outputs prediction images and uncertainty images into a folder.
3. `SegNet-Scripts/test_segmentation_camvid.py`: modified version which outputs prediction images into a folder.
4. `gco_python-Scripts/segnet_denoise.py`: applies pairwise MRF on top of CNN outputs.



####The following files are dependencies of `gco_python-Scripts/segnet_denoise.py`:

1. `gco_python-Scripts/data.py`: stores the pairwise potentials weight matrix. (with rgb optimization)
2. `gco_python-Scripts/data_prev.py`: stores the pairwise potentials weight matrix. (without rgb optimization)
3. `gco_python-Scripts/find_num_of_pairs.py`: produces data in `data.py` (counts num of all possible pairs on images then generated the pairwise potentials weight matrix.)

*More details about how to use this matrix are mentioned in the report.



####The following files are highly customized for specific use pr very trivial, so they may not be useful in other projects:
1. `install_dep.sh`: installs some dependencies for testing purpose while using docker.
2. `SegNet-Scripts/add_roadmark_to_233_pics.py`: adds roadmarks to ground truth images in test dataset. 
3. `SegNet-Scripts/check_233_pics.py`: simply shows two corresponding images sequentially. 
4. `SegNet-Scripts/check_233_pics_0_232.py`: simply shows two corresponding images sequentially, with measure of model uncertainty.
5. `SegNet-Scripts/check_how_many_colors.py`: prints the number of different colors on uncertainty images. can be customized to check any image.
6. `SegNet-Scripts/invert_bayesian_color.py`: converts weirdly-colored outputs of modified webdemo model into normally-colored outputs.
7. `SegNet-Scripts/rename.sh`: renames all files in a folder to `number.png`. `number` starts from 0. 
8. `SegNet-Scripts/run_test.sh`: a simple script to run my time-consuming tests overnight.

