"""computes metric correlations with and without outliers 
(with or without william's test for statistical significance),
and writes results to latex/csv tables or displays them in ipython notebook"""

import pandas as pd
import glob 
            
from outliers import is_outlier
from metric_williams import metric_williams
from utils import output_allsys_tables, output_combined_tables

class DACorrelation:
    """ stores and returns information related to Pearson correlation
    and (optionally) significance values for each language pair """
    
    def __init__(self, scores_dir = None, williams = False, outliers = False):  
        self.ss = williams
        self.outliers = outliers

        self.lps = []  
        self.correlations = {}  
        self.pvals = {}   
        if scores_dir:
            self.add_scores_dir(scores_dir)
        
    def add_scores_dir(self, scores_dir):  
        scores_files = f'{scores_dir}/*scores.csv'
        for file in glob.glob(scores_files): 
            scores = pd.read_csv(file, delimiter = '\s', engine='python') 
            if self.outliers:
                scores = scores[~is_outlier(scores['HUMAN'])]         
            self.add_scores(scores)

    def add_scores(self, scores):  
        lp = scores['LP'].values[0] 

        self.lps.append(lp) 

        corrs = pd.DataFrame(scores.corr().HUMAN[1:].rename('Pearson'))    
        corrs = corrs.sort_values('Pearson', ascending=False)
        corrs['N'] = len(scores) 

        if self.ss:
            self.pvals[lp], winners = metric_williams(scores)  
            corrs['Winner'] =  winners  
            
        self.correlations[lp] = corrs

    def get_tables(self, lps, formatter):   
        corrs = [] 
        for lp in lps: 
            corr = self.correlations[lp]
            if not self.ss:
                corr.Winner = [False for _ in corr.index]
            formattedscores = [formatter(c, w) for c,w in zip(corr.Pearson, corr.Winner)]    
            corrs.append(pd.DataFrame(index = corr.index, data = {(lp, corr.N[0]): formattedscores }))
            
        res = pd.DataFrame().join(corrs, how='outer', sort=False).fillna('-')
        return res.reindex(sorted(res.index.values,key = lambda x: x.upper()))

    def write_corr_files(self, output_dir):
        if self.outliers:
            suffix = '-nooutl'
        else:
            suffix = ''
        """writes correlations and significance results to file for each language pair"""
        for lp in self.lps: 
            lp_ = "".join(lp.split('-'))  
            self.correlations[lp].to_csv( f"{output_dir}/DA-{lp_}-cor{suffix}.csv", sep= '\t')
            if self.ss:
                self.pvals[lp].to_csv(f"{output_dir}/DA-{lp_}-sig{suffix}.csv", sep= '\t')
            
                  

if __name__ == '__main__':
     
    import argparse
    import os
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--scores-dir', type=str, default='data/wmt19_sys_scores', help="Directory with scores files")  
    parser.add_argument('--outliers', action='store_true', default = False, help='also include results without outlier systems')
    parser.add_argument('--winners', action='store_true', default = False, help="get winners using William's test")

    parser.add_argument('--corr-dir', type=str, default=None, help="Directory to store correlations for each language pair, and if 'winners' is true, also saves p-values")  
    parser.add_argument('--outputformat', type=str, default='latex', choices = ['latex','csv'], help="format to save final results tables")
    parser.add_argument('--tables-dir', type=str, default=None, help="Directory to save final results tables")

    args = parser.parse_args()


    # tables_template

    da_allsys = DACorrelation(args.scores_dir, args.winners, outliers = False)  
    if args.outliers:
        da_nooutl = DACorrelation(args.scores_dir, args.winners, outliers = True)    
        

    if args.corr_dir:
        if not os.path.exists(args.corr_dir):
            os.makedirs(args.corr_dir)

        da_allsys.write_corr_files(args.corr_dir)
        if args.outliers:
            da_nooutl.write_corr_files(args.corr_dir)


    if args.tables_dir:
        if not os.path.exists(args.tables_dir):
            os.makedirs(args.tables_dir)

        if args.outliers:
            output_combined_tables(da_allsys, da_nooutl, args.outputformat, args.tables_dir )
        else:
            output_allsys_tables(da_allsys, args.outputformat, args.tables_dir )
