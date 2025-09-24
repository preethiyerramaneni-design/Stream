
import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path

# Folder containing .nc files
data_folder = Path("/Users/yasaswininarreddy/Desktop/Stream/argo_data")
output_file = data_folder / "argo_master_clean.csv"

# List all .nc files
nc_files = list(data_folder.glob("*.nc"))

if not nc_files:
    raise FileNotFoundError("No .nc files found in the folder!")

all_records = []

for nc_file in nc_files:
    print(f"📂 Processing {nc_file.name}...")
    
    try:
        ds = xr.open_dataset(nc_file)

        # Extract variables
        time_var = ds.get("JULD") or ds.get("TIME")
        temp_var = ds.get("TEMP")
        sal_var = ds.get("PSAL")
        pres_var = ds.get("PRES")
        float_id = str(ds.get("PLATFORM_NUMBER").values[0]) if "PLATFORM_NUMBER" in ds.variables else nc_file.stem

        if time_var is None or temp_var is None or sal_var is None or pres_var is None:
            print(f"⚠️ Skipping {nc_file.name}: required variables not found")
            continue

        # Handle time
        if np.issubdtype(time_var.dtype, np.number):
            times = pd.to_datetime("1950-01-01") + pd.to_timedelta(time_var.values, unit="D")
        else:
            times = pd.to_datetime(time_var.values)

        # Flatten and append records
        n_profiles, n_levels = pres_var.shape
        for t_idx in range(n_profiles):
            for lvl in range(n_levels):
                all_records.append({
                    "float_id": float_id,
                    "time": times[t_idx],
                    "depth_dbar": pres_var.values[t_idx, lvl],
                    "temperature_C": temp_var.values[t_idx, lvl],
                    "salinity_psu": sal_var.values[t_idx, lvl]
                })

    except Exception as e:
        print(f"❌ Error processing {nc_file.name}: {e}")

# Create master DataFrame
master_df = pd.DataFrame(all_records)
master_df = master_df.dropna()

# Save as single CSV
master_df.to_csv(output_file, index=False)
print(f"\n✅ All files combined! Master CSV saved at: {output_file}")
print(master_df.head())

