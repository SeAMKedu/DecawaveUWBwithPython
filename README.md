# Position estimation from Decawave DWM1001 distance measurements

This tutorial shows how the position of a tag can be estimated from the raw distance measurements made by Decawave MDEK1001 development kit.

Decawave MDEK1001 is a development kit for indoor positioning application utilizing ultra-wideband (UWB) radio technology. UWB enables the accurate measure of the time of flight of the radio signal, leading to centimeter accuracy in the range measurement and positioning. 

If you have a Decawave MDEK1001 development kit, you can set up the system and collect data from Decawave modules by yourself. Otherwise, you can start from sample data of this page, and test the algorithm to be developed with that data.

The first chapters contain instructions how to setup the DWM1001 system and how to collect the raw distance data from the system. You can skip these chapters, if you want to use existing sample data instead, and start from the chapter [Sample test data](#sample-test-data).

Instructions for position estimation algorithms are given in chapter [Position estimation](#position-estimation). The position is calculated in 2D using least-squares solution.

## DWM1001 Development Kit

MDEK1001 development kit contains 12 encased development boards (DWM1001-DEV) and necessary software for system setup, networking and positioning. Each DWM1001-DEV module can be configured as an anchor or a tag. DWM1001-DEV modules use Bluetooth for communication and UWB for ranging. More information about MDEK1001 Development Kit can be found [here](https://www.decawave.com/product/mdek1001-deployment-kit/).

The figure below shows an DWM1001-DEV module.

![](images/mdek1001.PNG)

The system contains also Android application, which can be used for module configuration and positioning. Alternatively, the module configuration can be done by using the UART shell mode.

## System setup with Android application

Document [MDEK1001 Quick Start Guide](https://www.decawave.com/mdek1001/quickstart/) contains the instructions to set up the system quickly by using Android application. Four DWM1001-DEV modules are used as anchors and one module is used as a tag, which position will be estimated. 

![](images/Anchors.JPG)

After configuring the anchors and tags, the coordinates of anchors can be determined automatically by using Android application's Auto-Positioning function. However, it is recommended to measure the anchor coordinates manually with one cm accuracy or better.

After the configuration phase, the Android application is ready for estimating the position of the tag. 

## System setup using the UART shell mode

MDEV1001 module firmware contains an APIs to to create a network and configure the nodes directly over UART. Instructions for that are found from DWM1001 Gateway Quick Deployment Guide, which can be found [here](https://www.decawave.com/product/mdek1001-deployment-kit/). (Download "DWM1001, DW10001-DEV and MDEK1001 Documents, Source Code, Android Application & Firmware Image" zip package at the end of page.)

Connect the DWM1001-DEV to the PC over USB and launch a telnet client (for example TeraTerm or PuTTY). Set the baud rate as 115200. In the telnet client shell press `Enter` twice in order to start DWM1001 UART shell mode.

Each DWM1001-DEV module is configured either as Initiator, Anchor or Tag. 

- Anchor is used as reference to calculate tag position with trilateration. Position coordinates of the anchors are known.
- Initiator is an anchor, which will initialize the network. A network must contain at least one initiator.
- Tag is a mobile node whose position will be estimated.

All of the initiators, anchors and tags must have a common network ID (PAN ID).

Configure one module as an **Initiator** by following commands:

- `nis 0x1234`: set up the node PAN ID to 0x1234
- `aps 0 0 0`: set up the node coordinates to x = 0, y = 0, z = 0. Coordinates are given as millimeters.
- `nmi`: configure the node as initiator (and anchor) and reset the device. The UART shell mode is re-entered by sending `Enter` twice.

The node status is obtained by command `si`.

Configure three modules as **Anchors** by following commands:

- `nis 0x1234`: set up the node PAN ID to 0x1234
- `aps 1000 2000 0`: set up the node coordinates to x = 1 m, y = 2 m, z = 0. Coordinates are given as millimeters.
- `nma`: configure the node as anchor and reset the device.

Configure one module as a **Tag** by following commands:

- `nis 0x1234`: set up the node PAN ID to 0x1234
- `nmt`: configure the node as tag and reset the device.

## Collecting data using UART shell mode

The raw range measurements and position estimated by the Decawave system can be obtained with the UART shell mode. 

Connect the **tag module** to the PC over USB and launch a telnet client. In the telnet client shell press `Enter` twice in order to start DWM1001 UART shell mode. Send the `les` command to tag.

The tag starts to send raw range and position data to the telnet client window:

```python
dwm> les
CD37[0.00,0.00,0.00]=2.80 1495[0.00,3.99,0.00]=2.74 592F[5.00,0.00,0.00]=3.60 5B01[5.00,3.99,0.00]=3.70 le_us=3387 est[1.90,1.96,0.15,91]
CD37[0.00,0.00,0.00]=2.76 1495[0.00,3.99,0.00]=2.75 592F[5.00,0.00,0.00]=3.61 5B01[5.00,3.99,0.00]=3.73
...
```

Collect some data and save the data to a text file for further analysis.

## Sample test data

File [decawavedatafloor.txt](example/decawavedatafloor.txt) contains sample raw range and position data. One line contains the range measurements from the tag to each anchor, anchor coordinates and the estimated position.

```python
CD37[0.00,0.00,0.00]=2.80 1495[0.00,3.99,0.00]=2.74 592F[5.00,0.00,0.00]=3.60 5B01[5.00,3.99,0.00]=3.70 le_us=3387 est[1.90,1.96,0.15,91]
CD37[0.00,0.00,0.00]=2.76 1495[0.00,3.99,0.00]=2.75 592F[5.00,0.00,0.00]=3.61 5B01[5.00,3.99,0.00]=3.73 le_us=3387 est[1.90,1.94,0.24,90]
CD37[0.00,0.00,0.00]=2.79 1495[0.00,3.99,0.00]=2.74 592F[5.00,0.00,0.00]=3.75 5B01[5.00,3.99,0.00]=3.65 le_us=3387 est[1.89,1.98,0.36,85]
CD37[0.00,0.00,0.00]=2.78 1495[0.00,3.99,0.00]=2.74 592F[5.00,0.00,0.00]=3.61 5B01[5.00,3.99,0.00]=3.65 le_us=3631 est[1.89,1.97,0.41,90]
CD37[0.00,0.00,0.00]=2.80 1495[0.00,3.99,0.00]=2.71 592F[5.00,0.00,0.00]=3.66 5B01[5.00,3.99,0.00]=3.69 le_us=3418 est[1.90,1.99,0.14,88]
CD37[0.00,0.00,0.00]=2.77 1495[0.00,3.99,0.00]=2.74 592F[5.00,0.00,0.00]=3.69 5B01[5.00,3.99,0.00]=3.70 le_us=3387 est[1.90,2.00,0.05,95]
```

A line has the following information:

```python
CD37[0.00,0.00,0.00]=2.80 # anchor id = CD31, anchor position [0.00,0.00,0.00], distance 2.80
1495[0.00,3.99,0.00]=2.74 # anchor id = 1495, anchor position [0.00,3.99,0.00], distance 2.74
592F[5.00,0.00,0.00]=3.60 # anchor id = 592F, anchor position [5.00,0.00,0.00], distance 3.60
5B01[5.00,3.99,0.00]=3.70 # anchor id = 5B01, anchor position [5.00,3.99,0.00], distance 3.70
le_us=3387
est[1.90,1.96,0.15,91] # tag position and quality estimated by Decawave [1.90,1.96,0.15,91]
```

The figure below shows the anchor and tag positions during the data collection. The anchors were located at the corners of a 5 m x 4 m area. The anchor at the lower right corner was used as Initiator and origin of the coordinate system. The positions of the anchors were determined with tape measure with 1 or 2 cm accuracy. Also the distance from the tag were measured with tape measure. The tag was located approximately to position [2, 2, 0]. Because the anchors and the tag were at the same height the position can be estimated in 2D.

![](images/testsetup.PNG)

## Position estimation

Because the anchor or tag clocks are not synchronized to a common time reference, a double sided two-way ranging method is employed to measure the signal propagation delay. The distance or range is obtained by multiplying the two-way signal propagation delay by the speed of light, and then by dividing by 2.

The position is estimated by intersecting circles (2D) or spheres (3D) with radius *r<sub>i</sub>* and centre (*x<sub>i</sub>*, *y<sub>i</sub>*), as illustrated below.

![](images/Circles2.PNG)    (1)

Radius of the circle *r<sub>i</sub>* is obtained from the measured range. Point (*x<sub>i</sub>*, *y<sub>i</sub>*) is the known location of the base station transmitting or receiving the signal. When the distance measurements *r<sub>i</sub>* are available from at least two anchors, the
two-dimensional location of the receiver (*x<sub>u</sub>*, *y<sub>u</sub>*) can be solved from the following
set of non-linear equations 

![](images/eq1.gif)    (2)

where *i* ranges from 1 to N and references the base stations at known locations, (*x<sub>i</sub>*, *y<sub>i</sub>*) denote the *i*th base station coordinates in two dimensions, and *r<sub>i</sub>* is the range measurement from *i*th base station.

The nonlinear equation above can be solved for the unknowns by using either closed form solutions or by iterative methods based on linearization. The equation can be linearized by using Taylor series expansion (not explained here). 

Linearization yields the following equation: 

![](images/eq2.gif)    (3)

where  (*ˆx<sub>u</sub>*, *ˆy<sub>u</sub>*)  is an approximate position estimate, and *ˆρ<sub>i</sub>* is an approximated pseudorange, and (*Δx<sub>u</sub>*, *Δy<sub>u</sub>*) is the displacement from the approximate position to the true position, and 

![](images/eq3.GIF)    (4)

Equation 3 is simplified by introducing new variables where

![](images/eq3c.GIF).   (5)

Equation 3 can be written now more simply as 

![](images/eq3d.GIF).   (6)

In Equation 6 there are two unknowns (*Δx<sub>u</sub>*, *Δy<sub>u</sub>*) which can be solved by making ranging measurements to at least two base stations. The unknown displacement can be determined from Equation 7 shown in matrix form

![](images/eq4.GIF)    (7)

where

![](images/eq5.GIF)    (8)

Equation 7 has the following solution (pseudoinverse is used when there are more measurements that unknowns). 

![](images/eq6.GIF)

Matrix **H** is the direction cosine matrix containing unit vectors pointing from the linearization point to the location of the ith base station, **Δx** is the offset of the user from the linearization point, and **Δρ** contains differences between the predicted and observed ranges.

User’s position is calculated by using an iterative process. At the system startup the approximated location is set to some initial value. The center of the locationing area is  a good choice.  Next the direction cosine matrix **H** and the predicted-minus-observed pseudorange **Δρ** vector are computed. After that, the unknown displacement vector **Δx** is calculated by using Equation 7. A new approximate position is obtained by adding the displacement vector to the estimated position vector calculated at the previous round. The iteration process is repeated until the length of the displacement vector does not become smaller any more. 

## Exercise 1

Make a Python program, which estimates the position of the tag from the data collected from Decawave UWB system. The anchor coordinates and the range measurements are obtained from file [decawavedatafloor.txt](example/decawavedatafloor.txt). The contents of the data file are described [Sample test data](#sample-test-data).

Make a Python file called calc.py. Import first the libraries needed for mathematics and plotting. Introduce lists for x and y coordinates of calculated position. Open the file for reading and go through the lines in the file. Print the lines to the console.

```python
import numpy as np
import matplotlib.pyplot as plt
import math

# lists for recalculated positions
x_calculated = []
y_calculated = []

file = open("decawavedatafloor.txt", "r")

for row in file:
    row = row.rstrip()
    print(row)
```

Each line contains the following information:

```
CD37[0.00,0.00,0.00]=2.80 1495[0.00,3.99,0.00]=2.74 592F[5.00,0.00,0.00]=3.60 5B01[5.00,3.99,0.00]=3.70 le_us=3387 est[1.90,1.96,0.15,91]
```

Split the line to a list of strings by using space as a deliminiter and introduce a list for measurements:

```python
for row in file:
    row = row.rstrip()
    # print(row)

    # split the row to string array    
    pieces = row.split()

    # list of measurements
    measurements = []
```

Go through the list of strings and parse the anchor coordinates and the range measurement from the string ```1495[0.00,3.99,0.00]=2.74```. We will omit the fields le_us and est.

```python
    # get the anchor coordinates, ranges and original position    
     for p in pieces:
        if (p[:5] == "le_us"):
            continue
        elif p[:3] == "est":
            continue
        else:       
            # 1495[0.00,3.99,0.00]=2.74
            measurement = {}
            measurement["id"] = p[:p.find('[')]
            xyz = p[p.find('[')+1 : p.find(']')]
            xyza = xyz.split(',')
            measurement["x"] = float(xyza[0])
            measurement["y"] = float(xyza[1])
            measurement["z"] = float(xyza[2])
            measurement["range"] = float(p[p.find('=')+1 : ])
            # append the measurement to the list of measurements of this epoch
            measurements.append(measurement)
    # end for p in pieces:            
```
If there are at least two measurements, the position can be estimated. Define first the vector ***x*** for the estimated position and initialize it with some coordinate values inside the positioning area.
```python
    # end for p in pieces:

    if len(measurements) >= 2:
        # estimated position 2x1
        x = np.array([[3],[3]])
```

Make next the vector **ρ** for the measured ranges and vector **^ρ** for the estimated ranges.
```python
        # range measurements Nx1
        ranges = np.zeros((len(measurements), 1))
        i = 0
        for m in measurements:
            ranges[i][0] = m["range"]   
            i += 1     
            
        # estimated ranges Nx1
        estimated_ranges = np.zeros((len(measurements), 1))
```

Initialize then the direction cosine matrix **H** with zeroes
```python
        # direction cosines Nx2
        H = np.zeros((len(measurements), 2))
```

After the vector and matrix initializations, estimate the location of the tag **ρ** iteratively.
In each round calculate the delta position towards the true position and add it to the estimated
position calculated at the previous iteration cycle. Stop the iteration, when the length of the
delta position becomes very small.

```python
        ii = 0
        while ii < 20:

            i = 0
            for m in measurements:
                # calculate the predicted ranges
                estimated_ranges[i][0] = \
                    math.sqrt((m["x"] - x[0][0])**2 + (m["y"] - x[1][0])**2) 
                # calculate the direction cosines
                H[i][0] = (m["x"] - x[0][0]) / estimated_ranges[i][0]
                H[i][1] = (m["y"] - x[1][0]) / estimated_ranges[i][0]
                i += 1

            # observed minus predicted ranges
            delta_roo = ranges - estimated_ranges
            # pseudoinverse
            delta_x = np.linalg.inv(np.transpose(H) @ H) @ np.transpose(H)\
                @ delta_roo
            # subtract the delta position from the position calculated
            # in previous round
            x = x - delta_x
            # stop iteration when the delta position becomes small enough
            if np.linalg.norm(delta_x) < 0.001:
                break
            ii+=1
        # end while ii < 20:
```

Add the calculated position coordinates x and y to the list:

```python
        # end while ii < 20:
        # print(x[0][0], x[1][0])

        x_calculated.append(x[0][0])
        y_calculated.append(x[1][0])
    # end if len(measurements) >= 2:
# end for row in file:
```

Finally close the file and plot the calculated position coordinates.

```python
# end for row in file:
file.close()
plt.plot(x_calculated, y_calculated,'b.')
plt.show()
```

The complete program can be found [here](example/decawavedatafloor.txt).

# Exercise 2

Modify the program so that you can compare the recalculated position to the position calculated 
by the Decawave module originally. The original position vector can be found from the field *est*
at the end of the row.

# Exercise 3

Make the calculation in three dimensions. 
