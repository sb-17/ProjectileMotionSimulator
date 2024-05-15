from tkinter import *
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

def load_2D():
    exec(open("ProjectileMotion2D.py").read())
    
def load_3D():
    exec(open("ProjectileMotion3D.py").read())

root = Tk()
root.title("Projectile Motion Simulator")
root.geometry("600x400")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(4, weight=1)

title = Label(root, text="Select Mode\n", font=("Arial", 12)).grid(row=1, column=2)

button2D = Button(root, text="2D", command=load_2D).grid(row=2, column=1)
button3D = Button(root, text="3D", command=load_3D).grid(row=2, column=3)

root.mainloop()