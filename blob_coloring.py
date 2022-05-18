import cv2, math
import numpy as np


class CellCounting:
    def __init__(self):
        pass

    def blob_coloring(self, image):
        regions = dict()
        k = 1  # region number counter
        height, width = image.shape[:2]
        R = np.zeros((height, width))  # region color" array R
        I = image.copy()  # binary image I

        # 255 stands for 1
        # Algorithm:
        # Search bottom-up and left-to-right
        # Check up and left side of the current cell == 1
        # If its neighbors are 0, create a new blob there
        # Assign this blob with region counter
        # If they are, or one of them is 1,
        # Append up or left into this region

        for i in range(0, height):
            for j in range(0, width):
                # To check if we are in a cell that at a border or not
                is_corner, is_body = False, False
                if i is 0 and j is 0:
                    is_corner = True
                elif i is not 0 and j is not 0:
                    is_body = True

                # To check if we're currently visiting horizontally/vertically
                left_to_right, bottom_up = False, False
                if i is 0 and j is not 0:
                    left_to_right = True
                elif j is 0 and i is not 0:
                    bottom_up = True

                # To check if the cell at top and or edge
                adj = R[i][j - 1]  # adjacent left
                up = R[i - 1][j]  # top/up cell

                if I[i][j] == 255:
                    if is_corner:
                        # create new region in corner (0, 0)
                        R[i][j] = k  # k assigned to blob
                        regions[k] = [(i, j)]
                        k += 1

                    elif left_to_right:
                        # loop horizontally
                        if I[i][j - 1] != 255:  # if current image cell is not 1
                            R[i][j] = k  # assign new blob
                            regions[k] = [(i, j)]
                            k += 1
                        else:
                            # make the same region as left
                            # append region into the same region cell which has value 1
                            R[i][j] = adj
                            regions[R[i][j]].append((i, j))

                    elif bottom_up:
                        # loop vertically
                        if I[i - 1][j] != 255:
                            R[i][j] = k
                            regions[k] = [(i, j)]
                            k += 1
                        else:
                            # make the same region as up
                            R[i][j] = up
                            regions[R[i][j]].append((i, j))

                    elif is_body:  # in the middle of somewhere
                        if I[i][j - 1] == 0:
                            if I[i - 1][j] == 0:
                                # current cell(I[i][j]) is 1, but up((I[i - 1][j])) and left cells((I[i][j - 1])) are 0
                                # create and assign a new blob
                                R[i][j] = k
                                regions[k] = [(i, j)]
                                k += 1
                            elif I[i - 1][j] == 255:
                                # current cell(I[i][j] is 1, left cell(I[i][j - 1]) is 0, but up(I[i - 1][j]) is 1
                                # then assign the current region as up
                                R[i][j] = up
                                regions[R[i][j]].append((i, j))
                        elif I[i][j - 1] == 255:
                            if I[i - 1][j] == 0:
                                # current cell is 1, left cell is 0, but up is 1
                                R[i][j] = adj
                                regions[R[i][j]].append((i, j))
                            if I[i - 1][j] == 255:
                                R[i][j] = up
                                regions[R[i][j]].append((i, j))

                                # if top and left pixels belong to different regions, make them same
                                if adj != up:
                                    remove = R[i][j - 1]
                                    regions[R[i - 1][j]] = regions[R[i - 1][j]] + regions[R[i][j - 1]]

                                    for reg in regions[R[i][j - 1]]:
                                        R[reg[0]][reg[1]] = R[i - 1][j]
                                    regions.pop(remove)

            # Ignore cells w/ less than 15 pixel
            # Print report
        accepted_blobs = 0
        for region, val in list(regions.items()):
            if len(val) < 15:
                # if pixel is less than 15, remove this region from the regions
                regions.pop(region)
            else:
                accepted_blobs += 1

        print('Accepted ', accepted_blobs, ' blobs at total')
        print('regions:', regions)
        return regions

    def compute_statistics(self, region):
        stats = dict()

        # x = [p[0] for p in points]
        # y = [p[1] for p in points]
        # centroid = (sum(x) / len(points), sum(y) / len(points))

        for reg, val in list(region.items()):
            arr = np.array(val)
            #  print(arr.shape[0], arr.shape[1])
            mass = len(val)
            #  average of left points
            cx = int(round(math.fsum(arr[:, 0]) / mass))
            #  average of right points
            cy = int(round(math.fsum(arr[:, 1]) / mass))
            centroid = (cy, cx)
            print("(Region:", reg, ", Area:", mass, ", Centroid:", centroid, ')')
            stats[reg] = [centroid, mass]

        print("stats:", stats)
        return stats

    def mark_image_regions(self, image, stats):
        copy_image = image.copy()
        #  recall: stats[reg] = [centroid, mass]
        for reg, value in list(stats.items()):
            centroid = value[0]
            # print('centroid', centroid)
            mass = value[1]
            # print('area', area)
            text = ('*' + str(reg) + ',' + str(mass))
            pos = centroid
            font = cv2.FONT_HERSHEY_SIMPLEX
            color = (125, 246, 55)
            font_scale = 0.2
            font_size = 1
            cv2.putText(copy_image, text, pos, font, font_scale, color, font_size)

        return copy_image
