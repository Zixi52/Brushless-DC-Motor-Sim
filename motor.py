import vpython as py
from vpython import *
#Web VPython 3.2    
# -------------------------------GLOBAL CONSTANTS-------------------------------------
pi_2_3=2*pi/3
vector_thirds = [vec(cos(0), sin(0), 0), 
                 vec(cos(pi_2_3), sin(pi_2_3), 0),
                 vec(cos(2*pi_2_3), sin(2*pi_2_3), 0)]
# areaVector =[hat(vec()), hat(vec()), hat(vec())]
# -------------------------------GLOBAL VARIABLES-------------------------------------
stator_r =4

# motor_length is also stator length rn
motor_length = 10
originAxesLength = 3
temp_v1 =-2
batteryV =6.94

s_length = 200

t=0
dt=1/50
theta=0
dtheta= 1*2*pi

omega = 0 # angular vel
inertia = 1  # moment of inertia
damping = 1 # friction coefficient

corePermeability = 0
magnetBField = 0
magnetMass = 0.1

phases = [0, 0, 0] # Current in each phase A, B, C respectively, if i != 0 its on
phaseRs = [2, 2, 2] # Resistance in each phase A, B, C respectively
phaseBfields = [0, 0, 0]  #will be in units of T
phaseBEMF = [0, 0, 0] # Back EMFs induced in each phase
lastBField= [magnetBField*cos(theta+pi/2-0),
             magnetBField*cos(theta+pi/2-pi_2_3),
             magnetBField*cos(theta+pi/2+pi_2_3)]#last stored value of the BField perpendicular to each phase

wire_resistivity = 1.68e-8 # copper resistivity (ohm*m)
wire_cross_section = 0.000001 # 1 mm^2

# ------------------------------------------------CAMERA SETTINGS------------------------------------------------
canva = canvas(width=600, height=600, background=color.white, fov = 0.01, resizable=False, align = 'right') 
def setDefaultView(evt):
    canva.forward = vector(0, 0, -1)
    canva.center = vector(0, 0, 1)
light = local_light(pos=vec(0, 0, -2*motor_length), color=color.white)
canva.userzoom = False   # Disables scroll wheel zoom
canva.userspin = False   # Disables right-click rotation
canva.userpan = False    # Disables shift-click object sliding/panning
canva.autoscale = False  # Prevents camera from jumping around
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
    winding[i]=helix(pos=v,axis=hat(v2),
                  radius=3, coils=8, thickness=0.2, color=color.orange,
                  thicknesses=0.01, size =vec(2,4,motor_length)) # 4 is the width of inductor
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
    global theta
    if evt.key == 'r':
        a_curve.data = []
        v_curve.data = []
        t_curve.data = []
        for curve in iCurves + phaseBEMFCurves:
            curve.data = []
        global t, theta, omega
        t = 0
        theta = 0
        omega = 0
        rotatekTheta(-theta)

canva.bind('keydown', resetTimer)
canva.append_to_caption(' PRESS R TO RESTART SIMULATION YAY  ') 

clrbtn = button(bind=showOrigin, text='axes on')
canva.append_to_caption('   ') 
setDefaultView_b = button(bind=setDefaultView, text=' Reset View')

canva.append_to_caption('\n\n  Turns per Length (5-15 turns/m):') 
turns_slider = slider(bind=changeNumberCoils, 
                      max=15, min=5, step=1, value=8, 
                      length=s_length)

def changeNumberCoils(evt):
    for i in range(len(winding)):
        winding[i].coils = evt.value
    updatePhaseResistance()

def changeCorePermeability(evt):
    global corePermeability
    corePermeability = 1 - evt.value / core_slider.max
    for i in range(len(core)):
        core[i].color = color.gray(corePermeability)
canva.append_to_caption('Core Permeability/µ_0 (1-5414 H/m): ') 
core_slider = slider(bind=changeCorePermeability, min=1, max=5414, step=1, value=2, length=s_length)

def changeBatteryV(evt):
    global batteryV
    batteryV = evt.value
canva.append_to_caption('\n\n Battery Voltage (6.94V-51.6V): ') 
battery_slider = slider(bind=changeBatteryV, min=6.94, max=27, step=1, value=6.94, length=s_length)
canva.append_to_caption('') 

