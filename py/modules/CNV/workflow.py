import os
from py.modules.CNV.merge_data import merge_masked
from py.modules.CNV.format_markers import format_markers
from py.modules.CNV.GISTIC2_analysis import case_cluster_single, case_cluster_double
from py.data.cases import cluster_case_list

def CNV_analysis(datasets, output, input):
    
    probeset = './references/snp6.na35.remap.hg38.subset.txt'
    
    if not os.path.exists(output):
        os.makedirs(output)
        
    datasets = merge_masked(datasets, output)
    
    # Download Ref from https://gdc.cancer.gov/about-data/gdc-data-processing/gdc-reference-files
    # SNP6 GRCh38 Remapped Probeset File for Copy Number Variation Analysis: snp6.na35.remap.hg38.subset.txt
    markers_file = format_markers(probeset, output)
    if not markers_file:
        print(f'CNV Analysis - Please download the SNP6 GRCh38 remapped probeset first!')
        return datasets
    
    # Go to GISTIC2 for next step
    # Online version: https://cloud.genepattern.org/gp/pages/index.jsf?lsid=urn:lsid:broad.mit.edu:cancer.software.genepattern.module.analysis:00125:6.15.30
    
    # group_num, cluster_file = case_cluster(input['cluster_ref_gene'], output)
    group_num, cluster_file = case_cluster_double(input['cluster_ref_gene'], output)
    if cluster_file is None:
        return datasets
    cluster_case_list(cluster_file, group_num, output)
    
    return datasets