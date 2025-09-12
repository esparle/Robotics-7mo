import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

# create the fig and ax objects to handle figure and axes of the fixed frame
fig,ax = plt.subplots()

# Use 3d view 
ax = plt.axes(projection = "3d")



def setaxis(x1, x2, y1, y2, z1, z2):

    ax.set_xlim3d(x1,x2)
    ax.set_ylim3d(y1,y2)
    ax.set_zlim3d(z1,z2)
    ax.view_init(elev=30, azim=40)


def fix_system(axis_length, linewidth=5):

    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length] 
    z = [-axis_length, axis_length]
    zp = [0, 0]
    ax.plot3D(x, zp, zp, color='red', linewidth=linewidth)
    ax.plot3D(zp, y, zp, color='blue',linewidth=linewidth)
    ax.plot3D(zp, zp, z, color='green',linewidth=linewidth)
    

def sind(t):
    
    res = np.sin(t*np.pi/180)
    return res

def cosd(t):
   
    res = np.cos(t*np.pi/180)
    return res

def RotX(t):
    Rx = np.array(([1,0,0],[0,cosd(t),-sind(t)],[0,sind(t),cosd(t)]))
    return Rx

def RotY(t):
    Ry = np.array(([cosd(t),0,sind(t)],[0,1,0],[-sind(t),0,cosd(t)]))
    return Ry 

def RotZ(t):
    Rz = np.array(([cosd(t),-sind(t),0],[sind(t),cosd(t),0],[0,0,1]))
    return Rz

def drawVector(p_fin, p_init=[0,0,0], color='black',linewidth=1):
    deltaX = [p_init[0], p_fin[0]]
    deltaY = [p_init[1], p_fin[1]]
    deltaZ = [p_init[2], p_fin[2]]
    ax.plot3D(deltaX, deltaY, deltaZ,color=color, linewidth=linewidth)


def drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color = 'black'):

    drawScatter(p1)
    drawScatter(p2)
    drawScatter(p3)
    drawScatter(p4)
    drawScatter(p5)
    drawScatter(p6)
    drawScatter(p7)
    drawScatter(p8)

    drawVector(p1,p2)
    drawVector(p2,p3)
    drawVector(p3,p4)
    drawVector(p4,p1)
    drawVector(p5,p6)
    drawVector(p6,p7)
    drawVector(p7,p8)
    drawVector(p8,p5)
    drawVector(p4,p8)
    drawVector(p1,p5)
    drawVector(p3,p7)
    drawVector(p2,p6)


def drawScatter(point,color='black',marker='o'):
    ax.scatter(point[0],point[1],point[2],marker='o')

def transform_box(p1,p2,p3,p4,p5,p6,p7,p8, Rx=0, Ry=0, Rz=0, deltaX=0, deltaY=0, deltaZ=0):
    
    p1 = [p1[0],p1[1],p1[2],1]
    p2 = [p2[0],p2[1],p2[2],1]
    p3 = [p3[0],p3[1],p3[2],1]
    p4 = [p4[0],p4[1],p4[2],1]
    p5 = [p5[0],p5[1],p5[2],1]
    p6 = [p6[0],p6[1],p6[2],1]
    p7 = [p7[0],p7[1],p7[2],1]
    p8 = [p8[0],p8[1],p8[2],1]

    R = RotX(Rx).dot(RotY(Ry).dot(RotZ(Rz)))
    
    Rotation_Matrix = np.eye(4)
    Rotation_Matrix[:3,:3] = R

    T = np.array(([1,0,0,deltaX],
                    [0,1,0,deltaY],
                    [0,0,1,deltaZ],
                    [0,0,0,1]))
    
    TR_matrix = T.dot(Rotation_Matrix)

    p1_TR = TR_matrix.dot(p1)[:3]
    p2_TR = TR_matrix.dot(p2)[:3]
    p3_TR = TR_matrix.dot(p3)[:3]
    p4_TR = TR_matrix.dot(p4)[:3]
    p5_TR = TR_matrix.dot(p5)[:3]
    p6_TR = TR_matrix.dot(p6)[:3]
    p7_TR = TR_matrix.dot(p7)[:3]
    p8_TR = TR_matrix.dot(p8)[:3]

    return [p1_TR, p2_TR, p3_TR, p4_TR, p5_TR, p6_TR, p7_TR, p8_TR]

# Set the view 
setaxis(-15,15,-15,15,-15,15)

# plot the axis
fix_system(10,1)

p1_init = [0,0,0]
p2_init = [7,0,0]
p3_init = [7,0,3]
p4_init = [0,0,3]
p5_init = [0,2,0]
p6_init = [7,2,0]
p7_init = [7,2,3]
p8_init = [0,2,3]


drawBox(p1_init, p2_init, p3_init, p4_init,
        p5_init, p6_init, p7_init, p8_init)

box_moved_1 = transform_box(p1_init, p2_init, p3_init, p4_init,
                            p5_init, p6_init, p7_init, p8_init, 
                            deltaX=5, deltaY=5, deltaZ=2)

drawBox(box_moved_1[0],box_moved_1[1],box_moved_1[2],box_moved_1[3],
        box_moved_1[4],box_moved_1[5],box_moved_1[6],box_moved_1[7])

box_rot = transform_box(box_moved_1[0],box_moved_1[1],box_moved_1[2],box_moved_1[3],
                        box_moved_1[4],box_moved_1[5],box_moved_1[6],box_moved_1[7], 
                        deltaX=-4, deltaY=3, deltaZ=1, Rx=0, Ry=0, Rz=45)

drawBox(box_rot[0],box_rot[1],box_rot[2],box_rot[3],
        box_rot[4],box_rot[5],box_rot[6],box_rot[7])



# show image.
plt.draw()
plt.show()