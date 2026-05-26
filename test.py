import vpython as py
from vpython import *
# ------------------------------------------------CAMERA SETTINGS------------------------------------------------
canva = canvas(width=600, height=600, background=color.white) 

canva.forward = vector(0, 0, -1)
canva.center = vector(0, 0, 0)
canva.userzoom = False   # Disables scroll wheel zoom
canva.userspin = False   # Disables right-click rotation
canva.userpan = False    # Disables shift-click object sliding/panning
canva.autoscale = False  # Prevents camera from jumping around
canva.fov = 0.001    
print("hello world")
# ------------------------------------------------GLOBAL VARIABLES------------------------------------------------
stator_r =2
motor_length = 5
#========================STATOR=================================
hollow_stator_circle= shapes.circle(radius= 3, np= 32, scale =2, angle1 = 0.0, angle2 = 3*pi/2) # fix with thickness
linepath = [ vec(0,0,0), vec(0,0,motor_length) ]
extrusion( shape=hollow_stator_circle, path=linepath,color=color.green )

#Ethan's first python code 
# Create XYZ axis 
originAxes = [
    arrow(pos=vec(0, 0, 0), axis=vec(1, 0, 0), color=color.red,shaftwidth=.1,),
    arrow(pos=vec(0, 0, 0), axis=vec(1, 1, 0), color=color.green,shaftwidth=.1),
    arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 1), color=color.blue,shaftwidth=.1)]

def showOrigin (evt):
    if evt.text == 'axes on':
        for origin in originAxes:
                opacity=0.0
                clrbtn.text = 'axes off'
    else:
        for origin in originAxes:
                opacity=1.0
                clrbtn.text = 'axes on'
         
clrbtn = button( bind=showOrigin, text='axes on')
#=========================================================
# permanent magnet (rotating cylinder in the center)
# magnet = cylinder(pos=vector(0,0,0), axis=vector(0,0,1), radius=3, length=0.6,
#                   color=color.red, texture=textures.metal)
north_half= shapes.circle(radius= 2, np= 32, scale =2, angle1=0, angle2 = pi)
linepath = [ vec(0,0,0), vec(0,0,3) ]
extrusion( shape=north_half, path=linepath )

south_half= shapes.circle(radius= 2, np= 32, scale =2, angle1=pi, angle2 = 2*pi)
linepath = [ vec(0,0,0), vec(0,0,3) ]
extrusion( shape=south_half, path=linepath )


# Coil cores (arranged in a ring around the magnet)
# use a helix to show the wire winding
coil_wire = helix(pos=vector(3, 0, 0), axis=vector(0.6, 0, 0),
                  radius=1, coils=8, thickness=0.05, color=color.orange)

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



