# Aircraft Dogfight Simulation with Missiles 🛩️

A dynamic 3D visualization of a multi-aircraft dogfight featuring missile combat, built with Python and Matplotlib.

## Overview

This simulation depicts an intense aerial combat scenario between two squadrons (Red and Blue), each consisting of 2 aircraft. The visualization includes realistic flight trajectories, evasive maneuvers, and missile launches with tracking capabilities.

## Features

- **4 Aircraft Combat**: Two squadrons (Red and Blue) with 2 aircraft each
- **3D Flight Trajectories**: Realistic flight paths with altitude changes and tactical maneuvers
- **Missile System**: 5 missiles launch during the engagement with curved trajectories
- **Visual Tracking**: Color-coded trails for aircraft and missiles
- **Dynamic Camera**: Rotating viewpoint for optimal visualization
- **Real-time Status**: Display showing frame count and active missile count
- **Smooth Animation**: 300 frames of continuous aerial combat

## Requirements

```bash
numpy
matplotlib
```

## Installation

1. Ensure you have Python 3.7+ installed
2. Install required packages:

```bash
pip install numpy matplotlib
```

## Usage

Simply run the Python script:

```bash
python dogfight_simulation.py
```

The animation will start automatically in a new window.

## How It Works

### Aircraft Squadrons

**Red Squadron**
- Red 1: Primary pursuing aircraft with oscillating altitude
- Red 2: Secondary aircraft with offset trajectory

**Blue Squadron**
- Blue 1: Evasive maneuvers with complex spiral patterns
- Blue 2: High-altitude combat with defensive positioning

### Missile Launch Timeline

| Frame | Attacker | Target | Notes |
|-------|----------|--------|-------|
| 60    | Red 1    | Blue 1 | Opening salvo |
| 90    | Blue 1   | Red 2  | Counter-attack |
| 130   | Red 2    | Blue 2 | Mid-engagement |
| 170   | Blue 2   | Red 1  | Defensive response |
| 210   | Red 1    | Blue 2 | Final engagement |

### Visualization Elements

- **Aircraft Markers**: Large colored circles (red/blue) with black edges
- **Flight Trails**: Semi-transparent lines showing recent flight path (40 frames)
- **Missiles**: Orange/yellow markers with glowing trails
- **Grid**: 3D coordinate grid for spatial reference
- **Status Box**: Information overlay in top-left corner

## Customization

### Adjusting Parameters

**Number of Aircraft**: Modify the trajectory equations and add new `x`, `y`, `z` arrays

**Missile Launch Times**: Edit the frame numbers in the `update()` function:
```python
if frame == 60:  # Change this number
    missiles.append(launch_missile(...))
```

**Animation Speed**: Adjust the `interval` parameter (in milliseconds):
```python
anim = FuncAnimation(..., interval=50, ...)  # 50ms = 20 fps
```

**Trail Length**: Modify the `trail_length` variable:
```python
trail_length = 40  # Number of frames to show in trail
```

**Missile Duration**: Edit the duration in `launch_missile()`:
```python
duration = 40  # frames the missile stays active
```

### Camera Control

Change the viewing angle by modifying:
```python
ax.view_init(elev=25, azim=frame*0.4)
```

- `elev`: Elevation angle (vertical tilt)
- `azim`: Azimuth angle (horizontal rotation)

## Technical Details

### Trajectory Generation

Aircraft paths are generated using parametric equations:
- Circular components: `cos(t)` and `sin(t)` for orbital patterns
- Altitude variation: Sinusoidal functions for vertical maneuvers
- Evasive maneuvers: Multiple frequency sine waves for complex paths

### Missile Physics

Missiles follow interpolated paths with:
- Linear interpolation between launch and target positions
- Sinusoidal curve for realistic trajectory arcing
- Limited lifetime (40 frames) for visual clarity

## Performance Notes

- The animation runs at approximately 20 FPS (50ms intervals)
- 300 total frames provide ~15 seconds of animation per loop
- Missile trails are limited to 15 frames to maintain performance

## Troubleshooting

**Animation is slow**: Reduce the number of frames or increase the interval
```python
t = np.linspace(0, 4*np.pi, 200)  # Reduce from 300
```

**Window doesn't appear**: Ensure you have a display backend configured for Matplotlib

**Import errors**: Verify all dependencies are installed correctly

## Future Enhancements

- [ ] Add explosion effects when missiles reach targets
- [ ] Implement hit detection system
- [ ] Add cockpit view camera option
- [ ] Include sound effects
- [ ] Add more aircraft types with different colors
- [ ] Implement collision avoidance
- [ ] Add ground terrain visualization
- [ ] Create interactive controls for camera

## License

This project is open source and available for educational and personal use.

## Credits

Created using Python's Matplotlib and NumPy libraries for 3D visualization and mathematical computations.

---

**Enjoy the simulation! Feel free to modify and expand upon this code for your own projects.**
