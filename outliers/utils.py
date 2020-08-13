import pandas as pd

def fmt_nb(val): 
    if str(val).endswith('*'):
        return 'font-weight: bold' 
    else:
        return ''
     
def fmt_latex(val, win):  
    return f"\textbf{{{val:.3f}}}" if win else f"{val:.3f}" 

def add_star(val, win):  
    return f"{val:.3f}*" if win else f"{val:.3f}" 

def escape_latex(row):
    """copied from pandas source code available at
    https://github.com/pandas-dev/pandas/blob/master/pandas/io/formats/latex.py"""
    crow = [
                (
                    x.replace("\\", "\\textbackslash ")
                    .replace("_", "\\_")
                    .replace("%", "\\%")
                    .replace("$", "\\$")
                    .replace("#", "\\#") 
                    .replace("{", "\\{")
                    .replace("}", "\\}")
                    .replace("~", "\\textasciitilde ")
                    .replace("^", "\\textasciicircum ")
                    .replace("&", "\\&")
                    if (x and x != "{}")
                    else "{}"
                )
                for x in row
            ]
    return crow

def write_latex_table(tbl, filename):
    tbl.index = [f"\metric{{{val}}}" for val in escape_latex(tbl.index)]
    fmt ="".join(['l'] + ['c' for _ in tbl.columns.get_level_values(1)])
    tbl = tbl.replace('-', '$-$') 
    label = filename.split('.')[0].split('-')[-1]
    tabular = tbl.to_latex(buf = None, escape=False, column_format = fmt, 
        multicolumn_format = 'c')  

    with open(filename,'w') as outf:
        outf.write('\\begin{table}\n')
        outf.write(' \\setlength{\\tabcolsep}{1em}\n')
        outf.write(tabular)
        outf.write('\\end{table}\n')

def get_lp_groups(da):
    lp_groups = {}    
    lp_groups['ento'] = sorted([lp for lp in da.lps if lp.startswith('en-')])
    lp_groups['toen'] =  sorted([lp for lp in da.lps if lp.endswith('-en')])
    lp_groups['other'] =  sorted([lp for lp in da.lps if not 'en' in lp])
    if not lp_groups['other']:
        del lp_groups['other']
    return lp_groups

def combine_tables(tbl_all, tbl_nooutl, outputformat): 

    columns = {}
    if outputformat == 'latex':
        for lp, n_all in tbl_all.columns: 
            n_nooutl = tbl_nooutl[lp].columns[0]
            if n_all == n_nooutl: 
                columns[(lp, 'All', n_all)] = tbl_all[(lp, n_all)]
            else:
                columns[(lp, 'All\quad-out', f'{n_all}\quad\quad{n_nooutl}')] = [f'{a}\quad{o}' for a,o in zip(tbl_all[(lp, n_all)], tbl_nooutl[lp, n_nooutl])]
                 
        return pd.DataFrame.from_dict(columns).replace('-\quad-', '-') 
    else:
        for lp, n_all in tbl_all.columns: 
            columns[(lp, 'All', n_all)] = tbl_all[(lp, n_all)]
            n_nooutl = tbl_nooutl[lp].columns[0]
            if n_all != n_nooutl: 
                columns[(lp, '-out', n_nooutl)] = tbl_nooutl[lp, n_nooutl]
                 
        return pd.DataFrame.from_dict(columns) 


def combine_tables_latex(tbl_all, tbl_nooutl): 
    columns = {}

    for lp, n_all in tbl_all.columns: 
        n_nooutl = tbl_nooutl[lp].columns[0]
        if n_all == n_nooutl: 
            columns[(lp, 'All', n_all)] = tbl_all[(lp, n_all)]
        else:
            columns[(lp, 'All\quad-out', n_nooutl)] = [a+'\quad'+o for a,o in zip(tbl_all[(lp, n_all)], tbl_nooutl[lp, n_nooutl])]
             
    return pd.DataFrame.from_dict(columns).replace('-\quad-', '-') 
        # write_combined_tables(da_allsys, da_nooutl, outputformat, filename_template )

def output_combined_tables(da_allsys, da_nooutl, outputformat, output_dir = None):
    formatter = fmt_latex if outputformat == 'latex' else add_star
    lp_groups = get_lp_groups(da_allsys)

    for name, lps in lp_groups.items(): 

        tbl_all = da_allsys.get_tables(lps,formatter) 
        tbl_nooutl  = da_nooutl.get_tables(lps, formatter) 
        tbl_combined = combine_tables(tbl_all, tbl_nooutl, outputformat)  
        
        if outputformat == 'latex':
            write_latex_table(tbl_all, f'{output_dir}/tbl-DA-{name}.tex')
            write_latex_table(tbl_combined, f'{output_dir}/tbl-DA-{name}-nooutl.tex')
        elif outputformat == 'csv':
            tbl_all.to_csv(f'{output_dir}/{name}.csv')
            tbl_combined.to_csv( f'{output_dir}/{name}-nooutl.csv') 
        elif outputformat == 'display_nb':
            print(name)        
            display(tbl_combined.style.applymap(fmt_nb))        


def output_allsys_tables(da_allsys, outputformat, output_dir=None):
    formatter = fmt_latex if outputformat == 'latex' else add_star
    
    lp_groups = get_lp_groups(da_allsys)

    for name, lps in lp_groups.items():  
        tbl_all = da_allsys.get_tables(lps,formatter)   
        if outputformat == 'latex':
            write_latex_table(tbl_all, f'{output_dir}/tbl-DA-{name}.tex') 
        elif outputformat == 'csv':
            tbl_all.to_csv('f{output_dir}/tbl-DA-{name}.csv') 
        elif outputformat == 'display_nb':
            print(name)        
            display(tbl_all.style.applymap(fmt_nb))           
        
