import os


def format_markers(probeset, output):
    markers_file = "markersfile.txt"
    markers_file_path = os.path.join(output, markers_file)
    if os.path.exists(markers_file_path):
        return markers_file_path
    
    if not os.path.exists(probeset):
        return False
        
    print(f'CNV Analysis - Formatting Remapped Probeset: Saving Formatted Markers File -> {markers_file}')
    
    with open(markers_file_path, "w") as fw:
        f = open(probeset, 'r')
        fw.write('Marker Name\tChromosome\tMarker Position\n')
        for line in f.readlines():
            data = line.split()
            if data[5] == "FALSE":
                fw.write(f'{data[0]}\t{data[1]}\t{data[2]}\n')
        f.close()
    print(f'CNV Analysis - Formatting Remapped Probeset Completed')
    return markers_file_path