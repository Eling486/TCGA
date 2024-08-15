import os
import numpy as np
import pandas as pd


def cluster_case_list(cluster_file, group_num, output):
    cluster_data = pd.read_csv(cluster_file, sep="\t")

    group_list = range(0, group_num)
    
    print(f'CNV Analysis - Merging Data: Saving Cluster Data into list format')
    
    with open(os.path.join(output, f'{os.path.splitext(os.path.split(cluster_file)[1])[0]}_list.csv'), 'w') as fw:
        for group in group_list:
            fw.write(f'Group {group+1} (Copy Number = {cluster_data[cluster_data.group == group]['copy_num'].values[0]}):\n')
            fw.write(', '.join(list(cluster_data[cluster_data.group == group]['barcode'])))
            fw.write('\n\n')
