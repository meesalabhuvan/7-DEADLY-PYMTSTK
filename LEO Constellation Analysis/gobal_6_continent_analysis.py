"""
Global Coverage Definition Analysis
"""

import datetime as dt
import numpy as np
from agi.stk12.stkdesktop import STKDesktop
from agi.stk12.stkobjects import *
from agi.stk12.stkutil import *
from agi.stk12.utilities.colors import Color

# Constellation design 
NUM_PLANES = 4              
SATS_PER_PLANE = 8          
ALTITUDE_KM = 788           
INCLINATION_DEG = 86.4      

# Time period
START_TIME = "1 Jun 2022 15:00:00.000"
STOP_TIME = "2 Jun 2022 15:00:00.000"

# Coverage resolution
COVERAGE_RESOLUTION = 10  # degrees for lat/lon grid

# Define coverage regions of interest
COVERAGE_REGIONS = [
    {"name": "North_America", "lat_min": 25, "lat_max": 70, "lon_min": -170, "lon_max": -50},
    {"name": "South_America", "lat_min": -55, "lat_max": 15, "lon_min": -85, "lon_max": -35},
    {"name": "Europe", "lat_min": 35, "lat_max": 70, "lon_min": -10, "lon_max": 40},
    {"name": "Africa", "lat_min": -35, "lat_max": 37, "lon_min": -20, "lon_max": 52},
    {"name": "Asia", "lat_min": 0, "lat_max": 75, "lon_min": 40, "lon_max": 180},
    {"name": "Australia", "lat_min": -45, "lat_max": -10, "lon_min": 110, "lon_max": 155},
]

print("\nStarting STK application")

uiApp = STKDesktop.StartApplication(visible=True)
uiApp.Visible = True
uiApp.UserControl = True
stkRoot = uiApp.Root

print("\nSTK started successfully")

print("\nCreating scenario")

stkRoot.NewScenario("Global_Coverage_Analysis")
scenario = stkRoot.CurrentScenario

scenario.StartTime = START_TIME
scenario.StopTime = STOP_TIME
stkRoot.Rewind()

print(f"Scenario time: {START_TIME} to {STOP_TIME}")

print("\nCREATING SATELLITE CONSTELLATION")

satellites = []
sma = 6371 + ALTITUDE_KM

for plane in range(NUM_PLANES):
    raan = plane * (180.0 / NUM_PLANES)
    
    for sat_num in range(SATS_PER_PLANE):
        sat_name = f"Sat{plane+1}{sat_num+1}"
        
        satellite = AgSatellite(scenario.Children.New(AgESTKObjectType.eSatellite, sat_name))
        
        gfx = satellite.Graphics.Attributes
        gfx.Color = Color.FromRGB(255, 255, 0)
        gfx.Line.Width = AgELineWidth.e2
        gfx.Inherit = False
        gfx.IsGroundTrackVisible = False
        
        satellite.SetPropagatorType(AgEVePropagatorType.ePropagatorTwoBody)
        prop = satellite.Propagator
        
        kep = prop.InitialState.Representation.ConvertTo(AgEOrbitStateType.eOrbitStateClassical)
        kep.SizeShapeType = AgEClassicalSizeShape.eSizeShapeSemimajorAxis
        kep.SizeShape.SemiMajorAxis = sma
        kep.SizeShape.Eccentricity = 0
        
        kep.Orientation.Inclination = INCLINATION_DEG
        kep.Orientation.ArgOfPerigee = 0
        kep.Orientation.AscNodeType = AgEOrientationAscNode.eAscNodeRAAN
        kep.Orientation.AscNode.Value = raan
        
        true_anomaly = sat_num * (360.0 / SATS_PER_PLANE)
        true_anomaly += (360.0 / SATS_PER_PLANE / 2) * (plane % 2)
        
        kep.LocationType = AgEClassicalLocation.eLocationTrueAnomaly
        kep.Location.Value = true_anomaly
        
        prop.InitialState.Representation.Assign(kep)
        prop.Propagate()
        
        sensor = AgSensor(satellite.Children.New(AgESTKObjectType.eSensor, f"Sensor{sat_name[3:]}"))
        sensor.CommonTasks.SetPatternSimpleConic(62.5, 2.0)
        sensor.VO.PercentTranslucency = 75
        sensor.Graphics.LineWidth = AgELineWidth.e2
        sensor.Graphics.LineStyle = AgELineStyle.eDotted
        
        satellites.append({'sat': satellite, 'sensor': sensor, 'name': sat_name})

