import numpy as np
import math


class Filtering:

    def __init__(self, image):
        self.image = image

    # 180 degree rotation function for convolution
    def rotate_180(self, I):
        img = I.copy()
        height, width = I.shape[:2]

        for i in range(0, height):
            for j in range(0, width):
                img[i, j] = I[height - i - 1][width - j - 1]

        return img

    # additional helper method to apply filter
    def convolution(self, I, kernel):
        # dimensions of the image
        im_height, im_width = I.shape[:2]
        # rotate the kernel by 180 and then
        # get the dimensions of the kernel filter
        kernel = self.rotate_180(kernel)
        ker_height, ker_width = kernel.shape[:2]
        h, w = im_height + ker_height-1, im_width + ker_width-1

        zero_padded_img = np.zeros((h, w))
        zero_padded_img[1:im_height+1, 1:im_width+1] = I

        k_height = ker_height // 2
        k_width = ker_width // 2
        # filtered output matrix
        matrix = np.zeros((im_height, im_width))

        for i in range(k_height, im_height-k_height):
            for j in range(k_width, im_width-k_width):
                sum = 0
                for m in range(ker_height):
                    for n in range(ker_width):
                        sum += kernel[m][n] * zero_padded_img[i - k_height - m][j - k_width - n]
                matrix[i][j] = sum

        return matrix

    def get_gaussian_filter(self):
        """Initialzes/Computes and returns a 5X5 Gaussian filter"""
        M, N = 5, 5  # dimensions of the kernel
        kernel = np.zeros((M, N))  # 5x5 kernel
        center = 5 // 2  # the center pixel location of the kernel
        sum = 0  # sum of pixels of the kernel (to normalize)
        sigma = 1  # default standard deviation value

        for x in range(0, M):
            for y in range(0, N):
                # in the formula, x and y specify the delta from the center pixel
                delta = ((x - center) ** 2) + ((y - center) ** 2)
                # apply formula step-by-step
                formula = math.exp(-1 * delta / (2 * sigma * sigma)) / \
                      (2 * math.pi * (sigma ** 2))
                kernel[x, y] = formula
                sum += kernel[x, y]

        # normalize (to make the sum of the filter 1)
        # ...to be safe about the sigma
        1/sum * kernel

        return kernel

    def get_laplacian_filter(self):
        kernel = np.array([[0, 1, 0],
                           [1, -4, 1],
                           [0, 1, 0]])

        return kernel

    def filter(self, filter_name):
        filtered = np.zeros((self.image.shape[0], self.image.shape[1]))
        if filter_name == 'gaussian':
            kernel = self.get_gaussian_filter()
            filtered = self.convolution(self.image, kernel)
        elif filter_name == 'laplacian':
            kernel = self.get_laplacian_filter()
            filtered = self.convolution(self.image, kernel)

        return filtered
