# M600 Antaris Mission - Technical Report

## Executive Summary

This report documents the M600 Antaris satellite mission, a medium-class Earth observation platform designed for multi-intelligence gathering operations. The mission utilizes Systems Tool Kit (STK) for orbital simulation and analysis, implementing a sun-synchronous low Earth orbit (LEO) configuration optimized for continuous Earth monitoring capabilities.

**Mission Classification:** Earth Observation / Synthetic Aperture Radar / Signals Intelligence (EO/SAR/SIGINT)  
**Platform Class:** Medium (500 kg)  
**Orbital Regime:** Sun-Synchronous LEO  
**Mission Duration:** 24-hour simulation period  

---

## 1. Mission Objectives

The M600 Antaris mission is designed to achieve the following primary objectives:

### 1.1 Primary Objectives
- Continuous Earth observation coverage using electro-optical imaging systems
- High-resolution ground imaging with 5° × 5° field of view
- Reliable downlink communication through dual ground station architecture
- Demonstration of sun-synchronous orbit maintenance for consistent lighting conditions

### 1.2 Secondary Objectives
- Validation of X-band communication link budgets
- Assessment of ground station access windows and data throughput capacity
- Evaluation of nadir-pointing attitude control system performance

---

## 2. System Architecture

### 2.1 Space Segment

#### 2.1.1 Satellite Platform Specifications
- **Name:** M600_Antaris
- **Mass:** 500 kg (medium-class platform)
- **Mission Type:** Multi-intelligence (EO/SAR/SIGINT)
- **Design Life:** Not specified in simulation
- **Attitude Control:** Three-axis stabilized, nadir-pointing

#### 2.1.2 Payload Suite

**Electro-Optical (EO) Imager**
- **Type:** Rectangular pattern sensor
- **Field of View:** 5° × 5° (2.5° half-angles in both axes)
- **Ground Swath:** Approximately 96.2 km × 96.2 km at 550 km altitude
- **Pointing Mode:** Fixed (nadir-oriented)
- **Applications:** High-resolution Earth imaging, terrain mapping, change detection

**Communications Subsystem**
- **Downlink System:** X-Band transmitter
- **Designation:** XBand_Downlink
- **Frequency:** 8.2 GHz (X-band allocation)
- **Power Output:** 10W
- **Purpose:** High-rate data transmission to ground stations

### 2.2 Ground Segment

The mission employs a dual ground station architecture for maximizing contact opportunities and data retrieval:

#### Ground Station 1: Hyderabad, India
- **Location:** 17.385°N, 78.486°E
- **Elevation:** 0.5 km above MSL
- **Strategic Value:** Primary station for Indian subcontinent coverage
- **Access Windows:** Computed for 24-hour period

#### Ground Station 2: Svalbard, Norway  
- **Location:** 78.23°N, 15.39°E
- **Elevation:** 0.5 km above MSL
- **Strategic Value:** Polar station enabling high-latitude coverage and frequent passes
- **Access Windows:** Computed for 24-hour period

---

## 3. Orbital Design

### 3.1 Orbit Classification

The M600 Antaris operates in a sun-synchronous low Earth orbit, a specialized near-polar orbit where the orbital plane precesses at the same rate as the Earth's orbit around the Sun. This configuration ensures consistent solar illumination conditions for each pass over a given latitude.

### 3.2 Orbital Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Semi-major Axis | 6,928.14 km | Provides 550 km altitude above Earth's surface |
| Altitude | 550 km | Balance between resolution and orbit lifetime |
| Eccentricity | 0.001 | Near-circular orbit for consistent ground coverage |
| Inclination | 97.6° | Sun-synchronous condition at this altitude |
| Right Ascension of Ascending Node (RAAN) | 0.0° | Initial orbital plane orientation |
| Argument of Perigee | 0.0° | Circular orbit approximation |
| True Anomaly | 0.0° | Initial position in orbit |

### 3.3 Orbital Dynamics

**Orbital Period:** 95.68 minutes  
**Revolutions per Day:** 15.0  
**Ground Track Repeat Cycle:** Varies based on RAAN drift rate  

The orbital period of approximately 96 minutes enables 15 complete orbits per day, providing multiple opportunities for target revisits and ground station contacts.

### 3.4 Propagator Configuration

The mission simulation employs the **J2 Perturbation Propagator**, which accounts for:
- Earth's oblateness (J2 zonal harmonic)
- Gravitational perturbations affecting orbital elements
- Nodal precession required for sun-synchronous characteristics

This propagator provides sufficient accuracy for mission planning while maintaining computational efficiency.

---

## 4. Attitude Control System

