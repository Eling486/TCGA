import json
import os

import pandas as pd


def merge_masked(datasets, output):
    datasets_count = len(datasets)
    for dataset_index, dataset_name in enumerate(datasets):
        dataset = datasets[dataset_name]
        matadata_file = os.path.join(dataset["root"], dataset["matadata"])
        samples_dir = os.path.join(dataset["root"], dataset["dir"])
        seg_file = f'segmentationfile_{dataset_name}.txt'
        array_file = f'arraylistfile_{dataset_name}.txt'
        
        if os.path.exists(os.path.join(output, seg_file)) and os.path.exists(os.path.join(output, array_file)):
            datasets[dataset_name]['segmentation_file'] = os.path.join(output, seg_file)
            datasets[dataset_name]['array_list_file_file'] = os.path.join(output, array_file)
            continue

        with open(matadata_file, encoding="utf8") as f:
            metadata = json.load(f)
            sample_count = len(metadata)

            df_merged = pd.DataFrame()
            samples = []
            for sample_index, sample in enumerate(metadata):
                barcode = f'{sample["associated_entities"][0]["entity_submitter_id"][0:12]}'
                
                '''
                barcode = f'{sample["associated_entities"][0]["entity_submitter_id"][0:16]}'
                if not barcode[13:16] == '01A':
                    print(f'CNV Analysis - Merging Data: Dataset {dataset_index+1}/{datasets_count} ({dataset_name}) - Sample {sample_index+1}/{sample_count} (excluded)')
                    continue
                '''
                if barcode in samples:
                    print(f'CNV Analysis - Merging Data: Dataset {dataset_index+1}/{datasets_count} ({dataset_name}) - Sample {sample_index+1}/{sample_count} (excluded)')
                    continue
                samples.append(barcode)
                file_id = sample["file_id"]
                file_name = sample["file_name"][0:63]
                if file_name[-1] == '.':
                    file_name = f'{file_name[:-1]}_'
                df = pd.read_csv(os.path.join(samples_dir, file_id, file_name), sep="\t")
                df.rename(columns={"GDC_Aliquot": "Sample", "Start": "Start Position", "End": "End Position", "Num_Probes": "Num Markers", "Segment_Mean": "Seg.CN"}, inplace=True)
                df["Sample"] = barcode
                df_merged = pd.concat([df_merged, df])
                print(f'CNV Analysis - Merging Data: Dataset {dataset_index+1}/{datasets_count} ({dataset_name}) - Sample {sample_index+1}/{sample_count}')

            print(f'CNV Analysis - Merging Data: Saving Dataset {dataset_index+1}/{datasets_count} ({dataset_name}) -> {seg_file}')
            df_merged.to_csv(os.path.join(output, seg_file), sep='\t', index=False)
            print(f'CNV Analysis - Merging Data: Saving Dataset {dataset_index+1}/{datasets_count} ({dataset_name}) Array List File -> {array_file}')
            df_array = pd.DataFrame({'array': samples})
            df_array.to_csv(os.path.join(output, array_file), sep='\t', index=False)
            datasets[dataset_name]['segmentation_file'] = os.path.join(output, seg_file)
            datasets[dataset_name]['array_list_file_file'] = os.path.join(output, array_file)
    
    return datasets