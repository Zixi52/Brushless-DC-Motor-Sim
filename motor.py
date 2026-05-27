import vpython as py
from vpython import *
##Web VPython 3.2
# -------------------------------GLOBAL CONSTANTS-------------------------------------
pi_2_3=2*pi/3
# -------------------------------GLOBAL VARIABLES-------------------------------------
stator_r =4
motor_length = 10
originAxesLength = 3
temp_v1 =-2
batteryV =0

s_length = 200

dt=1/50
dw= 1*2*pi
w=0
t=0
# ------------------------------------------------CAMERA SETTINGS------------------------------------------------
canva = canvas(width=600, height=600, background=color.white, fov = 0.01, resizable=False, align = 'right') 
def setDefaultView(evt):
    canva.forward = vector(0, 0, -1)
    canva.center = vector(0, 0, 1)
light = local_light(pos=vec(0, 0, -2*motor_length), color=color.white)
canva.userzoom = False   # Disables scroll wheel zoom
canva.userspin = True   # Disables right-click rotation
canva.userpan = True    # Disables shift-click object sliding/panning
canva.autoscale = True  # Prevents camera from jumping around
print("hello world")
#========================STATOR=================================
stator_core_line = [ vec(0,0,(temp_v1)), vec(0,0, (temp_v1-motor_length)) ]
hollow_stator_circle= shapes.circle(radius= stator_r, np= 40, angle1 = 0.0, angle2 = 4*pi/2, thickness =.1) 
stator_core =extrusion( color=color.gray(.7), shape=hollow_stator_circle, path=stator_core_line, opacity=1, twosided=True)
hollow_motor_shell= shapes.circle(radius= stator_r*1.85, np= 40, angle1 = 0.0, angle2 = 4*pi/2, thickness =.1) 
motor_shell =extrusion( color=color.gray(0), shape=hollow_motor_shell, path=stator_core_line, opacity=1)

# Coil cores (arranged in a ring around the magnet) to show copper winding
winding = [None,None,None]
core = [None,None,None]
for i in range(len(core)):
    v = vector(stator_r*cos(pi_2_3*i), stator_r*sin(pi_2_3*i), (stator_core_line[0].z+stator_core_line[1].z)/2)
    v2=vector(cos(pi_2_3*i), sin(pi_2_3*i), 0)
    winding[i]=helix(pos=v,axis=v2,
                  radius=3, coils=8, thickness=0.2, color=color.orange,
                  thicknesses=0.02, size =vec(2,4,motor_length)) #4 is the width of inductor
    core[i] =box(pos= vec(v.x*1.3, v.y*1.3, v.z), length=3, height=2, width=motor_length*.5, color=color.gray(.7), axis = v2)
def changeNumberCoils(evt):
    print(evt)
    for i in range(len(winding)):
        winding[i].coils = evt.value
     
# CREATE XYZ ORIGIN AXIS 
originAxes = [
    arrow(pos=vec(0, 0, 0), axis=vec(originAxesLength, 0, 0), color=color.red, shaftwidth=originAxesLength/10,),
    arrow(pos=vec(0, 0, 0), axis=vec(0, originAxesLength, 0), color=color.green, shaftwidth=originAxesLength/10),
    arrow(pos=vec(0, 0, 0), axis=vec(0, 0, originAxesLength), color=color.blue, shaftwidth=originAxesLength/10)]
originLabels = [None, None, None]
originTexts = ["X", "Y", "Z"]
for i in range(len(originLabels)):
    originLabels[i] = text(pos =originAxes[i].axis, color =originAxes[i].color, text =originTexts[i], height=.5)
def showOrigin (evt):
    if evt.text == 'axes on': #if the button has this on click
        for i in range(len(originAxes)):
            originAxes[i].opacity=0.0
            originLabels[i].opacity=0.0
        clrbtn.text = 'axes off'
    else:
        for i in range(len(originAxes)):
            originAxes[i].opacity=1.0
            originLabels[i].opacity=1.0
        clrbtn.text = 'axes on'
##=============================ALL USER INPUTS============================
def resetTimer(evt):
    s=evt.key
    if(s == 'r'):
        w_dots.data=[]
        t_dots.data=[]
        iCurves[0].data =[]
        iCurves[1].data =[]
        iCurves[2].data =[]
        t =0
        rotateKW(-w)
        w=0
canva.bind('keydown', resetTimer)
canva.append_to_caption(' PRESS R TO RESTART AND BOOM  ') 

clrbtn = button( bind=showOrigin, text='axes on')
canva.append_to_caption('   ') 
setDefaultView_b = button( bind=setDefaultView, text=' Reset View')

canva.append_to_caption('\n\n  Turns per Length (5-15 turns/m):') 
n_slider = slider(bind=changeNumberCoils, max=15, min=5, step=1, value=5, id='x',align = 'none', length=s_length)
   
def changeCorePermeability(evt):
    new_hue=1 -evt.value/n_slider.max
    for i in range(len(core)):
        core[i].color = color.gray(new_hue)
