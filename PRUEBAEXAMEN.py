import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# ---------------------------
# Parámetros del robot
# ---------------------------
l1, l2, l3 = 2, 1.5, 1
theta1_f = 45    # grados
theta2_f = 60
theta3_f = -30

frames = 120
theta1_vals = np.linspace(0, theta1_f, frames)
theta2_vals = np.linspace(0, theta2_f, frames)
theta3_vals = np.linspace(0, theta3_f, frames)

# ---------------------------
# Funciones auxiliares
# ---------------------------
def sind(t):
    return np.sin(np.deg2rad(t))

def cosd(t):
    return np.cos(np.deg2rad(t))

def drawVector(p_fin, p_init=[0,0,0], color='black', linewidth=2):
    x = [p_init[0], p_fin[0]]
    y = [p_init[1], p_fin[1]]
    z = [p_init[2], p_fin[2]]
    ax.plot3D(x, y, z, color=color, linewidth=linewidth)

def fix_system(axis_length=5, linewidth=2):
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length]
    z = [-axis_length, axis_length]
    zp = [0,0]
    ax.plot3D(x, zp, zp, color='red', linewidth=linewidth)
    ax.plot3D(zp, y, zp, color='blue', linewidth=linewidth)
    ax.plot3D(zp, zp, z, color='green', linewidth=linewidth)

# ---------------------------
# Cinemática directa
# ---------------------------
def forward_kinematics(t1, t2, t3):
    x0, y0, z0 = 0,0,0
    x1, y1, z1 = l1*cosd(t1), l1*sind(t1), 0
    x2, y2, z2 = x1 + l2*cosd(t1 + t2), y1 + l2*sind(t1 + t2), 0
    x3, y3, z3 = x2 + l3*cosd(t1 + t2 + t3), y2 + l3*sind(t1 + t2 + t3), 0
    return np.array([[x0,y0,z0],[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]])

# ---------------------------
# Configuración gráfica
# ---------------------------
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Examen 1er Parcial")
fix_system(5)

# ---------------------------
# Función de actualización
# ---------------------------
def update(frame):
    ax.cla()  # limpiar figura
    fix_system(5)
    ax.set_title("Examen 1er Parcial")
    
    points = forward_kinematics(theta1_vals[frame],
                                theta2_vals[frame],
                                theta3_vals[frame])
    
    # Dibujar cada eslabón
    drawVector(points[1], points[0], color='orange', linewidth=4)
    drawVector(points[2], points[1], color='purple', linewidth=4)
    drawVector(points[3], points[2], color='cyan', linewidth=4)
    
    # Punto final
    ax.scatter(*points[-1], color='red', s=50)

    # Cámara
    ax.view_init(elev=30, azim=30 + frame*0.3)
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_zlim(-2,2)

# ---------------------------
# Animación
# ---------------------------
ani = FuncAnimation(fig, update, frames=frames, interval=80)

plt.show()