def changeMagnetStrength(evt):
    global magnetBField
    magnetBField = evt.value

canva.append_to_caption(' Magnet Strength (0G-167.8G): ') 
magnet_slider = slider(bind=changeMagnetStrength, min=0, max=167.8, step=1, value=0, length=s_length)
canva.append_to_caption('') 

def changeMagnetMass(evt):
    global magnetMass
    magnetMass = evt.value
    updateInertia()
canva.append_to_caption('\n\n Magnet Mass (.1796kg-1.18kg): ') 
mass_slider = slider(bind=changeMagnetMass, min=.1796, max=1.18, step=.1, value=0.1, length=s_length)
canva.append_to_caption('') 

# ====================== UPDATE FUNCTIONS ======================
def updatePhaseResistance(evt=None):
    global phaseRs
    turns_per_meter = turns_slider.value
    turns_per_coil = turns_per_meter * motor_length
    
    coil_radius = stator_r + 1.5
    circumference = 2 * pi * coil_radius
    
    total_wire_length = turns_per_coil * circumference
    resistance_per_phase = wire_resistivity * total_wire_length / wire_cross_section
    
    phaseRs = [resistance_per_phase] * 3

def updateInertia(evt=None):
    global inertia
    rotor_radius = 3.5
    inertia = 0.5 * magnetMass * (rotor_radius ** 2)
##=========================================================
#permanent magnet (rotating cylinder in the center)
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

def rotatekTheta(theta):
        mag.rotate(angle=theta, origin=vec(0, 0, 0), axis = vec(0, 0, 1))
# # ================PLAYING IWTH GRAPHS======================
dotSize=2   
canva.append_to_caption('\n ================================================================= \n Legend : Phase A in RED, Phase B in blue, Phase C in cyan ') 
g_t = graph(width=700, height=300, xtitle=("Angle (Radians)"), ytitle=("Torque (N*m)"), align='none', scroll =True, xmin =0, xmax = 2*pi)
t_curve=gcurve(color=color.magenta, size= dotSize,graph=g_t)

canva.append_to_caption(' ') 
g_v = graph(width=700, height=300, xtitle=("Time (seconds)"), ytitle=("Angular Vel. (Radians / s)"), align='none', scroll =True, xmin =0, xmax =5)
v_curve=gcurve(color=color.cyan, size= dotSize,graph=g_v)

canva.append_to_caption(' ') 
g_a = graph(width=700, height=300, xtitle=("Time (seconds)"), ytitle=("Angular Accel. (Radians / s^2)"), align='none', scroll =True, xmin =0, xmax =5)
a_curve=gcurve(color=color.green, size= dotSize,graph=g_a)

canva.append_to_caption('  ') 
g_bemf = graph(width=800, height=200, xtitle=("Time (seconds)"), ytitle=("Induced Back-EMF (V))"), align='none',scroll =True, xmin =0, xmax = 5)
phaseBEMFCurves = [None, None, None]
phaseBEMFCurves[0]  =gdots(color=color.red, size= dotSize,graph=g_bemf)
phaseBEMFCurves[1]  =gdots(color=color.cyan, size= dotSize,graph=g_bemf)
phaseBEMFCurves[2]  =gdots(color=color.blue, size= dotSize,graph=g_bemf)

canva.append_to_caption('  \n ') 
g_i = graph(width=800, height=200, xtitle=("Time (seconds)"), ytitle=("Current (A)"), align='none',scroll =True, xmin =0, xmax = 5)
iCurves = [None, None, None]
iCurves[0]  =gcurve(color=color.red, size= dotSize,graph=g_i)
iCurves[1]  =gcurve(color=color.cyan, size= dotSize,graph=g_i)
iCurves[2]  =gcurve(color=color.blue, size= dotSize,graph=g_i)

# THE PHYSICS  AND LOGIC BEHIND THIS
# one represents north pole, including error margin to not glitch everything out
def getHallSensors():
    hallSensorValue = [None, None, None] #counterclockwise
    global vector_thirds
    for i in range(len(hallSensorValue)):
        if (dot(vector_thirds[i], getMagnetBField()) > 0):
           hallSensorValue[i] = 1  # the hall sensors sees a north pole 
        else:
            hallSensorValue[i] = 0    # the hall sensors sees a south pole 
    return hallSensorValue