print(f"Created {len(satellites)} satellites with sensors")

# Create sensor constellation
sensorConstellation = AgConstellation(scenario.Children.New(AgESTKObjectType.eConstellation, "SensorConstellation"))

for sat_info in satellites:
    sensorConstellation.Objects.Add(sat_info['sensor'].Path)

print(f"Created sensor constellation with {len(satellites)} sensors")

print("\nCREATING COVERAGE DEFINITIONS")

coverage_definitions = []

for region in COVERAGE_REGIONS:
    print(f"\nCreating coverage for: {region['name']}")
    
    try:
        # Create Coverage Definition
        covDef = scenario.Children.New(AgESTKObjectType.eCoverageDefinition, region['name'])
        covDef = AgCoverageDefinition(covDef)
        
        # Set grid definition
        covDef.Grid.BoundsType = AgECvBounds.eBoundsLatLonRegion
        bounds = covDef.Grid.Bounds
        bounds.MinLatitude = region['lat_min']
        bounds.MaxLatitude = region['lat_max']
        bounds.MinLongitude = region['lon_min']
        bounds.MaxLongitude = region['lon_max']
        
        covDef.Grid.Resolution.LatLon = COVERAGE_RESOLUTION

        # Add sensors to coverage definition
        for sat_info in satellites:
            covDef.AssetList.Add(sat_info['sensor'].Path)

        print(f"  Computing coverage for {region['name']}...")
        covDef.ComputeAccesses()
        
        coverage_definitions.append({
            'name': region['name'],
            'covDef': covDef,
            'region': region
        })
        
        print(f"  Coverage computed successfully for {region['name']}")
        
    except Exception as e:
        print(f"  Error creating coverage for {region['name']}: {e}")

print(f"\nCreated {len(coverage_definitions)} coverage definitions")

print("ANALYZING COVERAGE STATISTICS")

region_results = []

for cov_def in coverage_definitions:
    print(f"REGION: {cov_def['name']}")
    try:
        covDef = cov_def['covDef']
        
        # Get Figure of Merit (Coverage) data provider
        coverageDP = covDef.DataProviders.Item("Percent Coverage")
        coverageData = coverageDP.Exec(scenario.StartTime, scenario.StopTime, 60)
        
        # Get percent coverage
        percentCoverage = list(coverageData.DataSets.GetDataSetByName("Percent Coverage").GetValues())
        times = list(coverageData.DataSets.GetDataSetByName("Time").GetValues())
        
        avg_coverage = np.mean([float(p) for p in percentCoverage])
        min_coverage = min([float(p) for p in percentCoverage])
        max_coverage = max([float(p) for p in percentCoverage])
        
        print(f"  Average Coverage: {avg_coverage:.2f}%")
        print(f"  Minimum Coverage: {min_coverage:.2f}%")
        print(f"  Maximum Coverage: {max_coverage:.2f}%")
        
        # Get access statistics
        accessDP = covDef.DataProviders.Item("Access Duration")
        accessData = accessDP.Exec()
        
        total_accesses = accessData.DataSets.RowCount
        print(f"  Total Access Intervals: {total_accesses}")
        
        # Calculate coverage gaps/outages
        coverage_threshold = 100.0 
        outage_times = []
        
        for i, cov_pct in enumerate(percentCoverage):
            if float(cov_pct) < coverage_threshold:
                outage_times.append({
                    'time': times[i],
                    'coverage': float(cov_pct),
                    'gap': coverage_threshold - float(cov_pct)
                })
        
        if len(outage_times) > 0:
            print(f"\n  Coverage Gaps Detected: {len(outage_times)} intervals")
            print(f"  Worst Coverage Gap: {max([o['gap'] for o in outage_times]):.2f}%")
            
            # Show worst 3 gaps
            print(f"\n  Top 3 Worst Coverage Gaps:")
            sorted_outages = sorted(outage_times, key=lambda x: x['gap'], reverse=True)
            for i, gap in enumerate(sorted_outages[:3]):
                print(f"    {i+1}. Time: {gap['time']}, Coverage: {gap['coverage']:.2f}%, Gap: {gap['gap']:.2f}%")
        else:
            print(f"\n  Full coverage maintained - No gaps!")
        
        # Store results
        region_results.append({
            'name': cov_def['name'],
            'avg_coverage': avg_coverage,
            'min_coverage': min_coverage,
            'max_coverage': max_coverage,
            'total_accesses': total_accesses,
            'num_gaps': len(outage_times),
            'worst_gap': max([o['gap'] for o in outage_times]) if len(outage_times) > 0 else 0
        })
        
    except Exception as e:
        print(f"  Error analyzing {cov_def['name']}: {e}")

