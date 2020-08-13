# tangled
Code, data, and additional analysis for the paper Tangled up in BLEU: Reevaluating the Evaluation of Automatic Machine Translation Evaluation Metrics



# Code to compute correlation without Outliers

## Requirements:
Python >= 3.6
numpy and pandas
And optionally, if you'd like to get "winners" of a language pair, i.e. metrics not outperformed by any other based on the William's test for statistical significance, you'll need the r2py library in python, and the psych library in R. 



The script takes as input a directory of *scores.csv files, with columns "LP SYSTEMID HUMAN METRIC1 METRIC2 ... METRICN"
 (These can be obtained using the combine-scores-sys-DA.py script released with the WMT results package every year. Files for WMT 19 are in the folder data/wmt19_sys_scores. )

## Usage 
```
usage: metrics_da_results.py [-h] [--scores-dir SCORES_DIR]
                             [--corr-dir CORR_DIR]
                             [--outputformat {latex,csv,display_nb}]
                             [--tables-dir TABLES_DIR] 
                             [--williams]
                             [--outliers]

optional arguments:
  -h, --help            show this help message and exit
  --scores-dir SCORES_DIR
  --corr-dir CORR_DIR
  --outputformat {latex,csv,display_nb}
  --tables-dir TABLES_DIR
  --williams
  --outliers
```

Example usage to compute correlations and winners both with and without outliers on WMT19 metrics data, and write correlations files and latex tables 

```
metrics_da_results.py --scores-dir ../data/wmt19_sys_scores \
                      --corr-dir ../data/wmt19_sys_correlations \
                      --outputformat latex \
                      --tables-dir .../data/wmt19_sys_tables \
                      --winners \
                      --outliers 
```







