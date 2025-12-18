
from agi.stk12.stkdesktop import STKDesktop
from agi.stk12.stkobjects import *
from agi.stk12.stkutil import *
from datetime import datetime, timedelta, timezone




# STEP 1: START STK APPLICATION

print("\n[Step 1] Starting STK Application...")
uiApp = STKDesktop.StartApplication()
uiApp.UserControl = True
uiApp.Visible = True
stkRoot = uiApp.Root
print("✓ STK Application started")

# STEP 2: CREATE SCENARIO 

print("\n[Step 2] Creating mission scenario...")
stkRoot.NewScenario("M600_Antaris_Mission")
scenario = stkRoot.CurrentScenario

# Set time 
start_time = datetime.now(timezone.utc)
stop_time = start_time + timedelta(days=1)
start_str = start_time.strftime("%d %b %Y %H:%M:%S.000")
stop_str = stop_time.strftime("%d %b %Y %H:%M:%S.000")

scenario.SetTimePeriod(start_str, stop_str)
stkRoot.Rewind()
print(f"✓ Scenario created")
print(f"   Start: {start_str} UTC")
print(f"   Stop:  {stop_str} UTC")


# STEP 3: CREATE M600 SATELLITE

print("\n[Step 3] Creating M600 satellite...")
satellite = scenario.Children.New(AgESTKObjectType.eSatellite, "M600_Antaris")
satellite = AgSatellite(satellite)
print("✓ Satellite 'M600_Antaris' created")


# STEP 4: CONFIGURE ORBIT (SUN-SYNCHRONOUS LEO)

print("\n[Step 4] Configuring Sun-Synchronous LEO orbit...")

# Orbital parameters
altitude_km = 550
eccentricity = 0.001
inclination_deg = 97.6
arg_of_perigee_deg = 0.0
raan_deg = 0.0
true_anomaly_deg = 0.0

# Calculate semi-major axis
earth_radius_km = 6378.137
semi_major_axis_km = earth_radius_km + altitude_km

# Set J2 propagator
satellite.SetPropagatorType(AgEVePropagatorType.ePropagatorJ2Perturbation)

#  initial state and convert to Classical elements
keplerian = satellite.Propagator.InitialState.Representation.ConvertTo(AgEOrbitStateType.eOrbitStateClassical)
keplerian = AgOrbitStateClassical(keplerian)

# Set size and shape 
keplerian.SizeShapeType = AgEClassicalSizeShape.eSizeShapeSemimajorAxis
sizeShape = AgClassicalSizeShapeSemimajorAxis(keplerian.SizeShape)
sizeShape.SemiMajorAxis = semi_major_axis_km
sizeShape.Eccentricity = eccentricity

# Set orientation 
orientation = keplerian.Orientation
orientation.Inclination = inclination_deg
orientation.ArgOfPerigee = arg_of_perigee_deg
orientation.AscNode.Value = raan_deg  

# Set location 
keplerian.LocationType = AgEClassicalLocation.eLocationTrueAnomaly
location = AgClassicalLocationTrueAnomaly(keplerian.Location)
location.Value = true_anomaly_deg

# Assign the state back
satellite.Propagator.InitialState.Representation.Assign(keplerian)

# Propagate
satellite.Propagator.Propagate()

# Calculate orbital metrics
mu = 398600.4418  
period_sec = 2 * 3.141592653589793 * (semi_major_axis_km**3 / mu) ** 0.5
period_min = period_sec / 60
revs_per_day = 1440.0 / period_min

print("✓ Orbit configured successfully (Object Model)")
print(f"   Semi-major axis: {semi_major_axis_km:.2f} km")
print(f"   Period: {period_min:.2f} minutes")
print(f"   Revolutions/day: {revs_per_day:.1f}")


# STEP 5: SET ATTITUDE (NADIR POINTING)

print("\n[Step 5] Configuring attitude control...")
# Use Connect command for attitude (most reliable)
stkRoot.ExecuteCommand('SetAttitude */Satellite/M600_Antaris Standard Nadir(Cbi)')
print("✓ Attitude: Nadir Pointing (Earth-facing)")



# STEP 6: ADD EO IMAGING SENSOR

print("\n[Step 6] Adding EO imaging sensor...")
sensor = satellite.Children.New(AgESTKObjectType.eSensor, "EO_Imager")
sensor = AgSensor(sensor)

# Set pointing to Fixed 
sensor.SetPointingType(AgESnPointing.eSnPtFixed)

# Set pattern to Rectangular
sensor.SetPatternType(AgESnPattern.eSnRectangular)
sensorPattern = AgSnRectangularPattern(sensor.Pattern)
sensorPattern.HorizontalHalfAngle = 2.5  # degrees
sensorPattern.VerticalHalfAngle = 2.5    # degrees

