import pandas as pd
from pathlib import Path

# Load the CSV (from preprocessing step)
csv_file = Path("argo_data/argo_master_clean.csv")
df = pd.read_csv(csv_file)

# If 'float_id' doesn't exist, create a dummy float ID
if 'float_id' not in df.columns:
    df['float_id'] = 'float_1'  # for single file, later use real IDs for multiple floats

# Generate metadata summaries
metadata = df.groupby('float_id').apply(
    lambda x: f"Float {x.float_id.iloc[0]}, {len(x)} measurements, "
              f"Depth range: {x.depth_dbar.min():.1f}-{x.depth_dbar.max():.1f} m, "
              f"Temperature range: {x.temperature_C.min():.2f}-{x.temperature_C.max():.2f} °C, "
              f"Salinity range: {x.salinity_psu.min():.2f}-{x.salinity_psu.max():.2f} PSU"
).reset_index(name='summary')

# Save metadata CSV for vector DB
metadata_file = Path("argo_data/argo_metadata.csv")
metadata.to_csv(metadata_file, index=False)

print(f"✅ Metadata saved: {metadata_file}")
print(metadata.head())