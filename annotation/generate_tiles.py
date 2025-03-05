from utils.utils_tiles import *

# Percentiles for color channel scaling
min_percentile = 2
max_percentile = 98

# Tile size
tile_size = 512

# Input and output folders
input_folder = "PlanetScope/data/"
output_folder_jpegs = "annotation/jpegs/"
output_folder_tiles = "annotation/tiles/"

# Create output folders if don't exist
if not os.path.exists(output_folder_jpegs):
    os.makedirs(output_folder_jpegs)
if not os.path.exists(output_folder_tiles):
    os.makedirs(output_folder_tiles)

# Get all the AnalyticMS_SR_clip.tif images in the PSScene folder
files = os.listdir(input_folder)
files = [f for f in files if f.endswith("AnalyticMS_SR_clip.tif")]

# Process each image
for f in files:

    print(f"Processing {f}...")

    # Input and output files
    input_tif = os.path.join(input_folder, f)
    output_jpeg = os.path.join(output_folder_jpegs, f[:-4] + ".jpeg")

    # Convert .tif to .jpeg
    tif_to_jpeg(input_tif, output_jpeg, min_percentile, max_percentile)

    # Split .jpeg into tiles
    split_into_tiles(output_jpeg, output_folder_tiles, tile_size)

    print(f"...{f} processed.\n\n")



