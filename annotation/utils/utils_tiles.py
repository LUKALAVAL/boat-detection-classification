import os
import subprocess
from osgeo import gdal



# Split a .jpeg file into .jpeg tiles
def split_into_tiles(input_jpeg, output_folder, tile_size=512):
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open .jpeg input file
    image = gdal.Open(input_jpeg)
    if not image:
        raise FileNotFoundError(f"Unable to open {input_jpeg}")

    # Get the size of the image
    band = image.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize

    # Function to check if a tile is fully black
    def is_tile_empty(tile):
        if(tile is None):
            return True
        return tile.max() == 0

    # Split the image into tiles
    for i in range(0, xsize, tile_size):
        for j in range(0, ysize, tile_size):
            output_file = os.path.join(output_folder, f"{os.path.basename(input_jpeg)[:-5]}_{i}_{j}.jpeg")
            tile = image.ReadAsArray(i, j, tile_size, tile_size)
            print(f"Processing tile {i}_{j}")
            if(not is_tile_empty(tile)):
                gdal.Translate(output_file, image, srcWin=[i, j, tile_size, tile_size])





# Get min and max values for a band using percentiles
def get_min_max_percentiles(band, min_percentile=2, max_percentile=98):
    stats = band.GetStatistics(True, True)
    min_val = stats[0]
    max_val = stats[1]
    return min_val, max_val

# Convert a .tif file to a .jpeg file
def tif_to_jpeg(input_tif, output_jpeg, min_percentile, max_percentile):

    # Open .tif input file
    image = gdal.Open(input_tif)

    # Get the 3 bands
    band1 = image.GetRasterBand(1)
    band2 = image.GetRasterBand(2)
    band3 = image.GetRasterBand(3)

    # Get min and max values for each band
    min1, max1 = get_min_max_percentiles(band1, min_percentile, max_percentile)
    min2, max2 = get_min_max_percentiles(band2, min_percentile, max_percentile)
    min3, max3 = get_min_max_percentiles(band3, min_percentile, max_percentile)

    # Parameters for gdal_translate command
    command = [
        'gdal_translate',
        '-of', 'JPEG',  # Output format
        '-ot', 'Byte',  # Output data type
        '-b', '3', # Red band    
        '-b', '2', # Green band
        '-b', '1', # Blue band
        '-scale', str(min3), str(max3), "0", "255", # Scale values to 0-255
        '-scale', str(min2), str(max2), "0", "255",
        '-scale', str(min1), str(max1),"0", "255",
        input_tif,
        output_jpeg
    ]

    # Run the gdal_translate command
    print(' '.join(command))
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the conversion was successful
    if result.returncode == 0:
        print("Conversion successful!", input_tif, "->", output_jpeg)
    else:
        print("Error!")
        print("Error code:", result.returncode)
        print("Standard output:", result.stdout)
        print("Standard error:", result.stderr)








