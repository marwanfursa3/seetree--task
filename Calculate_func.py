

import numpy as np



##Returnning the MAX value of the image
def Max_value(img):
    ##This relies on the histogram() method, and simply returns the low and high bins used.
    max_value = np.max(img);
    return max_value


##Returnning the MIN value of the image
def Min_value(img):
    min_value = np.min(img);
    return min_value


##Returnning the MEAN of the pixels level in the image
def Mean_value(img):
    Mean_value = np.mean(img)
    return Mean_value


##Returnning the MEDIAN  pixels level in the image
def Median_value(img):
    Median_value = np.median(img)
    return Median_value


## https://stackoverflow.com/questions/2374640/how-do-i-calculate-percentiles-with-python-numpy
# Returnning the N'th percentile of the image
def percentile_value(img, p):
    # converting PIL image to Numpy array
    converttonumpy = np.asarray(img)
    # Calculating the  N'th percentile of the image
    percentile = np.percentile(converttonumpy, p)
    return percentile