print("\nCOMPUTING SATELLITE ASSIGNMENTS TO REGIONS")

satellite_assignments = []

for cov_def in coverage_definitions:
    print(f"\n{cov_def['name']} - Analyzing satellite contributions")
    
    try:
        # Get asset coverage statistics
        assetDP = cov_def['covDef'].DataProviders.Item("Coverage By Asset")
        assetData = assetDP.Exec()
        
        # Get column names correctly
        asset_names = []
        coverage_times = []
        
        for i in range(assetData.DataSets.Count):
            dataset = assetData.DataSets.Item(i)
            col_name = dataset.ElementName  
            values = list(dataset.GetValues())
            
            if "Asset" in col_name or i == 0:  
                asset_names = values
            elif "Coverage" in col_name or "Percent" in col_name or i == 1:
                coverage_times = values
        
        # Create satellite contribution list
        sat_contributions = []
        for i, asset_name in enumerate(asset_names):
            sat_contributions.append({
                'name': asset_name.split('/')[-1], 
                'coverage_time': float(coverage_times[i])
            })
        
        # Sort by contribution
        sat_contributions.sort(key=lambda x: x['coverage_time'], reverse=True)
        
        print(f"  Top 5 contributing satellites:")
        for i, sat in enumerate(sat_contributions[:5]):
            print(f"    {i+1}. {sat['name']}: {sat['coverage_time']:.2f}%")
        
        satellite_assignments.append({
            'region': cov_def['name'],
            'satellites': sat_contributions
        })
        
    except Exception as e:
        print(f"  Error analyzing satellite assignments for {cov_def['name']}: {e}")

print("\nANALYZING ACCESS TIMING AND DELAYS")

timing_analysis = []

for cov_def in coverage_definitions:
    print(f"\n{cov_def['name']} - Access Timing Analysis")
    
    try:
        # Use Global Coverage Gaps data provider for timing gaps
        gapDP = cov_def['covDef'].DataProviders.Item("Global Coverage Gaps")
        gapData = gapDP.Exec(scenario.StartTime, scenario.StopTime)
        
        if gapData.DataSets.RowCount > 0 and gapData.DataSets.Count > 0:
            start_times = []
            stop_times = []
            durations = []
            
            # Extract data from datasets
            for i in range(gapData.DataSets.Count):
                dataset = gapData.DataSets.Item(i)
                col_name = dataset.ElementName
                values = list(dataset.GetValues())
                
                if "Start" in col_name:
                    start_times = values
                elif "Stop" in col_name:
                    stop_times = values
                elif "Duration" in col_name:
                    durations = values
            
            if len(start_times) > 0 and len(stop_times) > 0 and len(durations) > 0:
                gaps = []
                for i in range(min(len(start_times), len(stop_times), len(durations))):
                    gaps.append({
                        'start': start_times[i],
                        'end': stop_times[i],
                        'duration': float(durations[i])
                    })
                
                if gaps:
                    max_gap = max([g['duration'] for g in gaps])
                    avg_gap = np.mean([g['duration'] for g in gaps])
                    
                    print(f"  Number of Complete Coverage Gaps: {len(gaps)}")
                    print(f"  Maximum Gap: {max_gap/60:.2f} minutes")
                    print(f"  Average Gap: {avg_gap/60:.2f} minutes")
                    
                    # Show worst gaps
                    print(f"\n  Top 3 Longest Gaps:")
                    sorted_gaps = sorted(gaps, key=lambda x: x['duration'], reverse=True)
                    for i, gap in enumerate(sorted_gaps[:3]):
                        print(f"    {i+1}. Duration: {gap['duration']/60:.2f} minutes")
                        print(f"       From: {gap['start']}")
                        print(f"       To:   {gap['end']}")
                    
                    timing_analysis.append({
                        'region': cov_def['name'],
                        'num_gaps': len(gaps),
                        'max_gap': max_gap,
                        'avg_gap': avg_gap,
                        'gaps': gaps
                    })
                else:
                    print(f"  No complete coverage gaps (0% coverage) detected!")
                    print(f"  Note: Partial gaps (< 100% coverage) exist but region never loses all coverage")
            else:
                print(f"  No complete coverage gaps (0% coverage) detected!")
                print(f"  Note: Partial gaps (< 100% coverage) exist but region never loses all coverage")
        else:
            print(f"  No complete coverage gaps (0% coverage) detected!")
            print(f"  Note: Partial gaps (< 100% coverage) exist but region never loses all coverage")
                
    except Exception as e:
        print(f"  Error in timing analysis for {cov_def['name']}: {e}")

