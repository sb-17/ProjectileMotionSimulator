from tkinter import *
import numpy as np
import plotly.express as px

root = Tk()
root.title("3D Projectile Motion Simulator")
root.geometry("600x400")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(4, weight=1)

step = 0.001

airResistance = False

title2D = Label(root, text="Initial Data Entry\n", font=("Arial", 12)).grid(row=1, column=2)

thetaLabel = Label(root, text="Initial angle theta (deg)").grid(row=2, column=1)
thetaEntry = Entry(root)
thetaEntry.grid(row=2, column=3)

phiLabel = Label(root, text="Initial angle phi (deg)").grid(row=3, column=1)
phiEntry = Entry(root)
phiEntry.grid(row=3, column=3)

initialVelocityLabel = Label(root, text="Initial velocity").grid(row=4, column=1)
initialVelocityEntry = Entry(root)
initialVelocityEntry.grid(row=4, column=3)

massLabel = Label(root, text="Mass").grid(row=5, column=1)
massEntry = Entry(root)
massEntry.grid(row=5, column=3)

gravityAccelerationLabel = Label(root, text="Gravity acceleration").grid(row=6, column=1)
gravityAccelerationEntry = Entry(root)
gravityAccelerationEntry.grid(row=6, column=3)

dragCoefficientLabel = Label(root, text="Drag coefficient").grid(row=7, column=1)
dragCoefficientEntry = Entry(root)
dragCoefficientEntry.grid(row=7, column=3)

windVelocityLabel = Label(root, text="Wind velocity").grid(row=8, column=1)
windVelocityEntry = Entry(root)
windVelocityEntry.grid(row=8, column=3)

def AirResistance():
    global airResistance
    airResistance = not airResistance

Checkbutton(root, text="Air resistance", command=AirResistance).grid(row=8, column=2)

def graph(xpoints, ypoints, zpoints, theta, phi, v_0, m, g, c, v_air):
    df = {
        "x": xpoints,
        "y": ypoints,
        "z": zpoints,
        "theta": theta,
        "phi": phi,
        "v_0": v_0,
        "m": m,
        "g": g,
        "c": c,
        "v_air": v_air
    }
    fig = px.scatter_3d(df, x='x', y='y', z='z')
    common_range = [
        min(min(df['x']), min(df['y']), min(df['z'])),
        max(max(df['x']), max(df['y']), max(df['z']))
    ]

    fig.update_layout(
        scene=dict(
            xaxis = dict(range=common_range),
            yaxis = dict(range=common_range),
            zaxis = dict(range=common_range),
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=1)
        )
    )
    fig.show()


def calcTrajectory():
    global thetaEntry, phiEntry, initialVelocityEntry, massEntry, gravityAccelerationEntry, dragCoefficientEntry, windVelocityEntry, airResistance

    xpoints = []
    ypoints = []
    zpoints = []

    theta = float(thetaEntry.get())
    phi = float(phiEntry.get())
    v_0 = float(initialVelocityEntry.get())
    m = float(massEntry.get())
    g = float(gravityAccelerationEntry.get())
    c = float(dragCoefficientEntry.get())
    v_air = float(windVelocityEntry.get())

    v_xinit = np.sin(np.deg2rad(theta))*np.cos(np.deg2rad(phi))*v_0
    v_yinit = np.sin(np.deg2rad(theta))*np.sin(np.deg2rad(phi))*v_0
    v_zinit = np.cos(np.deg2rad(theta))*v_0

    if airResistance == False:
        for t in np.arange(0, 10000, step):
            currentX = v_xinit*t
            currentY = v_yinit*t
            currentZ = v_zinit*t - (1/2)*g*t**2
            if currentZ < 0:
                break
            xpoints.append(currentX)
            ypoints.append(currentY)
            zpoints.append(currentZ)

    else:
        for t in np.arange(0, 10000, step):
            currentX = v_air*t + m/c*(v_xinit - v_air)*(1 - np.exp(-c*t/m))
            currentY = v_yinit*m/c*(1 - np.exp(-c*t/m))
            currentZ = ((m**2*g + c*m*v_zinit)/c**2)*(1 - np.exp(-c*t/m)) - m*g*t/c
            if currentZ < 0:
                break
            xpoints.append(currentX)
            ypoints.append(currentY)
            zpoints.append(currentZ)

    graph(xpoints, ypoints, zpoints, theta, phi, v_0, m, g, c, v_air)

def calcArea():
    global initialVelocityEntry, massEntry, gravityAccelerationEntry, dragCoefficientEntry, windVelocityEntry, airResistance

    xpoints = []
    ypoints = []

    v_0 = float(initialVelocityEntry.get())
    m = float(massEntry.get())
    g = float(gravityAccelerationEntry.get())
    c = float(dragCoefficientEntry.get())
    v_air = float(windVelocityEntry.get())

    for phi in range(0, 360, 8):
        for theta in range(-90, 91, 10):
            v_xinit = np.sin(np.deg2rad(theta))*np.cos(np.deg2rad(phi))*v_0
            v_yinit = np.sin(np.deg2rad(theta))*np.sin(np.deg2rad(phi))*v_0
            v_zinit = np.cos(np.deg2rad(theta))*v_0

            if airResistance == False:
                for t in np.arange(0, 10000, step):
                    currentX = v_xinit*t
                    currentY = v_yinit*t
                    currentZ = v_zinit*t - (1/2)*g*t**2
                    if currentZ < 0:
                        xpoints.append(currentX)
                        ypoints.append(currentY)
                        break

            else:
                for t in np.arange(0, 10000, step):
                    currentX = v_air*t + m/c*(v_xinit - v_air)*(1 - np.exp(-c*t/m))
                    currentY = v_yinit*m/c*(1 - np.exp(-c*t/m))
                    currentZ = ((m**2*g + c*m*v_zinit)/c**2)*(1 - np.exp(-c*t/m)) -m*g*t/c
                    if currentZ < 0:
                        xpoints.append(currentX)
                        ypoints.append(currentY)
                        break
    
    fig = px.scatter(x=xpoints, y=ypoints)
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1
    )
    fig.show()


graphTrajectoryCurveButton = Button(root, text="Graph trajectory curve", command=calcTrajectory).grid(row=10, column=2)
graphRangeAreaButton = Button(root, text="Graph area", command=calcArea).grid(row=11, column=2)

root.mainloop()
