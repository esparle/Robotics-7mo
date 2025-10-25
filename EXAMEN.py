# sim_scara_omron_v2.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------- Parámetros del robot (mm) ----------
L1 = 475.0
L2 = 850.0
tool_len = 100.0
body_height = 760.0

# ---------- Movimiento (más amplio y lento) ----------
theta1_final = np.deg2rad(100.0)   # primer brazo gira ~100°
theta2_final = np.deg2rad(-150.0)  # segundo brazo rota ~-150°
z_start = 450.0
z_target = 100.0
z_end = 350.0
yaw_final_deg = 180.0              # rotación completa del efector

# Más frames = movimiento más lento
frames_joints = 250
frames_z = 200
frames_yaw = 200
frames_up = 200
frames_total = frames_joints + frames_z + frames_yaw + frames_up

# Interpolaciones suaves
theta1_vals = np.linspace(0.0, theta1_final, frames_joints)
theta2_vals = np.linspace(0.0, theta2_final, frames_joints)
z_down_vals = np.linspace(z_start, z_target, frames_z)
z_up_vals = np.linspace(z_target, z_end, frames_up)
yaw_vals = np.linspace(0.0, np.deg2rad(yaw_final_deg), frames_yaw)

# ---------- Cinemática directa SCARA ----------
def scara_forward(t1, t2, z, yaw=0.0):
    P0 = np.array([0.0, 0.0, body_height])
    x1 = L1 * np.cos(t1)
    y1 = L1 * np.sin(t1)
    P1 = P0 + np.array([x1, y1, 0.0])
    x2 = x1 + L2 * np.cos(t1 + t2)
    y2 = y1 + L2 * np.sin(t1 + t2)
    P2 = P0 + np.array([x2, y2, -z])

    c, s = np.cos(yaw), np.sin(yaw)
    Rz = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    tool_dir = Rz.dot(np.array([np.cos(t1 + t2), np.sin(t1 + t2), 0]))
    tool_end = P2 + tool_len * tool_dir

    X, Y, Z = [P0[0], P1[0], P2[0]], [P0[1], P1[1], P2[1]], [P0[2], P1[2], P2[2]]
    tX, tY, tZ = [P2[0], tool_end[0]], [P2[1], tool_end[1]], [P2[2], tool_end[2]]
    return X, Y, Z, tX, tY, tZ, P2

# ---------- Visualización ----------
plt.ion()
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')

reach = L1 + L2
lim = reach * 1.15
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_zlim(0, body_height + 250)
ax.set_box_aspect([1,1,0.7])
ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_zlabel('Z (mm)')
ax.set_title('Omron i4-850H (Simulación - Movimiento 180°)')

# Piso
xx, yy = np.meshgrid(np.linspace(-lim, lim, 2), np.linspace(-lim, lim, 2))
zz = np.zeros_like(xx)
ax.plot_surface(xx, yy, zz, alpha=0.1, color='gray', zorder=0)

# Columna base
ax.plot([0,0], [0,0], [0, body_height], color='dimgray', lw=15, alpha=0.8)

# Elementos del robot
link1_line, = ax.plot([], [], [], '-', lw=10, color='#E6E6E6', solid_capstyle='round')
link2_line, = ax.plot([], [], [], '-', lw=8, color='#C0C0C0', solid_capstyle='round')
tool_line, = ax.plot([], [], [], '-', lw=4, color='tab:blue', solid_capstyle='round')

# Trayectoria del efector
trail_X, trail_Y, trail_Z = [], [], []
trail_line, = ax.plot([], [], [], '--', lw=1.5, color='tab:gray', alpha=0.7)

# Texto
info_text = ax.text2D(0.02, 0.95, "", transform=ax.transAxes)

# Vista baja y angular (tipo suelo)
ax.view_init(elev=10, azim=-90)

# ---------- Animación ----------
def update(frame):
    if frame < frames_joints:
        t1, t2 = theta1_vals[frame], theta2_vals[frame]
        z, yaw = z_start, 0.0
        info = "Fase 1: Movimiento XY amplio..."
    elif frame < frames_joints + frames_z:
        idx = frame - frames_joints
        t1, t2 = theta1_vals[-1], theta2_vals[-1]
        z, yaw = z_down_vals[idx], 0.0
        info = "Fase 2: Descendiendo eje Z..."
    elif frame < frames_joints + frames_z + frames_yaw:
        idx = frame - (frames_joints + frames_z)
        t1, t2 = theta1_vals[-1], theta2_vals[-1]
        z, yaw = z_down_vals[-1], yaw_vals[idx]
        info = f"Fase 3: Girando efector ({np.rad2deg(yaw):.1f}°)..."
    else:
        idx = frame - (frames_joints + frames_z + frames_yaw)
        t1, t2 = theta1_vals[-1], theta2_vals[-1]
        z, yaw = z_up_vals[min(idx, len(z_up_vals)-1)], yaw_vals[-1]
        info = "Fase 4: Subiendo eje Z..."

    X, Y, Z, tX, tY, tZ, P2 = scara_forward(t1, t2, z, yaw)

    link1_line.set_data(X[0:2], Y[0:2])
    link1_line.set_3d_properties(Z[0:2])
    link2_line.set_data(X[1:3], Y[1:3])
    link2_line.set_3d_properties(Z[1:3])
    tool_line.set_data(tX, tY)
    tool_line.set_3d_properties(tZ)

    trail_X.append(P2[0])
    trail_Y.append(P2[1])
    trail_Z.append(P2[2])
    trail_line.set_data(trail_X, trail_Y)
    trail_line.set_3d_properties(trail_Z)

    info_text.set_text(info)
    return link1_line, link2_line, tool_line, trail_line, info_text

ani = FuncAnimation(fig, update, frames=frames_total, interval=60, blit=False)
plt.show(block=True)
