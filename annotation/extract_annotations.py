from utils.utils_annotations import *

# Input folder and output CSV file
input_folder = "tiles"
output_csv = "annotations.csv"

# Tile size in pixels
tile_size = 512

# Get all the annotation files in the input folder
files = os.listdir(input_folder)
files = [f for f in files if f.endswith(".txt")]
files.remove('classes.txt')

# Create the CSV file and write the header
with open(output_csv, 'w') as file:
    file.write("class_id,yolo_x,yolo_y,yolo_w,yolo_h,latitude,longitude,filename,mmsi,confidence\n")

# Process each image
for f in files:
    
    # Get the annotation and auxiliary XML file paths
    annotation_path = os.path.join(input_folder, f)
    aux_xml_path = annotation_path[:-4] +'.jpeg.aux.xml'

    new_annotations = convert_annotation(annotation_path, aux_xml_path, tile_size)

    # Append the new annotations to the CSV file
    with open(output_csv, 'a') as file:
        for annotation in new_annotations:
            file.write(','.join(map(str, annotation)) + f",{f},,\n")

    print(f"{f} processed.")