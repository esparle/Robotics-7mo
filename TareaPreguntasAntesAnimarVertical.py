import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------------------------
# Entradas del usuario
# ---------------------------
l1 = float(input("Longitud del primer eslabón: "))
l2 = float(input("Longitud del segundo eslabón: "))

x_target = float(input("Coordenada X final (frente o atrás): "))
z_target = float(input("Coordenada Z final (altura): "))

modo = input("¿Codo arriba (u) o codo abajo (d)? [u/d]: ").lower()
giro_base = float(input("¿Cuántos grados quieres que gire la base al final?: "))

# ---------------------------
# Cinemática inversa en el plano XZ
# ---------------------------
r = np.sqrt(x_target**2 + z_target**2)
cos_theta2 = (r**2 - l1**2 - l2**2) / (2 * l1 * l2)
cos_theta2 = np.clip(cos_theta2, -1, 1)
theta2 = np.arccos(cos_theta2)
if modo == "d":
    theta2 = -theta2

theta1 = np.arctan2(x_target, z_target) - np.arctan2(l2*np.sin(theta2), l1 + l2*np.cos(theta2))

# ---------------------------
# Parámetros de animación
# ---------------------------
frames_move = 100
frames_rotate = 60
frames_total = frames_move + frames_rotate

theta1_vals = np.linspace(0, theta1, frames_move)
theta2_vals = np.linspace(0, theta2, frames_move)
yaw_vals = np.linspace(0, np.deg2rad(giro_base), frames_rotate)

# ---------------------------
# Cinemática directa
# ---------------------------
def forward_kinematics(t1, t2, yaw=0, flat=False):
    # Coordenadas en el plano XZ
    x0, y0, z0 = 0, 0, 0
    x1 = l1 * np.sin(t1)
    z1 = l1 * np.cos(t1)

    x2 = x1 + l2 * np.sin(t1 + t2)
    z2 = z1 + l2 * np.cos(t1 + t2)

    if flat:
        # Giro plano en XY (horizontal)
        R = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                      [np.sin(yaw),  np.cos(yaw), 0],
                      [0, 0, 1]])
    else:
        # Giro sobre eje Y (vertical)
        R = np.array([[np.cos(yaw), 0, np.sin(yaw)],
                      [0, 1, 0],
                      [-np.sin(yaw), 0, np.cos(yaw)]])
    
    P0 = np.dot(R, np.array([x0, y0, z0]))
    P1 = np.dot(R, np.array([x1, y0, z1]))
    P2 = np.dot(R, np.array([x2, y0, z2]))

    X = [P0[0], P1[0], P2[0]]
    Y = [P0[1], P1[1], P2[1]]
    Z = [P0[2], P1[2], P2[2]]
    return X, Y, Z

# ---------------------------
# Configuración de la figura 3D
# ---------------------------
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect([1, 1, 1])

lim = (l1 + l2)
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_zlim(0, lim * 1.3)
ax.set_xlabel('X (frente)', labelpad=10)
ax.set_ylabel('Y (lateral)', labelpad=10)
ax.set_zlabel('Z (altura)', labelpad=10)
ax.set_title("Tarea 3er parcial, Rotación robot vertical", pad=20)

# Piso
xx, yy = np.meshgrid(np.linspace(-lim, lim, 2),
                     np.linspace(-lim, lim, 2))
zz = np.zeros_like(xx)
ax.plot_surface(xx, yy, zz, alpha=0.25, color='gray', zorder=0)

# Base y objetivo
ax.scatter(0, 0, 0, color='black', s=60)      # Base
ax.scatter(x_target, 0, z_target, color='red', s=60)  # Objetivo

# Línea del robot
line, = ax.plot([], [], [], 'o-', lw=3, color='blue')

# Vista más abierta para apreciar el plano XY
ax.view_init(elev=25, azim=-60)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.grid(False)

# ---------------------------
# Función de actualización
# ---------------------------
def update(frame):
    if frame < frames_move:
        # Movimiento vertical (en XZ)
        t1 = theta1_vals[frame]
        t2 = theta2_vals[frame]
        yaw = 0
        flat = False
    else:
        # Rotación plana en XY
        t1 = theta1
        t2 = theta2
        yaw = yaw_vals[frame - frames_move]
        flat = True

    X, Y, Z = forward_kinematics(t1, t2, yaw, flat)
    line.set_data(X, Y)
    line.set_3d_properties(Z)
    return line,

# ---------------------------
# Animación
# ---------------------------
ani = FuncAnimation(fig, update, frames=frames_total, interval=80, blit=True)
plt.show()
