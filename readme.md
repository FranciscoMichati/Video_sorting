This code is made to sort chronologically 100 unsorted frames.

The unsorted frames are readed from .npy files located in ./frames_npy. The .jpg version of this frames are located in ./frames_unsorted_images.

The code uses a L1-norm cost function to sort frames by minimizing "pixel distance" between consecutive frames, and then recreates the full video using openCV. 
The sorted .jpg frames together with the video are located in the folder ./frames_sorted