### 4.1 Pointing Strategy

**Mode:** Nadir Pointing (Earth-facing)  
**Implementation:** Standard Nadir (Central Body Inertial frame)  
**Control Method:** Three-axis stabilized platform

### 4.2 Operational Benefits

The nadir-pointing attitude ensures:
- Maximum ground coverage per orbit
- Simplified imaging geometry with consistent look angles
- Optimal antenna pointing for ground station communications
- Reduced complexity in image processing and geolocation

### 4.3 Attitude Reference Frame

The attitude is defined using the Central Body Inertial (Cbi) reference frame, maintaining the satellite's Z-axis aligned toward Earth's center throughout the orbit.

---

## 5. Mission Operations

### 5.1 Imaging Operations

**Coverage Strategy:** Continuous nadir imaging during daylight passes  
**Data Collection Rate:** Dependent on sensor duty cycle and onboard storage capacity  
**Ground Swath:** ~96 km cross-track coverage per pass  

The rectangular sensor pattern provides square ground coverage, simplifying mosaic creation and area coverage planning.

### 5.2 Communication Operations

#### Downlink Architecture
- **Primary Link:** X-band at 8.2 GHz
- **Data Rate:** To be determined based on link budget analysis
- **Modulation:** Not specified in baseline configuration
- **Protocol:** Not specified in baseline configuration

#### Contact Window Analysis

The dual ground station architecture provides:
- Multiple daily contact opportunities with each station
- Geographic diversity for redundancy
- Extended coverage through high-latitude Svalbard station
- Regional coverage through Hyderabad station

**Note:** Specific access window counts are computed during simulation execution and vary based on orbital geometry and ground station visibility constraints.

### 5.3 Data Management

**Onboard Storage:** Not specified in baseline configuration  
**Downlink Priority:** Real-time or near-real-time data transmission during ground station passes  
**Data Processing:** Ground-based processing assumed for imagery products

---

## 6. Technical Implementation

### 6.1 Software Environment

**Simulation Platform:** AGI Systems Tool Kit (STK) Version 12  
**Programming Interface:** Python API (agi.stk12)  
**Automation Level:** Fully scripted mission scenario generation

### 6.2 Implementation Methodology

The mission scenario is constructed through a systematic 11-step process:

1. **STK Application Initialization** - Launch and configure STK desktop environment
2. **Scenario Creation** - Define mission timeframe and temporal parameters
3. **Satellite Object Creation** - Instantiate M600_Antaris satellite object
4. **Orbit Configuration** - Set orbital elements using Classical (Keplerian) representation
5. **Attitude Configuration** - Apply nadir-pointing constraint via Connect command
6. **Sensor Integration** - Add and configure EO imaging sensor
7. **Transmitter Integration** - Add X-band downlink transmitter
8. **Ground Station Deployment** - Create and position ground facilities
9. **Access Analysis** - Compute satellite-to-ground station visibility windows
10. **Graphics Configuration** - Enable orbit and ground track visualization
11. **Mission Summary** - Output comprehensive parameter report

### 6.3 Key Technical Decisions

**Orbital Element Representation:** Classical (Keplerian) elements chosen for intuitive parameter specification and standard mission planning compatibility.

**Propagation Model:** J2 perturbation model selected as optimal balance between accuracy and computational efficiency for LEO missions.

**Attitude Command Method:** Connect command interface used for attitude configuration to ensure maximum reliability and STK version compatibility.

**Coordinate Frames:** Geodetic coordinates used for ground station positioning to match standard geographic reference systems.

---

## 7. Performance Analysis

### 7.1 Coverage Capabilities

**Ground Coverage per Orbit:** Approximately 96 km swath width  
**Daily Coverage Potential:** 15 orbital passes  
**Maximum Swath Coverage:** ~1,440 km per day (theoretical maximum with continuous operation)

### 7.2 Revisit Performance

For any given target location:
- **Worst-case revisit time:** <24 hours (guaranteed by 15 daily orbits)
- **Typical revisit frequency:** Multiple opportunities per day for mid-latitude targets
- **Polar region coverage:** Enhanced frequency due to orbit convergence at high latitudes

### 7.3 Communication Performance

**Ground Station Access Frequency:**
- Both stations receive multiple daily passes
- Svalbard station benefits from high inclination, receiving more frequent contacts
- Hyderabad station provides regular coverage for regional operations

**Data Downlink Capacity:**
- Limited by X-band transmitter specifications (10W power output)
- Constrained by accumulated contact time across all passes
- Requires detailed link budget analysis for throughput estimation

---

## 8. Visualization and Analysis Features

