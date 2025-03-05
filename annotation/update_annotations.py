import pandas as pd

# Load the input CSV file
input_df = pd.read_csv("annotations_mmsi.csv")

# Load the specs CSV file
specs_df = pd.read_csv("specs.csv")

# Merge the dataframes on the 'mmsi' column
merged_df = pd.merge(input_df, specs_df[['mmsi', 'type', 'type_specific']], left_on='Navire_AIS', right_on='mmsi', how='left')

# Save the result to a new CSV file
merged_df.to_csv("annotations_mmsi_type.csv", index=False)