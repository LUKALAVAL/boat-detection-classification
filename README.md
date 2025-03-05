# boat-detection

## !! The project is currently on hold !!

#### workflow
1. Retrieve satellite images from PlanetScope
2. Run `generate_tiles.py` (creates `jpegs/` and `tiles/`)
3. Annotate tiles using [labelImg](https://github.com/HumanSignal/labelImg)
4. Run `extract_annotations.py` to match the localized boats with the MMSI (to retrieve the boats types)
5. Update the annotated classes according to the previous step
6. Refine the annotations that were not updated 
