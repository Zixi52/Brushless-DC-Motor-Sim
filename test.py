import vpython as py
import os
from vpython import *
# ------------------------------------------------CAMERA SETTINGS------------------------------------------------
canva = canvas(width=600, height=600, background=color.white) 

canva.forward = vector(0, 0, -1)
canva.center = vector(0, 0, 0)
canva.userzoom = False   # Disables scroll wheel zoom
canva.userspin = True   # Disables right-click rotation
canva.userpan = True    # Disables shift-click object sliding/panning
canva.autoscale = True  # Prevents camera from jumping around
canva.fov = 0.0001    
print("hello world")
# ------------------------------------------------GLOBAL VARIABLES------------------------------------------------
stator_r =4
motor_length = 10
originAxesLength = 3
temp_v1 =-2
#========================STATOR=================================
hollow_stator_circle= shapes.circle(radius= stator_r, np= 20, angle1 = 0.0, angle2 = 4*pi/2, thickness =.1) # fix with thickness
stator_core_line = [ vec(0,0,temp_v1), vec(0,0,temp_v1-motor_length) ]
stator_core =extrusion( color=color.gray(.5), shape=hollow_stator_circle, path=stator_core_line )

pi_2_3=2*pi/3
# Coil cores (arranged in a ring around the magnet) to show copper windings
coil_wire = [None,None,None]
for i in range(len(coil_wire)):
    coil_wire[i]=helix(pos=vector(stator_r*cos(pi_2_3*i), stator_r*sin(pi_2_3*i), 
                                  (stator_core_line[0].z+stator_core_line[1].z)/2),
                       axis=vector(cos(pi_2_3*i), sin(pi_2_3*i), 0),
                  radius=2, coils=8, thickness=0.2, color=color.green,
                  thicknesses=0.1, size =vec(2,2,motor_length))

# Create XYZ axis  #
originAxes = [
    arrow(pos=vec(0, 0, 0), axis=vec(originAxesLength, 0, 0), color=color.red, shaftwidth=originAxesLength/10,),
    arrow(pos=vec(0, 0, 0), axis=vec(0, originAxesLength, 0), color=color.green, shaftwidth=originAxesLength/10),
    arrow(pos=vec(0, 0, 0), axis=vec(0, 0, originAxesLength), color=color.blue, shaftwidth=originAxesLength/10)]
originLabels = [None, None, None]
for i in range(len(originLabels)):
    if i == 0:
        str1 = "X"
    elif i == 1:
        str1 = "Y"
    elif i == 2:
        str1 = "Z"
    originLabels[i] = text(pos =originAxes[i].axis, color =originAxes[i].color, text = str1, height=1)

def showOrigin (evt):
    if evt.text == 'axes on': #if the button has this on click
        for origin in originAxes:
                origin.opacity=0.0
        for l in originLabels:
                l.opacity=0.0
        clrbtn.text = 'axes off'
    else:
        for origin in originAxes:
                origin.opacity=1.0
        for l in originLabels:
                l.opacity=1.0
        clrbtn.text = 'axes on'
         
clrbtn = button( bind=showOrigin, text='axes on')
#=========================================================
# permanent magnet (rotating cylinder in the center)
magnet = cylinder(pos=vector(0,0,0), axis=vector(0,0,1), radius=3, length=0.6,
                  color=color.red, texture=textures.metal)
north_half= shapes.circle(radius= 2, np= 32, scale =2, angle1=0, angle2 = pi)
linepath = [ vec(0,0,0), vec(0,0,3) ]
extrusion( shape=north_half, path=linepath )

south_half= shapes.circle(radius= 2, np= 32, scale =2, angle1=pi, angle2 = 2*pi)
linepath = [ vec(0,0,0), vec(0,0,3) ]
extrusion( shape=south_half, path=linepath )

# Magnetic field arrow through a coil
B_arrow = arrow(pos=vector(3.5, 0, 0), axis=vector(0, 2, 0),
                shaftwidth=0.1, color=color.cyan)

# Electric field / current direction arrow
E_arrow = arrow(pos=vector(0,0,0), axis=vector(-5, 0, 0),
                shaftwidth=0.1, color=color.yellow)

# Torque vector on the magnet
torque_arrow = arrow(pos=vector(0,0,0), axis=vector(0, 0, 5),
                     shaftwidth=0.1, color=color.magenta)


# def change_box_size(s):
#     my_box.length = s.value
# def change_cylinder_radius(r):
#     cyl.radius = r.value

# slider(bind=change_box_size, min=0.5, max=3, value=1, text="Box Size \n")
# slider(bind=change_cylinder_radius, min=1, max=10, value=1, text="cylinder radius \n")

# ball = sphere(color=color.cyan)



# Keep the window alive in VS Code terminal
input("\nPress [ENTER] in the terminal to close the canvas...")

os._exit(0);