### 8.1 Enabled Graphics

The simulation includes the following visualization elements:
- **Inertial orbit track** - Complete orbital path in inertial frame
- **Ground track projection** - Satellite ground trace on Earth's surface  
- **Reference axes display** - Satellite body-fixed coordinate frame
- **3D scene rendering** - Real-time 3D visualization in STK viewport

### 8.2 Analysis Capabilities

The implemented scenario supports:
- Access window computation and reporting
- Orbital parameter tracking over time
- Ground swath visualization
- Communication link geometry analysis
- Sensor coverage analysis

---

## 9. Operational Considerations

### 9.1 Mission Constraints

**Orbital Lifetime:** The 550 km altitude provides balance between imaging resolution and atmospheric drag. Expected lifetime (not modeled) would be several years with modest propulsion for orbit maintenance.

**Power Budget:** Not explicitly modeled in baseline scenario. Sun-synchronous orbit enables predictable solar panel illumination for power generation planning.

**Thermal Environment:** Sun-synchronous orbit provides consistent thermal conditions per orbit, simplifying thermal control system design.

### 9.2 Ground Operations

**Mission Control Functions:**
- Orbit determination and prediction
- Sensor tasking and scheduling  
- Ground station scheduling and coordination
- Data reception and archival
- Image processing and distribution

**Operational Tempo:**
- 24/7 operations implied by continuous imaging mission
- Multiple daily ground contacts requiring scheduling coordination
- Real-time or near-real-time data processing capability needed

---

## 10. Future Enhancements

### 10.1 Potential Mission Extensions

**Constellation Deployment:** Multiple M600-class satellites could provide:
- Reduced revisit times
- Increased daily coverage area
- Enhanced temporal resolution for change detection
- Improved emergency response capabilities

**Payload Upgrades:**
- Addition of SAR capability for all-weather imaging
- Integration of SIGINT sensors for electromagnetic spectrum monitoring
- Multispectral or hyperspectral imaging enhancements

**Ground Segment Expansion:**
- Additional ground stations for improved geographic coverage
- Implementation of inter-satellite links for data relay
- Integration with commercial ground station networks

### 10.2 Analysis Refinements

The baseline simulation could be enhanced with:
- Solar panel and power subsystem modeling
- Thermal analysis and constraint validation
- Propulsion system modeling for orbit maintenance
- Detailed link budget calculations
- Onboard storage capacity and data management simulation
- Target access analysis for specific points of interest
- Cloud cover statistics integration for optical imaging

---

## 11. Conclusion

The M600 Antaris mission represents a well-architected Earth observation system leveraging proven orbital mechanics principles and mission design practices. The sun-synchronous LEO orbit at 550 km altitude provides an optimal balance between ground resolution, orbit stability, and operational flexibility.

Key mission strengths include:
- **Consistent imaging conditions** through sun-synchronous orbit selection
- **Reliable communications** via dual ground station architecture  
- **Operational simplicity** through nadir-pointing attitude control
- **Comprehensive simulation** enabling detailed mission planning and analysis

The implementation demonstrates effective use of STK's automation capabilities through Python scripting, creating a reproducible and modifiable mission scenario suitable for trade studies, operational planning, and educational purposes.

**Mission Readiness Assessment:** The baseline configuration provides a solid foundation for detailed mission planning. Additional analysis of power, thermal, and data handling subsystems would be required for operational deployment.

---

## Appendices

### Appendix A: Orbital Parameter Calculations

**Semi-major axis calculation:**
```
a = R_earth + h
a = 6,378.137 km + 550 km = 6,928.137 km
```

**Orbital period calculation:**
```
T = 2π × √(a³/μ)
where μ = 398,600.4418 km³/s²
T = 5,740.8 seconds = 95.68 minutes
```

**Revolutions per day:**
```
n = 1440 minutes/day ÷ 95.68 minutes/orbit = 15.0 orbits/day
```

### Appendix B: Ground Swath Calculation

**Cross-track swath width:**
```
W = 2 × h × tan(θ/2)
where h = 550 km, θ = 5°
W ≈ 96.2 km
```

### Appendix C: System Requirements

**Software Dependencies:**
- AGI Systems Tool Kit (STK) 12.x
- Python 3.x with STK Integration API
- Windows operating system (for STK Desktop)

**Hardware Requirements:**
- Sufficient RAM for 3D visualization (8 GB minimum recommended)
- Graphics card supporting OpenGL for 3D rendering
- Multi-core processor for computation performance

---

**Report Prepared:** December 2025  
**Document Version:** 1.0  
**Classification:** Unclassified Technical Documentation
