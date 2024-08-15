from py.modules.CNV.workflow import CNV_analysis

CNV_data_dir = './samples/CNV/Masked Copy Number Segment'

datasets = {
    'tumor': {
        'root': f'{CNV_data_dir}/tumor',
        'matadata': 'metadata.cart.2024-08-07.json',
        'dir': 'gdc_download_20240807_234030.948014'
    },
    'normal': {
        'root': f'{CNV_data_dir}/normal',
        'matadata': 'metadata.cart.2024-08-07.json',
        'dir': 'gdc_download_20240808_000241.574272'
    }
}

input = {
    'cluster_ref_gene': ['BRCA1', 'BECN1', 'PARP1']
}

if __name__ == "__main__":
    datasets = CNV_analysis(datasets, './output/CNV', input)
    pass