def getMagnetBField():
    global theta, magnetBField
    return magnetBField / 10000 * vec(cos(theta), sin(theta), 0) #returns vector

def calculatePhaseBField():
    global phaseBfields

def calculateBackEMFS():
    global phaseBEMF #in volts
    #the componentof magnet's b field in each direction is 
    getMagnetBField()
    global phaseBEMF, lastBField
    #b field of a,b,c: sonion(theta+pi), sonion(theta+pi/3), sonion(theta-pi/3)
    #db/dt a,b,c: cos(theta+pi), cos(theta+pi/3), cos(theta-pi/3)
    #V= -N dφ/dt
    #V= -N[d(BA)/dt]
    #V= -N(pi*l*w)[dB/dt] for an ellipse cross-section
    sol=winding[0]
    for i in range(len(winding)):
        newBfield =dot(getMagnetBField(),winding[i].axis)
        dφ_dt = (newBfield - lastBField[i])/dt
        phaseBEMF[i]= -sol.coils *sol.size.x*sol.size.y*dφ_dt
        lastBField[i] = newBfield
    # print(phaseBEMF)
    
def applyPhaseCurrents(phase_arr):
    global phases
    for i in range(3):
        if phase_arr[i] == 0:
            phases[i] = 0
            winding[i].color=color.orange
        else:
            phases[i] = phase_arr[i] * batteryV / phaseRs[i]
            if phase_arr[i] == -1:
                winding[i].color=color.red
            else:
                winding[i].color=color.green

def getNewStep():
    hall_sensors = getHallSensors()
    #0 is float
    print("hall:", hall_sensors)
    if (hall_sensors == [1,0,1]):
        applyPhaseCurrents([0, -1, 1])
        #CH BL
    elif (hall_sensors == [1,0,0]):
        applyPhaseCurrents([1, -1, 0])
        #AH BL
    elif (hall_sensors == [1,1,0]):
        applyPhaseCurrents([1, 0, -1])
        #AH CL
    elif (hall_sensors == [0,1,0]):
        applyPhaseCurrents([0, 1, -1])
        #BH CL
    elif (hall_sensors == [0,1,1]):
        applyPhaseCurrents([-1, 1, 0])
        #BH AL  
    elif (hall_sensors == [0,0,1]):
        applyPhaseCurrents([-1, 0, 1])
        #CH AL
 
def calculateTorque():
    B = getMagnetBField()
    torque = 0.0
    L = vec(0, 0, motor_length) # current direction along z
    
    for i in range(3):
        coil_angle = pi_2_3 * i
        r = stator_r * vec(cos(coil_angle), sin(coil_angle), 0) # vector to coil center
        
        # Force on coil: F = N * I * (L × B)
        F = winding[i].coils * phases[i] * cross(L, B)
        
        # Torque vector: tau = r × F
        tau = cross(r, F)
        
        # Component along motor axis (z)
        torque += dot(tau, vec(0, 0, 1))
    
    return torque
    
updatePhaseResistance()
updateInertia()
while(1):
    rate(1/dt)
    getNewStep()
    torque = calculateTorque()
    alpha = (torque - damping * omega) / inertia
    omega += alpha * dt
    theta += omega * dt
    rotatekTheta(omega * dt)
    # print(phases, batteryV, getMagnetBField())
    # rotatekTheta(dtheta*dt)
    calculateBackEMFS()
    t_curve.plot(theta, torque)
    v_curve.plot(t, omega)
    a_curve.plot(t, alpha)
    iCurves[0].plot(t, phases[0])
    iCurves[1].plot(t, phases[1])
    iCurves[2].plot(t, phases[2])
    phaseBEMFCurves[0].plot(t, phaseBEMF[0])
    phaseBEMFCurves[1].plot(t, phaseBEMF[1])
    phaseBEMFCurves[2].plot(t, phaseBEMF[2])
    # theta=theta+dtheta*dt
    t=t+dt