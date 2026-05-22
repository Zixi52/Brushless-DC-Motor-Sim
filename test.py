import vpython as py
from vpython import *

canva = canvas(width=600, height=600, background=color.white) 

canva.forward = vector(0, 0, -1)
canva.center = vector(0, 0, 0)
canva.userzoom = False   # Disables scroll wheel zoom
canva.userspin = False   # Disables right-click rotation
canva.userpan = False    # Disables shift-click object sliding/panning
canva.autoscale = False  # Prevents camera from jumping around

print("hello world")

# Create your geometry
my_box = box(color=color.blue)
cyl = cylinder(pos=vec(0, 0, 0), axis=vec(0, 0, 3), color=color.red)


def change_box_size(s):
    my_box.length = s.value

def change_cylinder_radius(r):
    cyl.radius = r.value

slider(bind=change_box_size, min=0.5, max=3, value=1, text="Box Size \n")
slider(bind=change_cylinder_radius, min=1, max=10, value=1, text="cylinder radius \n")

# Keep the window alive in VS Code terminal
ball = sphere(color=color.cyan)


#Ethan;'s first python code 
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



input("\nPress [ENTER] in the terminal to close the canvas...")



