
# modules
import cv2
import numpy as np


# Cross_correlation func
def cross_correlation_2d(arr, kernel):
    """
    :param arr:
    :param kernel:2D Tuple like(a,b)
    :return:The Matrix obtained by cross_correlation in 2D.
    :return: Cross_correlation Matrix
    """
    rows_arr, cols_arr = arr.shape[:2]
    rows_ker, cols_ker = kernel.shape[:2]
    padding = (rows_ker - 1) // 2

    rows_pad, cols_pad = rows_arr + 2 * padding, cols_arr + 2 * padding
    arr_pad = np.zeros((rows_pad, cols_pad))
    arr_pad[padding:padding + rows_arr, padding:padding + cols_arr] = arr[:]

    optMat = np.zeros((rows_arr, cols_arr), dtype=np.float32)
    # The cross_correlation output Matrix
    if rows_ker % 2 == 0 & cols_ker % 2 == 0 & rows_ker != cols_ker:
        print('Cross_correlation_2d Error!The size of kernel must be (2k+1)*(2k+1)!')
        return
    elif arr.ndim != 2:
        print('Cross_correlation_2d Error!The dimension of array must be 2!')
        return
    else:
        for i in range(0, rows_arr):
            for j in range(0, cols_arr):
                optMat[i][j] = np.sum(arr_pad[i:i + rows_ker, j:j + cols_ker] * kernel)
        return optMat


# Convolution func
def convolve_2d(img, kernel):
    """
    :param img:
    :param kernel:
    :return: Result of Convolution.
    """
    kernel = np.rot90(np.fliplr(kernel), 2)
    convolve_product = cross_correlation_2d(img, kernel)

    return convolve_product


# Gaussian blur
def Gaussian_blur_kernel_2d(ksize: int, sigma):
    """
    :param ksize:Size of Kernel.Rows and Cols should be odd.
    :param sigma:Standard deviation of convolution kernel in horizontal direction
    :return:Gaussian Blur Kernel
    """
    if ksize % 2 == 0:
        print("The size of Gaussion kernel's rows and cols should be odd!")
        return
    else:
        kernel = np.zeros((ksize, ksize), dtype=np.float32)
        center = ksize // 2
        if sigma <= 0:
            sigma = ((ksize - 1) * 0.5 - 1) * 0.3 + 0.8
        s = sigma ** 2
        sum_val = 0
        for i in range(ksize):
            for j in range(ksize):
                x, y = i - center, j - center
                kernel[i, j] = np.exp(-(x ** 2 + y ** 2) / (2 * s))
                kernel[i, j] /= np.sqrt(2 * np.pi * s)
                sum_val += kernel[i, j]
        kernel /= sum_val

        return kernel


def low_pass(img, ksize: int, sigma):
    """
    :param img:
    :param ksize:Size of Kernel
    :param sigma:Standard deviation of convolution kernel in horizontal direction
    :return:Low Pass Matrix
    """
    kernel = Gaussian_blur_kernel_2d(ksize, sigma)
    b, g, r = cv2.split(img)
    b1 = convolve_2d(b, kernel)
    g1 = convolve_2d(g, kernel)
    r1 = convolve_2d(r, kernel)
    res = cv2.merge([b1, g1, r1])
    res = res.astype(np.uint8)
    return res


def high_pass(img, ksize: int, sigma):
    """
    :param img:
    :param ksize:Size of Kernel
    :param sigma:Standard deviation of convolution kernel in horizontal direction
    :return:
    """
    img_low = low_pass(img, ksize, sigma)
    img = img.astype(np.int32)
    img_low = img_low.astype(np.int32)
    res = img - img_low
    # Normalize to avoid negative pixel values
    res = 255 * (res - res.min()) / (res.max() - res.min())
    res = res.astype(np.uint8)
    return res


if __name__ == '__main__':
    # Image Read
    img1 = cv2.imread('cat.jpg')
    img2 = cv2.imread('dog.jpg')
    # Image Process
    img1_high = high_pass(img1, 33, 13)
    img2_low = low_pass(img2, 23, 7)
    hybrid_img = cv2.addWeighted(img1_high, 0.5, img2_low, 0.7, 0)
    # Save Images
    cv2.imwrite('left.png', img2_low)
    cv2.imwrite('right.png', img1_high)
    cv2.imwrite('hybrid.png', hybrid_img)
