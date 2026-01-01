import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Create figure and 3D axis
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Time parameters
t = np.linspace(0, 4*np.pi, 300)

# Aircraft trajectories
x1 = 35 * np.cos(t)
y1 = 35 * np.sin(t)
z1 = 5 * np.sin(2*t) + 22

x2 = 30 * np.cos(t - np.pi/3) + 5
y2 = 30 * np.sin(t - np.pi/3) + 5
z2 = 6 * np.sin(2*t + 1) + 20

# Blue Squadron (2 aircraft)
x3 = 32 * np.cos(t + np.pi/2) + 12 * np.sin(3*t)
y3 = 32 * np.sin(t + np.pi/2) + 12 * np.cos(3*t)
z3 = 8 * np.cos(2*t) + 26

x4 = 28 * np.cos(t + np.pi) + 8 * np.sin(2.5*t)
y4 = 28 * np.sin(t + np.pi) + 8 * np.cos(2.5*t)
z4 = 7 * np.sin(2*t - 1) + 24

# Missile data structure
missiles = []

def launch_missile(frame, from_x, from_y, from_z, to_x, to_y, to_z):
    """Create a missile trajectory from one point toward another"""
    duration = 40  # frames
    traj_t = np.linspace(0, 1, duration)
    
    # Add some curvature to missile path
    curve = 3 * np.sin(np.pi * traj_t)
    
    mx = from_x + (to_x - from_x) * traj_t + curve
    my = from_y + (to_y - from_y) * traj_t + curve * 0.5
    mz = from_z + (to_z - from_z) * traj_t
    
    return {
        'start_frame': frame,
        'x': mx,
        'y': my,
        'z': mz,
        'active': True
    }

# Initialize plot elements
# Aircraft trails
line1, = ax.plot([], [], [], 'r-', linewidth=2, alpha=0.6, label='Red 1')
line2, = ax.plot([], [], [], 'darkred', linewidth=2, alpha=0.6, label='Red 2')
line3, = ax.plot([], [], [], 'b-', linewidth=2, alpha=0.6, label='Blue 1')
line4, = ax.plot([], [], [], 'darkblue', linewidth=2, alpha=0.6, label='Blue 2')

# Aircraft positions
point1, = ax.plot([], [], [], 'ro', markersize=12, markeredgecolor='black', markeredgewidth=1)
point2, = ax.plot([], [], [], 'ro', markersize=12, markeredgecolor='black', markeredgewidth=1)
point3, = ax.plot([], [], [], 'bo', markersize=12, markeredgecolor='black', markeredgewidth=1)
point4, = ax.plot([], [], [], 'bo', markersize=12, markeredgecolor='black', markeredgewidth=1)

# Missile plot elements (we'll update these dynamically)
missile_lines = []
missile_points = []

# Set axis limits
ax.set_xlim([-50, 50])
ax.set_ylim([-50, 50])
ax.set_zlim([0, 45])
ax.set_xlabel('X (km)', fontsize=10)
ax.set_ylabel('Y (km)', fontsize=10)
ax.set_zlabel('Altitude (km)', fontsize=10)
ax.set_title('Multi-Aircraft Dogfight with Missiles', fontsize=14, fontweight='bold')
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.3)

# Status text
status_text = ax.text2D(0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
                        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

def init():
    line1.set_data([], [])
    line1.set_3d_properties([])
    line2.set_data([], [])
    line2.set_3d_properties([])
    line3.set_data([], [])
    line3.set_3d_properties([])
    line4.set_data([], [])
    line4.set_3d_properties([])
    return line1, line2, line3, line4

def update(frame):
    global missiles, missile_lines, missile_points
    
    trail_length = 40
    start_idx = max(0, frame - trail_length)
    
    # Update aircraft trails
    line1.set_data(x1[start_idx:frame], y1[start_idx:frame])
    line1.set_3d_properties(z1[start_idx:frame])
    
    line2.set_data(x2[start_idx:frame], y2[start_idx:frame])
    line2.set_3d_properties(z2[start_idx:frame])
    
    line3.set_data(x3[start_idx:frame], y3[start_idx:frame])
    line3.set_3d_properties(z3[start_idx:frame])
    
    line4.set_data(x4[start_idx:frame], y4[start_idx:frame])
    line4.set_3d_properties(z4[start_idx:frame])
    
    # Update aircraft positions
    if frame > 0:
        idx = min(frame-1, len(x1)-1)
        point1.set_data([x1[idx]], [y1[idx]])
        point1.set_3d_properties([z1[idx]])
        
        point2.set_data([x2[idx]], [y2[idx]])
        point2.set_3d_properties([z2[idx]])
        
        point3.set_data([x3[idx]], [y3[idx]])
        point3.set_3d_properties([z3[idx]])
        
        point4.set_data([x4[idx]], [y4[idx]])
        point4.set_3d_properties([z4[idx]])
    
    # Launch missiles at specific intervals
    if frame == 60:
        idx = min(59, len(x1)-1)
        missiles.append(launch_missile(frame, x1[idx], y1[idx], z1[idx], x3[idx], y3[idx], z3[idx]))
    if frame == 90:
        idx = min(89, len(x3)-1)
        missiles.append(launch_missile(frame, x3[idx], y3[idx], z3[idx], x2[idx], y2[idx], z2[idx]))
    if frame == 130:
        idx = min(129, len(x2)-1)
        missiles.append(launch_missile(frame, x2[idx], y2[idx], z2[idx], x4[idx], y4[idx], z4[idx]))
    if frame == 170:
        idx = min(169, len(x4)-1)
        missiles.append(launch_missile(frame, x4[idx], y4[idx], z4[idx], x1[idx], y1[idx], z1[idx]))
    if frame == 210:
        idx = min(209, len(x1)-1)
        missiles.append(launch_missile(frame, x1[idx], y1[idx], z1[idx], x4[idx], y4[idx], z4[idx]))
    
    # Clear old missile graphics
    for line in missile_lines:
        line.remove()
    for point in missile_points:
        point.remove()
    missile_lines = []
    missile_points = []
    
    # Update and draw active missiles
    active_count = 0
    for missile in missiles:
        if missile['active']:
            local_frame = frame - missile['start_frame']
            if 0 <= local_frame < len(missile['x']):
                # Draw missile trail
                trail_start = max(0, local_frame - 15)
                mline, = ax.plot(missile['x'][trail_start:local_frame+1], 
                                missile['y'][trail_start:local_frame+1],
                                missile['z'][trail_start:local_frame+1],
                                'yellow', linewidth=1.5, alpha=0.7)
                missile_lines.append(mline)
                
                # Draw missile head
                mpoint, = ax.plot([missile['x'][local_frame]], 
                                 [missile['y'][local_frame]],
                                 [missile['z'][local_frame]],
                                 'o', color='orange', markersize=6, 
                                 markeredgecolor='red', markeredgewidth=1)
                missile_points.append(mpoint)
                active_count += 1
            else:
                missile['active'] = False
    
    # Update status text
    status_text.set_text(f'Frame: {frame}\nActive Missiles: {active_count}')
    
    # Rotate view
    ax.view_init(elev=25, azim=frame*0.4)
    
    return [line1, line2, line3, line4, point1, point2, point3, point4, status_text] + missile_lines + missile_points

# Create animation
anim = FuncAnimation(fig, update, init_func=init, frames=len(t), 
                    interval=50, blit=False, repeat=True)

plt.tight_layout()
plt.show()
