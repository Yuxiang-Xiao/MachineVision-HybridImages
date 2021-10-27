# MV-HybridImages-2021
### 🎈Click the star if it's helpful for U,plz.:P
#### The Project 1 of Machine Vision courses in Shien-Ming Wu School  of SCUT, Oct/21.Refer to the CV courses of Cornell-CS5670.
#### ❗❗❗Warning:The code is for learning and communication only. Please indicate the source, author, and MIT Licence in the citation. 
# Project 1: Hybrid Images
------

### Overview

The Project-1 aims to create hybrid image by blending the high frequency portion of one image with the low-frequency portion of another. This work can be mainly divided into 2 parts shown below.

- **Filtering**

  Filtering is a convolution operation in terms of mathematical process. To realize the convolution process, defining a function for correlation is necessary. In fact, **2D correlation** is related to **2D convolution** by a 180° rotation of the kernel.

  By generating **Gaussian filter kernel**, the corresponding weights of different pixels can be determined by the value of Gaussian function, which helps remove the noises of original images.

  There are mainly 2 types of filtering achieved using this method. One is **high-pass filter**, and the other is **low-pass filter**. Pictures filtered through low-pass filter (e.g. Gaussian) will be more smooth. In contrast, pictures filtered through high-pass filter will be more sharpened.

- **Hybrid**

  By hybriding the high-pass-filtered image and low-pass-filtered image, one can see high-pass-filtered (sharpened) image at a short distance while seeing low-pass-filtered (smooth) image at a long distance.

### Installation

- Opencv-python Module
- Numpy Module

### Implementation

- Correlation&Convolution_2D

	~~~python
	def cross_correlation_2d(arr, kernel):
    """
    :param arr:
    :param kernel:2D Tuple like(a,b)
    :return:The Matrix obtained by cross_correlation in 2D.
    :return: Cross_correlation Matrix
    """
	
	def convolve_2d(img, kernel):
	    """
	    :param img:
	    :param kernel:
	    :return: Result of Convolution.
	    """
	~~~

- Gaussian Kernel

  ~~~python
  def Gaussian_blur_kernel_2d(ksize: int, sigma):
      """
      :param ksize:Size of Kernel.Rows and Cols should be odd.
      :param sigma:Standard deviation of convolution kernel in horizontal direction
      :return:Gaussian Blur Kernel
      """
  ~~~

- Low&High Pass

  ~~~python
  def low_pass(img, ksize: int, sigma):
      """
      :param img:3D array of img
      :param ksize:Size of Kernel
      :param sigma:Standard deviation of convolution kernel in horizontal direction
      :return:Low Pass Image's array
      """
  def high_pass(img, ksize: int, sigma):
      """
      :param img:3D array of img
      :param ksize:Size of Kernel
      :param sigma:Standard deviation of convolution kernel in horizontal direction
      :return:High Pass Image's array
      """
  ~~~
  

### Results

- The image of dog is used for low pass. Cat image is used for high pass 

  ~~~ python
  # For cat image，the kernel size is (33,33),sigma=13
  img1_high = high_pass(img1, 33, 13)
  # For dog image，the kernel size is (23,23),sigma=7
  img2_low = low_pass(img2, 23, 7)
  #The mix-in ratio is 0.5 for cat img,0.7 for dog img
  hybrid_img = cv2.addWeighted(img1_high, 0.5, img2_low, 0.7, 0)
  ~~~


  <img src=".\Results\right.png" width="200px" /><img src=".\Results\left.png" width="200px" /><img src=".\Results\hybrid.png" width="200px"/>

  

  <img src=".\Results\hybrid.png" width="200px" /><img src=".\Results\hybrid.png" width="150px" /><img src=".\Results\hybrid.png" width="100px" /><img src=".\Results\hybrid.png" width="50px" /><img src=".\Results\hybrid.png" width="30px" />

### Comments for details

#### 1. Details for Filtering

- To simplify the convolution process, kernel is defined as square matrix with the length of 2k+1.(k=0,1,2...) 

- In correlation_2d part, zeros are used for padding to avoid edge loss. The size of padding is determined by  the size of kernel. 

  And for that, the size of image remain the same after correlation&convolution process.

#### 2. Details for Low&High Pass

- The *Correlation&Convolution_2d* and *Gaussian_blur_kernel_2d* function only process on 2D array. An Image of 3D array would be split into 3 channels (B/G/R) , execute the operation, merged to a new 3D array.

- For high pass, subtract the original image and the low pass image directly will result in negative pixel value. That will bias the image color to black (pixel value 0).

  To solve this problem, the method of positive management is used.
  
  <img src="https://latex.codecogs.com/svg.image?New\,\,pixel\,\,value=255*\frac{x-\min&space;\left(&space;x&space;\right)}{\max&space;\left(&space;x&space;\right)&space;-\min&space;\left(&space;x&space;\right)}" title="New\,\,pixel\,\,value=255*\frac{x-\min \left( x \right)}{\max \left( x \right) -\min \left( x \right)}" />