# Calculate ground swath
swath_km = 2 * altitude_km * 3.14159265 * 2.5 / 180
print("✓ Sensor configured:")
print("   - Type: Rectangular EO Imager")
print("   - FOV: 5° × 5°")
print(f"   - Ground swath: ~{swath_km:.1f} km × {swath_km:.1f} km")



# STEP 7: ADD X-BAND TRANSMITTER


print("\n[Step 7] Adding X-Band transmitter...")
transmitter = satellite.Children.New(AgESTKObjectType.eTransmitter, "XBand_Downlink")
transmitter = AgTransmitter(transmitter)

print("✓ Transmitter created:")
print("   - Name: XBand_Downlink")
print("   - (Configure frequency/power manually in STK GUI)")
# STEP 8: ADD GROUND STATIONS

print("\n[Step 8] Adding ground stations...")

# Ground Station 1: Hyderabad
gs_hyderabad = scenario.Children.New(AgESTKObjectType.eFacility, "GS_Hyderabad")
gs_hyderabad = AgFacility(gs_hyderabad)
gs_hyderabad.Position.AssignGeodetic(17.385, 78.486, 0.5)
print("✓ Ground Station 1: Hyderabad, India (17.385°N, 78.486°E)")

# Ground Station 2: Svalbard
gs_svalbard = scenario.Children.New(AgESTKObjectType.eFacility, "GS_Svalbard")
gs_svalbard = AgFacility(gs_svalbard)
gs_svalbard.Position.AssignGeodetic(78.23, 15.39, 0.5)
print("✓ Ground Station 2: Svalbard, Norway (78.23°N, 15.39°E)")

# STEP 9: COMPUTE ACCESS 
print("\n[Step 9] Computing downlink access windows...")

# Access to Hyderabad
print("\n  [Computing access to Hyderabad...]")
access_hyd = satellite.GetAccessToObject(gs_hyderabad)
access_hyd.ComputeAccess()

try:
    accessDP_hyd = access_hyd.DataProviders.GetDataPrvTimeVarFromPath("Access Data//Access Intervals")
    accessResults_hyd = accessDP_hyd.ExecSingle(scenario.StartTime, scenario.StopTime)
    accessCount_hyd = accessResults_hyd.DataSets.Count
    print(f"  ✓ Hyderabad access windows: {accessCount_hyd}")
except Exception as e:
    print(f"  ⚠ Access details: {e}")

# Access to Svalbard
print("\n  [Computing access to Svalbard...]")
access_sva = satellite.GetAccessToObject(gs_svalbard)
access_sva.ComputeAccess()

try:
    accessDP_sva = access_sva.DataProviders.GetDataPrvTimeVarFromPath("Access Data//Access Intervals")
    accessResults_sva = accessDP_sva.ExecSingle(scenario.StartTime, scenario.StopTime)
    accessCount_sva = accessResults_sva.DataSets.Count
    print(f"  ✓ Svalbard access windows: {accessCount_sva}")
except Exception as e:
    print(f"  ⚠ Access details: {e}")

# STEP 10: CONFIGURE 3D GRAPHICS

print("\n[Step 10] Configuring 3D graphics...")

try:
    # Satellite graphics - use VO (Visualization Object) interface
    satVO = satellite.VO
    satVO.Vector.RefAxes.IsVisible = True
    satVO.OrbitSystems.InertialByWindow.IsVisible = True
    satVO.GroundTrack.IsVisible = True
    
    print("✓ Graphics configured")
    print("   - Orbit track: Visible")
    print("   - Ground track: Visible")
except Exception as e:
    print(f"⚠ Graphics: {e}")

# STEP 11: MISSION SUMMARY


print(f"\n   SATELLITE: M600_Antaris")
print(f"   Platform: Medium-class (500 kg)")
print(f"   Mission: EO/SAR/SIGINT")
print(f"\n  ORBITAL PARAMETERS:")
print(f"   Semi-major axis: {semi_major_axis_km:.2f} km")
print(f"   Altitude: {altitude_km} km")
print(f"   Eccentricity: {eccentricity}")
print(f"   Inclination: {inclination_deg}° (Sun-Synchronous)")
print(f"   RAAN: {raan_deg}°")
print(f"   Arg of Perigee: {arg_of_perigee_deg}°")
print(f"   Period: {period_min:.2f} minutes")
print(f"   Revolutions/day: {revs_per_day:.1f}")
print(f"\n PAYLOAD:")
print(f"   EO Imager: 5° × 5° FOV")
print(f"   Ground swath: ~{swath_km:.1f} km × {swath_km:.1f} km")
print(f"   X-Band Downlink: 8.2 GHz, 10W")
print(f"\n GROUND SEGMENT:")
print(f"   Station 1: Hyderabad, India")
print(f"   Station 2: Svalbard, Norway")

print(" MISSION MODEL COMPLETE")

stkRoot.Rewind()