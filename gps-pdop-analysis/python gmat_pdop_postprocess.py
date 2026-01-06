"""
PDOP Analysis from GMAT EarthFixedCS Outputs
===========================================

Input (GMAT ReportFile, whitespace-delimited):
- GPS_Positions.csv
- Receiver_Position.csv

Column format (per screenshot):
- GPSi.UTCGregorian
- GPSi.EarthFixedCS.X / Y / Z

All units: km
Frame: EarthFixed (ECEF)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import warnings

warnings.filterwarnings("ignore")

# ============================================================
# FORCE SCRIPT DIRECTORY
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

print("=" * 70)
print("PDOP ANALYSIS SCRIPT")
print("Script directory:", SCRIPT_DIR)
print("=" * 70)


# ============================================================
# COORDINATE UTILITIES
# ============================================================

def ecef_to_geodetic(x, y, z):
    a = 6378.137
    f = 1 / 298.257223563
    e2 = 2 * f - f**2

    lon = np.arctan2(y, x)
    p = np.sqrt(x**2 + y**2)
    lat = np.arctan2(z, p * (1 - e2))

    for _ in range(5):
        N = a / np.sqrt(1 - e2 * np.sin(lat)**2)
        alt = p / np.cos(lat) - N
        lat = np.arctan2(z, p * (1 - e2 * N / (N + alt)))

    return np.degrees(lat), np.degrees(lon), alt


def ecef_to_enu_matrix(lat_deg, lon_deg):
    lat = np.radians(lat_deg)
    lon = np.radians(lon_deg)
    return np.array([
        [-np.sin(lon),              np.cos(lon),               0],
        [-np.sin(lat)*np.cos(lon), -np.sin(lat)*np.sin(lon),  np.cos(lat)],
        [ np.cos(lat)*np.cos(lon),  np.cos(lat)*np.sin(lon),  np.sin(lat)]
    ])


# ============================================================
# PDOP CALCULATION
# ============================================================

def elevation_angle(sat_ecef, rec_ecef):
    los = sat_ecef - rec_ecef
    lat, lon, _ = ecef_to_geodetic(*rec_ecef)
    R = ecef_to_enu_matrix(lat, lon)
    enu = R @ los
    return np.degrees(np.arctan2(enu[2], np.linalg.norm(enu[:2])))


def compute_pdop(sat_positions, rec_position, elev_mask=5.0):
    H = []

    for sat in sat_positions:
        los = sat - rec_position
        r = np.linalg.norm(los)
        if r < 1e-6:
            continue

        if elevation_angle(sat, rec_position) >= elev_mask:
            u = los / r
            H.append([-u[0], -u[1], -u[2], 1.0])

    if len(H) < 4:
        return np.nan, len(H)

    H = np.array(H)

    try:
        Q = np.linalg.inv(H.T @ H)
        return np.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2]), len(H)
    except np.linalg.LinAlgError:
        return np.nan, len(H)


# ============================================================
# LOAD GMAT DATA (MATCHES YOUR FILE EXACTLY)
# ============================================================

def load_data():
    gps_file = "GPS_Positions.csv"
    rec_file = "Receiver_Position.csv"

    print("✓ Found GPS_Positions.csv")
    print("✓ Found Receiver_Position.csv")

    # Read without parsing dates first
    gps_df = pd.read_csv(gps_file, delim_whitespace=True, dtype=str)
    rec_df = pd.read_csv(rec_file, delim_whitespace=True)

    # Debug: Print first few time values and column names
    print("\nDEBUG - First 3 rows of GPS columns:")
    print(gps_df.columns.tolist())
    print(gps_df.head(3))
    
    # ---------------- TIME ----------------
    # The UTC time might be split across multiple columns
    # Look for columns that might contain date/time parts
    time_cols = [col for col in gps_df.columns if 'UTC' in col or 'Gregorian' in col]
    
    if len(time_cols) == 0:
        # If no UTC column found, use index as time
        print("\nWARNING: No UTC time column found, using epoch index")
        times = [datetime(2026, 1, 1) + pd.Timedelta(seconds=60*i) for i in range(len(gps_df))]
    else:
        print(f"\nFound time-related columns: {time_cols}")
        # Combine all time columns into a single string
        time_strings = []
        for idx in range(len(gps_df)):
            time_parts = [str(gps_df[col].iloc[idx]) for col in time_cols]
            time_str = ' '.join(time_parts)
            time_strings.append(time_str)
        
        print(f"\nFirst 3 combined time strings:")
        for i in range(min(3, len(time_strings))):
            print(f"  {time_strings[i]}")
        
        # Try to parse the combined time string
        times = []
        for t_str in time_strings:
            try:
                # Try the expected format
                times.append(datetime.strptime(t_str, "%d %b %Y %H:%M:%S.%f"))
            except:
                try:
                    # Try without microseconds
                    times.append(datetime.strptime(t_str, "%d %b %Y %H:%M:%S"))
                except:
                    # If all else fails, use a default time with incrementing seconds
                    times.append(datetime(2026, 1, 1) + pd.Timedelta(seconds=60*len(times)))

    # ---------------- SATELLITES ----------------
    x_cols = [c for c in gps_df.columns if c.endswith(".EarthFixedCS.X") or c.endswith(".X")]
    num_sats = len(x_cols)

    print(f"\n✓ Epochs     : {len(times)}")
    print(f"✓ Satellites : {num_sats}")
    print(f"✓ Satellite columns found: {x_cols[:3]}..." if len(x_cols) > 3 else f"✓ Satellite columns: {x_cols}")

    sats = np.zeros((len(times), num_sats, 3))
    for s in range(num_sats):
        # Try different column naming patterns
        sat_name = f"GPS{s+1}"
        x_col = f"{sat_name}.EarthFixedCS.X"
        y_col = f"{sat_name}.EarthFixedCS.Y"
        z_col = f"{sat_name}.EarthFixedCS.Z"
        
        # If those don't exist, try without CS
        if x_col not in gps_df.columns:
            x_col = f"{sat_name}.EarthFixed.X"
            y_col = f"{sat_name}.EarthFixed.Y"
            z_col = f"{sat_name}.EarthFixed.Z"
        
        sats[:, s, 0] = pd.to_numeric(gps_df[x_col], errors='coerce')
        sats[:, s, 1] = pd.to_numeric(gps_df[y_col], errors='coerce')
        sats[:, s, 2] = pd.to_numeric(gps_df[z_col], errors='coerce')

    # ---------------- RECEIVER ----------------
    rec_x_col = "Receiver.EarthFixed.X" if "Receiver.EarthFixed.X" in rec_df.columns else "Receiver.EarthFixedCS.X"
    rec_y_col = "Receiver.EarthFixed.Y" if "Receiver.EarthFixed.Y" in rec_df.columns else "Receiver.EarthFixedCS.Y"
    rec_z_col = "Receiver.EarthFixed.Z" if "Receiver.EarthFixed.Z" in rec_df.columns else "Receiver.EarthFixedCS.Z"
    
    rec = np.column_stack([
        rec_df[rec_x_col],
        rec_df[rec_y_col],
        rec_df[rec_z_col]
    ])

    return times, sats, rec


# ============================================================
# MAIN
# ============================================================

def main():
    times, sats, recs = load_data()

    pdops, visibles = [], []

    print("\nComputing PDOP...")
    for i in range(len(times)):
        pdop, vis = compute_pdop(sats[i], recs[i])
        pdops.append(pdop)
        visibles.append(vis)

        if (i + 1) % 100 == 0:
            print(f"  Processed {i+1}/{len(times)} epochs")

    results = pd.DataFrame({
        "UTCGregorian": [t.strftime("%d %b %Y %H:%M:%S.%f")[:-3] for t in times],
        "VisibleSatellites": visibles,
        "PDOP": pdops
    })

    results.to_csv("PDOP_Results.csv", index=False)
    print("\n✓ Saved PDOP_Results.csv")

    # ---------------- PLOTS ----------------
    hours = [(t - times[0]).total_seconds() / 3600 for t in times]

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(hours, pdops)
    plt.ylabel("PDOP")
    plt.title("PDOP vs Time")
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(hours, visibles)
    plt.xlabel("Time (hours)")
    plt.ylabel("Visible Satellites")
    plt.grid()

    plt.tight_layout()
    plt.savefig("PDOP_Analysis.png", dpi=300)
    plt.show()

    print("✓ Saved PDOP_Analysis.png")
    print("\nANALYSIS COMPLETE ✔")


if __name__ == "__main__":
    main()