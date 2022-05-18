import numpy as np
import cv2


class Operation:

    def __init__(self):
        pass

    def merge(self, image_left, image_right, column):
        rl, cl = image_left.shape
        rr, cr = image_right.shape

        # get particular parts of the images by given column
        roi_left = image_left[0:rl, 0:column]
        roi_right = image_right[0:rr, column:cr]

        # get size of rois
        shl = roi_left.shape
        shr = roi_right.shape

        row_max, col_tot = rl, (shl[1] + shr[1])

        # generate a zero matrix and merge two roi images in it
        merged_mat = np.zeros((row_max, col_tot), np.uint8)
        merged_mat[0:shl[0], 0:shl[1]] = roi_left
        merged_mat[0:shr[0], shl[1]:col_tot] = roi_right

        cv2.imshow("result", merged_mat)
        cv2.waitKey(0)

        return merged_mat

    def intensity_scaling(self, input_image, column, alpha, beta):
        image_shp = input_image.shape

        left_image = input_image[:image_shp[0], :column]
        right_image = input_image[:image_shp[0], column:image_shp[1]]

        left_image = left_image * alpha
        right_image = right_image * beta

        # Result matrix
        mat = np.zeros((image_shp[0], image_shp[1]), np.uint8)
        mat[:left_image.shape[0], :left_image.shape[1]] = left_image
        mat[:right_image.shape[0], left_image.shape[1]:] = right_image

        cv2.imshow("mat", mat)
        cv2.waitKey(0)

        return input_image

    def centralize_pixel(self, input_image, column):
        image_shp = input_image.shape

        left_image = input_image[:image_shp[0], :column]
        right_image = input_image[:image_shp[0], column:image_shp[1]]

        num_of_lpixs = left_image.size
        num_of_rpixs = right_image.size

        tot_left, tot_right = 0, 0
        # get sum of left side pixels
        for row in range(left_image.shape[0]):
            for col in range(left_image.shape[1]):
                tot_left += left_image[row, col]

        # get sum of right side pixels
        for row in range(right_image.shape[0]):
            for col in range(right_image.shape[1]):
                tot_right += right_image[row, col]

        # Get average pixel intensity for both side
        avg_l_pixel = tot_left // num_of_lpixs
        avg_r_pixels = tot_right // num_of_rpixs

        # Compute offsets
        left_offset = (128 - avg_l_pixel)
        right_offset = (128 - avg_r_pixels)

        # Add offset to the left and right sides
        left_im = left_image + left_offset
        right_im = right_image + right_offset

        # Fix pixels that in out of boundary
        for row in range(left_im.shape[0]):
            for col in range(left_im.shape[1]):
                curr_pixel = left_im[row, col]
                if curr_pixel > 255:
                    curr_pixel = 255
                if curr_pixel < 0:
                    curr_pixel = 0
                left_im[row, col] = np.uint8(curr_pixel)

        for row in range(right_im.shape[0]):
            for col in range(right_im.shape[1]):
                curr_pixel = right_im[row, col]
                if curr_pixel > 255:
                    curr_pixel = 255
                if curr_pixel < 0:
                    curr_pixel = 0
                right_im[row, col] = np.uint8(curr_pixel)

        # Result matrix
        mat = np.zeros((image_shp[0], image_shp[1]), np.uint8)
        mat[:left_im.shape[0], :left_im.shape[1]] = left_im
        mat[:right_im.shape[0], left_im.shape[1]:] = right_im

        cv2.imshow("output", mat)
        cv2.waitKey(0)

        return mat
