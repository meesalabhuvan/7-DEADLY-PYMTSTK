# Sanyark Space - Global Coverage Analysis System

## 🛰️ Project Overview

This project provides comprehensive coverage analysis for **Sanyark Space**, a company building the essential space backbone for secure and autonomous PNT (Positioning, Navigation, and Timing) and M2M/IoT Communications from a unified LEO constellation.

The system analyzes satellite constellation coverage across six major global regions, identifying outages, computing access statistics, and generating detailed reports for mission planning and optimization.

---

## 📋 Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Output Files](#output-files)
- [Understanding the Results](#understanding-the-results)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### Coverage Analysis
- **6 Continental Regions**: North America, South America, Europe, Africa, Asia, Australia
- **Real-time Coverage Metrics**: Average, minimum, and maximum coverage percentages
- **Outage Detection**: Identifies when and where signal gaps occur
- **Timing Analysis**: Calculates outage duration and frequency

### Satellite Constellation Modeling
- **Multi-plane Architecture**: Configurable number of orbital planes
- **Distributed Coverage**: Phase-shifted satellites for optimal coverage
- **Realistic Propagation**: J2 perturbation modeling for accurate orbital mechanics
- **Sensor Simulation**: 62.5° field-of-view sensors for ground coverage

### Detailed Reporting
- **Coverage Statistics**: Per-region coverage percentages and access counts
- **Satellite Assignments**: Which satellites cover which regions most
- **Gap Analysis**: Complete list of coverage outages with start/end times
- **Visual STK Scenario**: Interactive 3D visualization in AGI STK

---

## 🖥️ System Requirements

### Software Requirements
- **AGI STK 12** (Systems Tool Kit)
- **Python 3.7+**
- **agi.stk12** Python module (installed with STK)

### Python Libraries
```
numpy
datetime
agi.stk12.stkdesktop
agi.stk12.stkobjects
agi.stk12.stkutil
agi.stk12.utilities.colors
```

### Hardware Recommendations
- **RAM**: 8GB minimum, 16GB recommended
- **CPU**: Multi-core processor (computation-intensive)
- **Storage**: 2GB free space for scenario and output files

---

## 📦 Installation

1. **Install AGI STK 12**
   - Download from [AGI's website](https://www.agi.com/)
   - Ensure Python integration is enabled during installation

2. **Verify Python Module**
   ```bash
   python -c "import agi.stk12"
   ```
   If this fails, add STK's Python directory to your PATH

3. **Clone/Download the Script**
   ```bash
   # Place gobal_6_continent_analysis.py in your working directory
   ```

4. **Install NumPy** (if not already installed)
   ```bash
   pip install numpy
   ```

---

## ⚙️ Configuration

### Constellation Parameters

Edit these values at the top of the script to customize your constellation:

```python
# Constellation design 
NUM_PLANES = 4              # Number of orbital planes
SATS_PER_PLANE = 8          # Satellites per plane (Total: 32)
ALTITUDE_KM = 788           # Orbital altitude in kilometers
INCLINATION_DEG = 86.4      # Orbital inclination (near-polar)

# Time period
START_TIME = "1 Jun 2022 15:00:00.000"
STOP_TIME = "2 Jun 2022 15:00:00.000"  # 1-day analysis

# Coverage resolution
COVERAGE_RESOLUTION = 10    # Grid resolution (degrees)
```

### Coverage Regions

Pre-configured regions (can be modified):

| Region | Latitude Range | Longitude Range |
|--------|----------------|-----------------|
| North America | 25° to 70°N | -170° to -50° |
| South America | -55° to 15° | -85° to -35° |
| Europe | 35° to 70°N | -10° to 40° |
| Africa | -35° to 37° | -20° to 52° |
| Asia | 0° to 75°N | 40° to 180° |
| Australia | -45° to -10° | 110° to 155° |

---

## 🚀 Usage

### Basic Usage

1. **Run the Script**
   ```bash
   python gobal_6_continent_analysis.py
   ```

2. **Wait for Completion**
   - Satellite creation: ~1-2 minutes
   - Coverage computation: ~5-10 minutes per region
   - Total runtime: ~30-45 minutes

3. **Review Results**
   - Check console output for real-time progress
   - Open generated text files for detailed reports
   - Explore STK GUI for visual analysis

### Console Output Example

```
Starting STK application
STK started successfully

Creating scenario
Scenario time: 1 Jun 2022 15:00:00.000 to 2 Jun 2022 15:00:00.000

CREATING SATELLITE CONSTELLATION
Created 32 satellites with sensors

CREATING COVERAGE DEFINITIONS
Creating coverage for: North_America
  Computing coverage for North_America...
  Coverage computed successfully for North_America

ANALYZING COVERAGE STATISTICS
REGION: North_America
  Average Coverage: 87.34%
  Minimum Coverage: 65.12%
  Maximum Coverage: 100.00%
  Total Access Intervals: 1247
```

---

## 📊 Output Files

The script generates three detailed report files:

### 1. `global_coverage_summary.txt`
**Purpose**: Overview of coverage performance for all regions

**Contents**:
- Constellation configuration
- Average/min/max coverage percentages per region
- Number of access intervals
- Coverage gap counts
- Worst coverage gap percentage

**Example**:
```
REGIONAL COVERAGE RESULTS:

North_America:
  Average Coverage: 87.34%
  Min Coverage: 65.12%
  Max Coverage: 100.00%
  Total Accesses: 1247
  Coverage Gaps: 234
  Worst Gap: 34.88%
```

### 2. `satellite_assignments.txt`
**Purpose**: Shows which satellites contribute most to each region

**Contents**:
- Top 10 satellites per region
- Coverage percentage contribution
- Ranked by effectiveness

**Use Case**: Optimize satellite placement or identify underperforming satellites

**Example**:
```
North_America:
Rank   Satellite            Coverage %
1      Sensor11             15.32
2      Sensor24             14.87
3      Sensor13             13.45
```

### 3. `timing_outage_analysis.txt`
**Purpose**: Detailed timeline of coverage gaps

**Contents**:
- Number of coverage gaps
- Maximum gap duration (minutes)
- Average gap duration
- Start/end time for each gap
- Gap duration in seconds and minutes

**Use Case**: Critical for understanding when service is unavailable

**Example**:
```
North_America:
  Number of Coverage Gaps: 12
  Maximum Gap: 4.32 minutes
  Average Gap: 2.15 minutes

  Gap #1:
    Start: 1 Jun 2022 15:23:45.000
    End: 1 Jun 2022 15:27:12.000
    Duration: 3.45 minutes (207.00 seconds)
```

---

## 🔍 Understanding the Results

### Coverage Metrics Explained

**Average Coverage**: 
- Percentage of time the region has at least one satellite visible
- **Target**: >95% for commercial IoT, >99% for critical PNT

**Coverage Gaps**:
- Periods when coverage drops below 100%
- Does NOT mean zero coverage (use Gap Analysis for that)

**Access Intervals**:
- Number of times satellites pass over the region
- Higher = more redundancy and handoff opportunities

### Interpreting Gap Analysis

**Complete Coverage Gaps** (from timing_outage_analysis.txt):
- Times when the region has 0% coverage
- Critical for mission planning
- Target: <5 minutes for commercial, <1 minute for critical

**Partial Gaps** (from global_coverage_summary.txt):
- Coverage exists but below 100%
- Multiple satellites may still be visible
- Less critical but affects redundancy

### Satellite Assignment Insights

**Top Contributing Satellites**:
- High percentage = satellite frequently serves this region
- Use to optimize ground station placement
- Identify satellites for regional service prioritization

---

## 🛠️ Customization

### Adding New Regions

Add to the `COVERAGE_REGIONS` list:

```python
COVERAGE_REGIONS.append({
    "name": "Middle_East",
    "lat_min": 15,
    "lat_max": 45,
    "lon_min": 35,
    "lon_max": 75
})
```

### Changing Sensor FOV

Modify sensor creation:

```python
sensor.CommonTasks.SetPatternSimpleConic(70.0, 2.0)  # 70° half-angle
```

### Extending Analysis Period

```python
START_TIME = "1 Jun 2022 00:00:00.000"
STOP_TIME = "8 Jun 2022 00:00:00.000"  # 7-day analysis
```

**Note**: Longer periods = longer computation time (linear scaling)

### Grid Resolution

Higher resolution = more accurate but slower:

```python
COVERAGE_RESOLUTION = 5   # 5° grid (more detailed)
COVERAGE_RESOLUTION = 20  # 20° grid (faster but coarser)
```

---

## 🐛 Troubleshooting

### Common Issues

**1. STK Fails to Start**
```
Error: Failed to start STK
```
**Solution**: 
- Ensure STK 12 is installed
- Check that no other STK instance is running
- Restart your computer if needed

**2. "Invalid object path" Error**
```
STKRuntimeError: Invalid object path
```
**Solution**: 
- This usually occurs with sensor pointing
- Check that objects are created before referencing
- Verify object names don't contain special characters

**3. Coverage Computation Hangs**
```
Computing coverage for North_America... [no progress]
```
**Solution**: 
- Reduce `COVERAGE_RESOLUTION` (try 15 or 20)
- Reduce number of satellites temporarily
- Check CPU usage - may just be slow

**4. Memory Issues**
```
MemoryError or system becomes unresponsive
```
**Solution**: 
- Close other applications
- Reduce analysis duration (1 day instead of 7)
- Reduce coverage resolution
- Analyze regions one at a time

### Performance Tips

- **Start Small**: Test with 2 planes, 4 satellites per plane
- **Short Duration**: Begin with 1-day analysis
- **Coarse Grid**: Use 15-20° resolution for initial tests
- **Monitor Progress**: Watch console for errors early

---

## 📈 Typical Results

Based on the default configuration (32 satellites, 788 km, 86.4° inclination):

| Region | Expected Avg Coverage | Expected Max Gap |
|--------|----------------------|------------------|
| North America | 85-90% | 3-5 minutes |
| Europe | 85-92% | 2-4 minutes |
| Asia | 80-88% | 4-6 minutes |
| Australia | 75-85% | 5-8 minutes |
| South America | 78-85% | 5-7 minutes |
| Africa | 82-88% | 3-6 minutes |

**Higher latitudes** generally have better coverage due to polar orbit inclination.

---

## 🎯 Mission Applications

### PNT Services
- **Navigation Backup**: Identify GPS-denied periods
- **Timing Distribution**: Plan for continuous time sync
- **Position Accuracy**: Ensure multi-satellite visibility

### IoT/M2M Communications
- **Data Uplink Planning**: Schedule transmissions during coverage
- **Store-and-Forward**: Size buffers based on max gap duration
- **Quality of Service**: Guarantee coverage SLAs per region

### Network Planning
- **Ground Station Placement**: Optimize using satellite assignments
- **Link Budget Analysis**: Factor in elevation angles and range
- **Handoff Strategy**: Plan satellite transitions using gap analysis

---

## 📞 Support and Contribution

### Getting Help
- Review console output for specific error messages
- Check STK documentation: [AGI Help](https://help.agi.com/)
- Verify Python/STK integration is working

### Reporting Issues
When reporting problems, include:
1. Full error message
2. Configuration parameters used
3. STK version
4. Python version
5. Console output (last 50 lines)


## 🚀 Quick Start Checklist

- [ ] STK 12 installed and licensed
- [ ] Python 3.7+ with numpy
- [ ] agi.stk12 module verified
- [ ] Script downloaded to working directory
- [ ] Configuration reviewed (satellites, time period)
- [ ] 2GB+ free disk space
- [ ] No other STK instances running
- [ ] Ready to run: `python gobal_6_continent_analysis.py`


---

**Build the future of autonomous space infrastructure with Sanyark Space! 🛰️🌍**
