import numpy as np

b=1.4826 

def is_outlier(scores_list, threshold = 2.5):
    """ takes a numpy array of scores (or any numbers),
    and returns a Boolean array indicating if the score is an outlier """
    median = np.median(scores_list)
    devs =  abs(scores_list - median)
    mad = np.median(devs) * b
    rescaled  = abs(scores_list -  median)/mad 
    outliers = rescaled > 2.5 
    return outliers

  