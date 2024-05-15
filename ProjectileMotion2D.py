from tkinter import *
import numpy as np
import sympy as sp
import plotly.express as px
import matplotlib.pyplot as plt

root = Tk()
root.title("2D Projectile Motion Simulator")
root.geometry("600x400")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(4, weight=1)

airResistance = False

title2D = Label(root, text="Initial Data Entry\n", font=("Arial", 12)).grid(row=1, column=2)

angleLabel = Label(root, text="Initial angle (deg)").grid(row=2, column=1)
angleEntry = Entry(root)
angleEntry.grid(row=2, column=3)

initialVelocityLabel = Label(root, text="Initial velocity").grid(row=3, column=1)
initialVelocityEntry = Entry(root)
initialVelocityEntry.grid(row=3, column=3)

massLabel = Label(root, text="Mass").grid(row=4, column=1)
massEntry = Entry(root)
massEntry.grid(row=4, column=3)

gravityAccelerationLabel = Label(root, text="Gravity acceleration").grid(row=5, column=1)
gravityAccelerationEntry = Entry(root)
gravityAccelerationEntry.grid(row=5, column=3)

dragCoefficientLabel = Label(root, text="Drag coefficient").grid(row=6, column=1)
dragCoefficientEntry = Entry(root)
dragCoefficientEntry.grid(row=6, column=3)

windVelocityLabel = Label(root, text="Wind velocity").grid(row=7, column=1)
windVelocityEntry = Entry(root)
windVelocityEntry.grid(row=7, column=3)

def AirResistance():
    global airResistance
    airResistance = not airResistance

Checkbutton(root, text="Air resistance", command=AirResistance).grid(row=8, column=2)

def graph(xpoints, ypoints, angle, v_0, m, g, c, v_air):
    plt.plot(xpoints, ypoints)
    plt.annotate("Initial angle: " + str(angle) + "\n" + "Initial velocity: " + str(v_0) + "\n" + "Mass: " + str(m) + "\n" + "Gravitational acceleration: " + str(g) + "\n" + "Drag coefficient: " + str(c) + "\n" + "Air velocity: " + str(v_air),
                    xy=(0.05, 0.7), xycoords='axes fraction')
    plt.show()


def calc():
    global angleEntry, initialVelocityEntry, massEntry, gravityAccelerationEntry, dragCoefficientEntry, windVelocityEntry

    xpoints = []
    ypoints = []

    angle = float(angleEntry.get())
    v_0 = float(initialVelocityEntry.get())
    m = float(massEntry.get())
    g = float(gravityAccelerationEntry.get())
    c = float(dragCoefficientEntry.get())
    v_air = float(windVelocityEntry.get())

    global airResistance
    v_xinit = np.round(np.cos(np.deg2rad(angle)), 6) * v_0
    v_yinit = np.round(np.sin(np.deg2rad(angle)), 6) * v_0

    if airResistance == False:
        time = v_0*2/g

        lastx = 0
        for t in np.arange(0, time, 0.001):
            currentY = v_yinit*t-(1/2)*g*t**2
            if currentY < 0:
                break
            ypoints.append(currentY)
            lastx += 0.001*v_xinit
            xpoints.append(lastx)

    else:
        x, y = sp.symbols('x y')

        for t in np.arange(0, 10000, 0.01):
            eqx = sp.Eq(x, (m*(v_xinit-v_air)*sp.exp(-c*t/m)
                        * (sp.exp(c*t/m)-1))/c+v_air*t)
            eqy = sp.Eq(y, ((m**2*g+c*m*v_yinit)/c**2)
                        * (1-sp.exp(-c*t/m))-m*g*t/c)
            currentY = sp.nsolve(eqy, y, 0.01)
            if currentY < 0:
                break
            ypoints.append(currentY)
            currentX = sp.nsolve(eqx, x, 0.01)
            xpoints.append(currentX)

    graph(xpoints, ypoints, angle, v_0, m, g, c, v_air)

graphItButton = Button(root, text="Graph it!", command=calc).grid(row=9, column=2)

root.mainloop()