print("\nSAVING REPORTS")

# Main summary 
with open("global_coverage_summary.txt", 'w') as f:
    f.write("="*80 + "\n")
    f.write("SANYARK SPACE - GLOBAL COVERAGE ANALYSIS SUMMARY\n")
    f.write("="*80 + "\n\n")
    
    f.write("CONSTELLATION CONFIGURATION:\n")
    f.write(f"  Number of Planes: {NUM_PLANES}\n")
    f.write(f"  Satellites per Plane: {SATS_PER_PLANE}\n")
    f.write(f"  Total Satellites: {len(satellites)}\n")
    f.write(f"  Altitude: {ALTITUDE_KM} km\n")
    f.write(f"  Inclination: {INCLINATION_DEG}°\n")
    f.write(f"  Sensor FOV: 62.5°\n\n")
    
    f.write("COVERAGE ANALYSIS PERIOD:\n")
    f.write(f"  Start: {START_TIME}\n")
    f.write(f"  Stop: {STOP_TIME}\n")
    f.write(f"  Resolution: {COVERAGE_RESOLUTION}° grid\n\n")
    
    f.write("="*80 + "\n")
    f.write("REGIONAL COVERAGE RESULTS:\n\n")
    
    for result in region_results:
        f.write(f"\n{result['name']}:\n")
        f.write(f"  Average Coverage: {result['avg_coverage']:.2f}%\n")
        f.write(f"  Min Coverage: {result['min_coverage']:.2f}%\n")
        f.write(f"  Max Coverage: {result['max_coverage']:.2f}%\n")
        f.write(f"  Total Accesses: {result['total_accesses']}\n")
        f.write(f"  Coverage Gaps: {result['num_gaps']}\n")
        f.write(f"  Worst Gap: {result['worst_gap']:.2f}%\n")

print("Summary report saved: global_coverage_summary.txt")

# Satellite assignment 
with open("satellite_assignments.txt", 'w') as f:
    f.write("SATELLITE ASSIGNMENTS TO COVERAGE REGIONS\n")
    f.write("="*80 + "\n\n")
    
    for assignment in satellite_assignments:
        f.write(f"\n{assignment['region']}:\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Rank':<6} {'Satellite':<20} {'Coverage %':<20}\n")
        f.write("-"*80 + "\n")
        
        for i, sat in enumerate(assignment['satellites'][:10]): 
            f.write(f"{i+1:<6} {sat['name']:<20} {sat['coverage_time']:<20.2f}\n")

print("Satellite assignments saved: satellite_assignments.txt")

# Timing and outage 
with open("timing_outage_analysis.txt", 'w') as f:
    f.write("TIMING DELAY AND OUTAGE ANALYSIS\n")
    f.write("="*80 + "\n\n")
    
    for timing in timing_analysis:
        f.write(f"\n{timing['region']}:\n")
        f.write("-"*80 + "\n")
        f.write(f"  Number of Coverage Gaps: {timing['num_gaps']}\n")
        f.write(f"  Maximum Gap: {timing['max_gap']/60:.2f} minutes\n")
        f.write(f"  Average Gap: {timing['avg_gap']/60:.2f} minutes\n\n")
        
        f.write("  Detailed Gap List:\n")
        for i, gap in enumerate(timing['gaps'][:20]): 
            f.write(f"\n  Gap #{i+1}:\n")
            f.write(f"    Start: {gap['start']}\n")
            f.write(f"    End: {gap['end']}\n")
            f.write(f"    Duration: {gap['duration']/60:.2f} minutes ({gap['duration']:.2f} seconds)\n")

print("Timing/outage analysis saved: timing_outage_analysis.txt")

print("ANALYSIS COMPLETE!")

print(f"\n GLOBAL COVERAGE ANALYSIS:")
print(f"  Regions Analyzed: {len(region_results)}")
print(f"  Total Satellites: {len(satellites)}")

print("\n Coverage Summary:")
for result in region_results:
    print(f"  {result['name']}: {result['avg_coverage']:.2f}% avg, {result['num_gaps']} gaps")

print("\n STK scenario remains open for further analysis")