# canva.append_to_caption('Core Permeability/Permeability of Free Space (1-5000): \n') 
canva.append_to_caption('Core Permeability/µ_0 (1-5000): ') 
n_slider = slider(bind=changeCorePermeability, min=1, max=5000, step=1, value=2, id='x', align = 'none', length=s_length)

def changeBatteryV(evt):
    batteryV = evt.value
canva.append_to_caption('\n\n Battery Voltage (6V-694V): ') 
V_slider = slider(bind=changeBatteryV, min=6, max=694, step=1, value=6, id='x', align = 'none', length=s_length)
canva.append_to_caption('') 

def changeMagnetStrength(evt):
    magnetBField = evt.value
canva.append_to_caption(' Magnet Strength (27G-9470G): ') 
V_slider = slider(bind=changeMagnetStrength, min=27, max=9470, step=1, value=6, id='x', align = 'none', length=s_length)
canva.append_to_caption('') 

def changeMagnetMass(evt):
    magnetMass = evt.value
canva.append_to_caption('\n\n Magnet Mass (.1kg-1678kg): ') 
V_slider = slider(bind=changeMagnetMass, min=.1, max=1678, step=.1, value=6, id='x', align = 'none', length=s_length)
canva.append_to_caption('') 
##=========================================================
#permanent magnet (rotating cylinder in the center)
# magnet = cylinder(pos=vector(0,0,0), axis=vector(0,0,1), radius=3, length=0.6,
#                   color=color.red, texture=textures.metal)
magnetSweep = [ vec(0, 0, temp_v1), vec(0, 0,temp_v1-motor_length) ]
north_disk= shapes.circle(radius= 3.5, np= 22, scale =1, angle1=0, angle2 = pi)
northPole = extrusion( shape=north_disk, path=magnetSweep, color= color.red, opacity=1, twosided=True)

south_disk= shapes.circle(radius= 3.5, np= 22, scale =1, angle1=pi, angle2 = 2*pi)
southPole = extrusion( shape=south_disk, path=magnetSweep,color= color.blue , twosided=True)
mag = compound([northPole, southPole], axis = vec(1,0,0))

        
# Magnetic field arrow through a coil
B_arrow = arrow(pos=vector(3.5, 0, 0), axis=vector(0, 2, 0),
                shaftwidth=0.2, color=color.cyan)
# Electric field / current direction arrow
E_arrow = arrow(pos=vector(0,0,0), axis=vector(-5, 0, 0),
                shaftwidth=0.1, color=color.yellow)
# Torque vector on the magnet
torque_arrow = arrow(pos=vector(0,0,0), axis=vector(0, 0, 5),
                     shaftwidth=0.1, color=color.magenta)

def rotateKW(w):
        mag.rotate(angle=w, origin=vec(0, 0, 0), axis = vec(0, 0, 1))
# # ================PLAYING IWTH GRPAHS======================
dotSize=2
canva.append_to_caption(' \n') 
g_t = graph(width=600, height=200, xtitle=("Angle (Radians)"), ytitle=("Torque (N*m)"), align='none', scroll =True, xmin =0, xmax = 2*pi)
t_dots=gdots(color=color.green, size= dotSize,graph=g_t)

canva.append_to_caption(' \n') 
g_a = graph(width=600, height=200, xtitle=("Time (seconds)"), ytitle=("Acceleration (N*m)"), align='none', scroll =True, xmin =0, xmax =5)
a_dots=gdots(color=color.green, size= dotSize,graph=g_a)

canva.append_to_caption('  \n ') 
g_bemf = graph(width=800, height=200, xtitle=("Time (seconds)"), ytitle=("Induced Back-EMF (V))"), align='none',scroll =True, xmin =0, xmax = 5)
BEMFCurves = [None, None, None]
BEMFCurves[0]  =gdots(color=color.red, size= dotSize,graph=g_bemf)
BEMFCurves[1]  =gdots(color=color.magenta, size= dotSize,graph=g_bemf)
BEMFCurves[2]  =gdots(color=color.blue, size= dotSize,graph=g_bemf)

canva.append_to_caption('  \n ') 
g_i = graph(width=800, height=200, xtitle=("Time (seconds)"), ytitle=("Current (A)"), align='none',scroll =True, xmin =0, xmax = 5)
iCurves = [None, None, None]
iCurves[0]  =gdots(color=color.red, size= dotSize,graph=g_i)
iCurves[1]  =gdots(color=color.magenta, size= dotSize,graph=g_i)
iCurves[2]  =gdots(color=color.blue, size= dotSize,graph=g_i)


while(1):
    rate(1/dt)
    rotateKW(dw*dt)
    t_dots.plot(w, w % (pi/3) +15)
    a_dots.plot(w, w % (pi/3) +12)
    iCurves[0].plot(t, sin(w))
    iCurves[1].plot(t, sin(w+pi_2_3))
    iCurves[2].plot(t, sin(w-pi_2_3))
    BEMFCurves[0].plot(t, sin(w))
    BEMFCurves[1].plot(t, sin(w+pi_2_3))
    BEMFCurves[2].plot(t, sin(w-pi_2_3))
    w=w+dw*dt
    t=t+dt



# Keep the window alive in VS Code terminal
input("\nPress [ENTER] in the terminal to close the canvas...")
