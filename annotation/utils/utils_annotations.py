from osgeo import osr
import xml.etree.ElementTree as ET
import os

def pixel_to_geo_transform(geo_transform, x, y):
    # Convert pixel coordinates to geographic coordinates using the GeoTransform.
    x_geo = geo_transform[0] + x * geo_transform[1] + y * geo_transform[2]
    y_geo = geo_transform[3] + x * geo_transform[4] + y * geo_transform[5]
    return x_geo, y_geo

def process_aux_xml(aux_xml_path):
    # Parse the .aux.xml file to extract metadata.
    tree = ET.parse(aux_xml_path)
    root = tree.getroot()
    metadata = {elem.tag: elem.text for elem in root.iter()}
    
    # Extract GeoTransform values and store them in metadata.
    geo_transform_values = metadata['GeoTransform'].split(',')
    for i, value in enumerate(geo_transform_values):
        metadata[f'GeoTransform_{i}'] = value.strip()
    return metadata

def transform_to_wgs84(x_geo, y_geo, srs_wkt):
    # Create spatial reference objects for the source and WGS84 coordinate systems.
    srs = osr.SpatialReference()
    srs.ImportFromWkt(srs_wkt)
    srs_wgs84 = osr.SpatialReference()
    srs_wgs84.ImportFromEPSG(4326)
    
    # Transform geographic coordinates to WGS84.
    transform = osr.CoordinateTransformation(srs, srs_wgs84)
    return transform.TransformPoint(x_geo, y_geo)[:2]

def convert_annotation(annotation_path, aux_xml_path, tile_size=512):
    
    # Process the .aux.xml file to extract metadata
    metadata = process_aux_xml(aux_xml_path)
    
    # Retrieve GeoTransform from metadata
    geo_transform = tuple(float(metadata[f'GeoTransform_{i}']) for i in range(6))

    # New annotations
    new_annotations = []

    # Open the annotation file (yolo) and read the bounding boxes
    with open(annotation_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip().split()
            
            # Extract the class ID and bounding box coordinates
            class_id, yolo_x, yolo_y, yolo_w, yolo_h = map(float, line)
            class_id = int(class_id)

            # Calculate the center of the bounding box
            center_x = (yolo_x + yolo_w / 2) * tile_size
            center_y = (yolo_y + yolo_h / 2) * tile_size
            
            # Convert pixel coordinates to geographic
            x_geo, y_geo = pixel_to_geo_transform(geo_transform, center_x, center_y)
    
            # Convert geographic coordinates to WGS84
            lat, lon = transform_to_wgs84(x_geo, y_geo, metadata['SRS'])

            # Extract the timestamp from the filename
            basename_split = os.path.basename(annotation_path).split('_')
            date = basename_split[0]
            time = basename_split[1]
            timestamp = f"{date[:4]}-{date[4:6]}-{date[6:]} {time[:2]}:{time[2:4]}:{time[4:]}"

            # Append the new annotation to the list
            new_annotations.append([class_id, yolo_x, yolo_y, yolo_w, yolo_h, lat, lon, timestamp])
            
    return new_annotations