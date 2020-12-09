import numpy as np
import matplotlib.pyplot as plt
import math

file = open("decawavedatafloor.txt", "r")

# lists for recalculated positions
x_calculated = []
y_calculated = []

# lists for original position coordinates calculated by decawave
x_original = []
y_original = []
z_original = []

for row in file:
    row = row.rstrip()
    # CD37[0.00,0.00,0.00]=2.80 1495[0.00,3.99,0.00]=2.74 
    #   592F[5.00,0.00,0.00]=3.60 5B01[5.00,3.99,0.00]=3.70 
    #   le_us=3387 est[1.90,1.96,0.15,91]
    # split the row to string array    
    pieces = row.split()

    measurements = []

    # read the anchor coordinates, ranges and original position    
    for p in pieces:
        if (p[:5] == "le_us"):
            continue
        elif p[:3] == "est":
            # est[1.90,1.96,0.15,91]
            xyz = p[p.find('[')+1 : p.find(']')]
            xyza = xyz.split(',')
            x_original.append(float(xyza[0]))
            y_original.append(float(xyza[1]))
            z_original.append(float(xyza[2]))
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
            measurements.append(measurement)

    if len(measurements) >= 2:
        # define matrices for 2D ToF calculation using least squares method
        # ranges Nx1
        ranges = np.zeros((len(measurements), 1))
        i = 0
        for m in measurements:
            ranges[i][0] = m["range"]   
            i += 1     
        # estimated position 2x1
        x = np.array([[3],[1]])
        # direction cosines Nx2
        H = np.zeros((len(measurements), 2))
        # estimated ranges Nx1
        estimated_ranges = np.zeros((len(measurements), 1))

        # iterate until the delta_x becomes small enough
        ii = 0
        while ii < 20:

            i = 0
            for m in measurements:
                estimated_ranges[i][0] = \
                    math.sqrt((m["x"] - x[0][0])**2 + (m["y"] - x[1][0])**2) 
                H[i][0] = (m["x"] - x[0][0]) / estimated_ranges[i][0]
                H[i][1] = (m["y"] - x[1][0]) / estimated_ranges[i][0]
                i += 1

            # observed minus predicted ranges
            delta_roo = ranges - estimated_ranges
            # pseudoinverse
            delta_x = np.linalg.inv(np.transpose(H) @ H) @ np.transpose(H)\
                @ delta_roo
            x = x - delta_x
            if np.linalg.norm(delta_x) < 0.001:
                break
            ii+=1
        print(x[0][0], x[1][0])

        x_calculated.append(x[0][0])
        y_calculated.append(x[1][0])
file.close()
plt.plot(x_calculated, y_calculated,'b.')
plt.show()
plt.plot(x_original, y_original,'r.')
plt.show()
print("Mean and std of the recalculated solution")
print(np.mean(x_calculated), np.mean(y_calculated))
print(np.std(x_calculated), np.std(y_calculated))
print("Mean and std of the original solution")
print(np.mean(x_original), np.mean(y_original))
print(np.std(x_original), np.std(y_original))
