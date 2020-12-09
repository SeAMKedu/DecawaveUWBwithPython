import numpy as np
import matplotlib.pyplot as plt
import math

file = open("decawavedatafloor.txt", "r")

# lists for recalculated positions
x_calculated = []
y_calculated = []

for row in file:
    row = row.rstrip()
    # print(row)

    # split the row to string array    
    pieces = row.split()

    # list of measurements
    measurements = []

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

    if len(measurements) >= 2:
        # estimated position 2x1
        x = np.array([[3],[3]])

        # range measurements Nx1
        ranges = np.zeros((len(measurements), 1))
        i = 0
        for m in measurements:
            ranges[i][0] = m["range"]   
            i += 1     

        # estimated ranges Nx1
        estimated_ranges = np.zeros((len(measurements), 1))

        # direction cosines Nx2
        H = np.zeros((len(measurements), 2))

        # iterate until the delta_x becomes small enough
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
        # print(x[0][0], x[1][0])

        x_calculated.append(x[0][0])
        y_calculated.append(x[1][0])
    # end if len(measurements) >= 2:
# end for row in file:
file.close()
plt.plot(x_calculated, y_calculated,'b.')
plt.show()

