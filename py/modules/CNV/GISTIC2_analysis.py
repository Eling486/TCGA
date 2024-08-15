import os
import pandas as pd

def read_thresholded_data(genes, output):
    thresholded_data_file = './input/GISTIC2/all_thresholded.by_genes.txt'
    
    if not os.path.exists(thresholded_data_file):
        print(f'CNV Analysis - Please using GISTIC2 to identify the genes first!')
        return None
    
    df = pd.read_csv(thresholded_data_file, sep="\t")
    df = df[df['Gene Symbol'].isin(genes)]
    df.to_csv(os.path.join(output, 'CNV_gene_selected.csv'), sep='\t', index=False)
    return df

def case_cluster_single(genes, output):
    
    df = read_thresholded_data(genes, output)
    if df is None:
        return None, None
    
    cluster_result = pd.DataFrame()
    CNV = {}
    group_next = 0
    
    for barcode in df.iloc[:, 3:]:
        copy_num = df[df['Gene Symbol'] == genes[0]][barcode].values[0]
        group = group_next
        if copy_num in CNV:
            group = CNV[copy_num]
        else:
            CNV[copy_num] = group_next
            group_next += 1
        sample_result = pd.DataFrame({'barcode': barcode, 'group': group, 'copy_num': copy_num}, columns=['barcode','group','copy_num'], index=[0])
        cluster_result = pd.concat([cluster_result, sample_result])
    cluster_result.to_csv(os.path.join(output, f'case_cluster_{genes[0]}.csv'), sep='\t')
    print(f'CNV Analysis - Merging Data: Saving Cluster Data ({len(CNV)} groups totally)')
    return len(CNV), os.path.join(output, f'case_cluster_{genes[0]}.csv')

def case_cluster_double(genes, output):
    df = read_thresholded_data(genes, output)
    if df is None:
        return None, None
    
    cluster_result = pd.DataFrame()
    
    for barcode in df.iloc[:, 3:]:
        group_num = None
        copy_num_type = None
        copy_num_1 = df[df['Gene Symbol'] == genes[0]][barcode].values[0]
        copy_num_2 = df[df['Gene Symbol'] == genes[1]][barcode].values[0]
        if copy_num_1 < 0 and copy_num_2 < 0:
            group_num = 0
            copy_num_type = '-/-'
        if copy_num_1 < 0 and copy_num_2 == 0:
            group_num = 1
            copy_num_type = '-/0'
        if copy_num_1 < 0 and copy_num_2 > 0:
            group_num = 2
            copy_num_type = '-/+'
            
        if copy_num_1 == 0 and copy_num_2 < 0:
            group_num = 3
            copy_num_type = '0/-'
        if copy_num_1 == 0 and copy_num_2 == 0:
            group_num = 4
            copy_num_type = '0/0'
        if copy_num_1 == 0 and copy_num_2 > 0:
            group_num = 5
            copy_num_type = '0/+'
            
        if copy_num_1 > 0 and copy_num_2 < 0:
            group_num = 6
            copy_num_type = '+/-'
        if copy_num_1 > 0 and copy_num_2 == 0:
            group_num = 7
            copy_num_type = '+/0'
        if copy_num_1 > 0 and copy_num_2 > 0:
            group_num = 8
            copy_num_type = '+/+'
        sample_result = pd.DataFrame({'barcode': barcode, 'group': group_num, 'copy_num': copy_num_type}, index=[0])
        cluster_result = pd.concat([cluster_result, sample_result])
    cluster_result.to_csv(os.path.join(output, f'case_cluster_{genes[0]}+{genes[1]}.csv'), sep='\t')
    print(f'CNV Analysis - Merging Data: Saving Cluster Data')
    return 9, os.path.join(output, f'case_cluster_{genes[0]}+{genes[1]}.csv')