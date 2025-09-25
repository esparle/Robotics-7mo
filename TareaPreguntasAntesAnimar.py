import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------------------------
# Entradas del usuario
# ---------------------------
l1 = float(input("Longitud del primer eslabón: "))
l2 = float(input("Longitud del segundo eslabón: "))

x_target = float(input("Coordenada X final: "))
y_target = float(input("Coordenada Y final: "))

modo = input("¿Codo arriba (u) o codo abajo (d)? [u/d]: ").lower()

# ---------------------------
# Cinemática inversa para 2DOF
# ---------------------------
r = np.sqrt(x_target**2 + y_target**2)

# Ley de cosenos para θ2
cos_theta2 = (r**2 - l1**2 - l2**2) / (2 * l1 * l2)
cos_theta2 = np.clip(cos_theta2, -1, 1)  # evitar errores numéricos
theta2 = np.arccos(cos_theta2)

if modo == "d":
    theta2 = -theta2

# Cálculo de θ1
theta1 = np.arctan2(y_target, x_target) - np.arctan2(l2*np.sin(theta2), l1 + l2*np.cos(theta2))

# ---------------------------
# Interpolación de ángulos
# ---------------------------
frames = 100
theta1_vals = np.linspace(0, theta1, frames)
theta2_vals = np.linspace(0, theta2, frames)

# ---------------------------
# Cinemática directa
# ---------------------------
def forward_kinematics(t1, t2):
    x0, y0, z0 = 0, 0, 0
    x1 = l1 * np.cos(t1)
    y1 = l1 * np.sin(t1)
    z1 = 0

    x2 = x1 + l2 * np.cos(t1 + t2)
    y2 = y1 + l2 * np.sin(t1 + t2)
    z2 = 0

    return [x0, x1, x2], [y0, y1, y2], [z0, z1, z2]

# ---------------------------
# Gráfica 3D
# ---------------------------
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(- (l1 + l2), (l1 + l2))
ax.set_ylim(- (l1 + l2), (l1 + l2))
ax.set_zlim(-1, 1)  # plano XY
ax.set_title("Animación Robot 2-DOF")
line, = ax.plot([], [], [], 'o-', lw=3)

# ---------------------------
# Función de actualización
# ---------------------------
def update(frame):
    X, Y, Z = forward_kinematics(theta1_vals[frame],
                                 theta2_vals[frame])
    line.set_data(X, Y)
    line.set_3d_properties(Z)
    return line,

# ---------------------------
# Animación
# ---------------------------
ani = FuncAnimation(fig, update, frames=frames, interval=100, blit=True)
plt.show()
