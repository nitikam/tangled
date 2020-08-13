import pandas as pd

import rpy2
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri

rpy2.robjects.numpy2ri.activate()
psych = importr('psych') 

INSIGNIFICANT=.12

def williams(n, r12, r13, r23):
    """python interface to the R implementation of the William test for dependent correlations.
    n: number of samples,
    r12: correlation between metric 1 and human, 
    r13: correlation between metric 2 and human, 
    r23: correlation between metric 1 and metric 1 and metric 2

    output: pvalue of william's test"""
    return psych.r_test(n = n, r12 = r12, r13 = r13, r23 = r23, twotailed=False)[-1][0] 


def metric_williams(scores, threshold = 0.05, gold = 'HUMAN'): 
    """input: 
    scores: Pandas dataframe with columns "LP SYSTEM HUMAN METRIC1 METRIC2 ... METRICN" 
    
    output:  
    pvals: a pandas dataframe with p-vals of William's test for every pair of metrics
    winners: list of whether each metric is not outperformed by any other metric
     """
    sample_sz = len(scores) 
    corrs = scores.corr().sort_values(gold, ascending=False)

    metrics = corrs.index.values[1:]
    pvals = pd.DataFrame(columns = metrics)

    for metric1  in metrics:
#         print(metric1)
        m1_h = corrs[metric1][gold] 
        m1_pvals = []
        for metric2 in metrics:
#             print(metric2, end = ' ')
            m1_m2 = corrs[metric1][metric2]
            m2_h = corrs[metric2][gold]
            if metric1 == metric2 or m1_h < m2_h:
                pval = INSIGNIFICANT
            else:
                pval = williams(n = sample_sz, r12 = m1_h, r13 = m2_h, r23 = m1_m2)
            if pval > threshold:
                pval = INSIGNIFICANT
            m1_pvals.append(pval)
        pvals.loc[metric1] = m1_pvals 
    winners = (pvals.values == INSIGNIFICANT).all(0)    #  (pandas<0.24) df.to_numpy() #
    return pvals, winners
 
    
