# Brushless-DC-Motor-Sim
AP Physics C Final Project
by Ethan Lin and Zixi Qiao

Overview:

    A DC motor uses magnetic forces between a current carrying solenoid and a magnetic field to generate torque on the motor, causing it to spin. The currents have to be constantly switching, or commutating, to reorient the magnet. In a brushed DC motor, that is done by physical and mechanical commutators.

    However, this is a simulation of a brushless DC motor with a 6 block commutation algorithm. This motor contains a cylindrical magnet (rotor) in the center surrounded by three stator solenoids (aka windings/phases) that connect at a star point, where the commutation is done electrically. In a motor, the maximum torque is generated when the magnetic fields of the rotor and stator are orthogonal. 6 step commutation mimics that by turning on phases (or sending currents through phases) such that the net B field is orthogonal to the rotor's B field.
    To do that, one hall sensor is place physically in the midpoint of each phase (labeled hall sensor 1, 2, and 3 counterclockwise, which corresponds to index 0, 1, and 2). A hall sensor will report a value of 1 when it is facing the north pole of the rotor magnet, and 0 at the south pole.
    
      Assuming that position theta (not the same one in the code) of 0 degrees corresponds to the angle at +x. At t=0, the B-field is at 90 degrees. This gives us all the sensor possible combinations, which correspond to the magnet B-Field being at the positions:
    Hall sensor combination          ==>          B-Field Angle position
    [1, 0, 1]                                   ==>              (-30, 30) (Sector 0)
    [1, 0, 0]                                   ==>              (30, 90) (Sector 1)
    [1, 1, 0]                                   ==>              (90, 150) (Sector 2)
    [0, 1, 0]                                   ==>              (150, 210) (Sector 3)
    [0, 1, 1]                                   ==>              (210, 270) (Sector 4)
    [0, 0, 1]                                   ==>             (270, 330) (Sector 5)
    
    We can model the current in each phase on a 2d plane using a 3-axis graph, where each axis is 120 degrees apart from each other (phase A at 0 degrees, phase B at 120 degrees, and phase C at 240 degrees) and join at the origin. Currents going into a phase (represented by attaching that phase to positive voltage) will be pointing towards the origin, and current coming out a phase (represented by attaching that phase to Ground (GND) or 0V) will be pointing away from the origin. Since only 2 phases will be phases will be connected to a voltage at a time, they will both be in series, and have currents of equal magnitudes.
    
    Because the angle at which the currents enter into a motor phase doesn't matter, we can reorient all of the phase currents to be parallel to the B field vectors they produce, simplifying the model. If the current vectors have equal magnitudes, so do the B-field vectors. Call the sum of the B field vectors B_net.

    The average B field angle of a rotor B field in sector 0 is 0 degrees, so B_net should sum to 90 degrees, which can be achieved by sending current into phase C (creating B-field vector of 60 degrees) and recieving current from phase B (creating B-field vector of 120 degrees), yielding a B_net of 90 degrees. As we repeat this process for other sectors, we get the following table:
            **third column shows which rail (+V or GND) is conencted to which phase
    Hall sensor combination          ==>          B-Field Angle position            ==>           (+V, GND)
    [1, 0, 1]                                   ==>              (-30, 30) (Sector 0)            ==>           (C,B)
    [1, 0, 0]                                   ==>              (30, 90) (Sector 1)             ==>           (A,B)
    [1, 1, 0]                                   ==>              (90, 150) (Sector 2)            ==>           (A,C)
    [0, 1, 0]                                   ==>              (150, 210) (Sector 3)          ==>           (B,C)
    [0, 1, 1]                                   ==>              (210, 270) (Sector 4)          ==>           (B,A)
    [0, 0, 1]                                   ==>             (270, 330) (Sector 5)          ==>           (C,A)

    We then assign each phase to the voltages described according to this chart.
    
    By cycling forward in the phases (Sector 1 -> 2-->3-->4-->5-->0), we get torque and angular acceleration in the +Z axis (counterclockwise) about the axis of the rotor, causing changes in angular velocity. As the rotor rotates, it will change its Sector (or block), and the commutation logic will shift and adjust to it so that we can get the most torque. Over time, the greater angular velocity will generate a higher back EMF (due to a high rate change in magnetic flux) on the connected inductors. This will reduce the effective current in each inductor, thus reducing the torque generate. This negative feedback loop, combined with the friction on the rotor (from spinning elements like bearings) will limit the motor's angular speed.

Physics:

For the rotor to rotate, we must calculate the torque on each phase's dipole moment inside the rotor's magnetic field. The magnetic dipole moment determines how strong the magnetic field will be inside/around the solenoid as well as how much the solenoid will rotate inside the field. The formula to find the phase's dipole moment 
mu = number of coils * phase current * coil area * coil axis, where coil axis denotes the direction of mu. You also scale this by the relative core permeability of each coil, which affects the magnetic field generated by any given dipole moment. Then, you find the cross product of mu and the magnet's B field to find torque.

Additionally, when the magnet rotates, you have to account for the back EMF generated that affects each phase's current, accelerating or decelerating the magnet. The formula for this is EMF = -N dφ/dt = -N d(BA)/dt = - N A dB/dt, where N is the number of coils, dφ/dt is the change in flux with respect to time, A is the area of the coil's cross-section, and B is the magnet's B field on the coil. In each time step, we calculate the current magnet's B field and store the previous value of the magnet's B field. Next, we divide by the time step to get the approximate dB/dt. Then, we use Kirchhoff's Voltage Law to find the current in each phase.

For simplicity's sake, we assume the circuit reaches steady-state instantly and treat it as purely resistive, ignoring the inductor's opposition to changing current.


Graphs:

We graph the torque on the rotor vs the angle of the rotor. We also graph the angular velocity, angular acceleration, induced back EMFs, and current in each phase with respect to time.


Visual Indicators: 

The cyan arrow shows the rotor magnet's B-field direction.
The orange arrow shows the net stator B-field direction.
The yellow arrow shows the net current/electric field direction in the active windings.
The magenta ring's radius represents the magnitude of the torque.


User Controls:

Sliders:

Magnet Strength (Gauss)- Adjusts the strength of the rotor's magnetic field from 0G to 1678G. A stronger magnet increases both the torque produced for a given current and the back-EMF induced at a given speed.

Battery Voltage (V)- Allows the user to adjust the battery voltage from 6.94V-27V. Higher voltages allows for more current in each coil, which affects the force and torque generation of the motor.

Turns per coil (turns/coil)- Allows the user to adjust the number of turns on the coil from 10-30. More turns lead to a longer wire length per solenoid, which increases the amount of back EMF and reduces the current proportionally.

Relative Core Permeability (µ/µ_0)- The core permeability affects how effectively the stator windings generate magnetic field for a given current.

Magnet Mass (kg)- Allows the user to adjust the mass of the cylindrical magnet. An increase in magnet mass increases the inertia of the rotor, which dampens/ smoothens angular acceleration (reduces the size of angular acceleration fluctuations).

Buttons:

Reset Button - Reset the time of the simulation to time = 0 seconds. It also clears the graph, resets the diagram,and resets the simulation sliders and input to default values.

Toggles Axes - Toggles the visibility of the X, Y, and Z axis arrows on the diagram.