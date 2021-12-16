import os
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt

##############################
# Function
def Rotation(Xtemp,Ytemp,ANGLE,i):
    XX = np.cos(ANGLE*i)*Xtemp - np.sin(ANGLE*i)*Ytemp
    YY = np.sin(ANGLE*i)*Xtemp + np.cos(ANGLE*i)*Ytemp
    return XX,YY

def Transform(Xtemp,Ytemp,X_t,Y_t):
    Xtemp = Xtemp + X_t
    Ytemp = Ytemp + Y_t
    return Xtemp,Ytemp

def Hypocycloid(R,Z,Resolution):
    rh = R/(2*Z)
    kh = R/rh
    THETAh = np.linspace(0,2*np.pi/kh,Resolution)
    Xh = rh*(kh-1)*np.cos(THETAh)+rh*np.cos((kh-1)*THETAh)
    Yh = rh*(kh-1)*np.sin(THETAh)-rh*np.sin((kh-1)*THETAh)
    return Xh,Yh,rh,kh

def Epycycloid(R,Z,Resolution):
    re = R/(2*Z)
    ke = R/re
    THETAe = np.linspace(0,2*np.pi/ke,Resolution)
    Xe = re*(ke+1)*np.cos(THETAe)-re*np.cos((ke+1)*THETAe)
    Ye = re*(ke+1)*np.sin(THETAe)-re*np.sin((ke+1)*THETAe)
    return Xe,Ye,re,ke

def Circle(DIA,SEG_CIRCLE):
    THETA0 = np.linspace(0.0,2*np.pi,SEG_CIRCLE)
    XX = DIA/2*np.sin(THETA0)
    YY = DIA/2*np.cos(THETA0)
    return XX,YY

def CRD2_PLOT(M,Z1,Ze,pins,X_0,Y_0):
    fig = plt.figure(figsize=(13,13))
    plt.axes().set_aspect('equal')
    plt.title('Cycloidal Eccentric Reducer Designer 2')
    plt.grid(True)

    R1 = Z1*M/2
    Resolution1 = 20
    Z2 = Z1-Ze
    R2 = Z2*M/2
    Resolution2 = 20
    X_e = -(R2-R1)
    seg_circle = 360
    bearing_dia = 2*R2*0.6
    pin_dia = (bearing_dia/2-R2)*0.4
    angle_pins = 2*np.pi/pins
    I=Z2-Z1/Z2

    ###################
    # Eccentric Disc
    Xh,Yh,rh,kh = Hypocycloid(R2,Z2,Resolution2)
    for i in range(0,int(2*Z2)):
        if(i%2!=0): # Case in Odd Number
            Xh1,Yh1 = Rotation(Xh,Yh,2*np.pi/kh,i)
            Xh2,Yh2 = Transform(Xh1,Yh1,X_0+X_e,Y_0)
            plt.plot(Xh2,Yh2,'-',linewidth=1.5,color='blue',label='_nolegend_')

    Xe,Ye,re,ke = Epycycloid(R2,Z2,Resolution1)
    for i in range(0,int(2*Z2)):
        if(i%2==0): # Case in Even Number
            Xe1,Ye1 = Rotation(Xe,Ye,2*np.pi/kh,i)
            Xe2,Ye2 = Transform(Xe1,Ye1,X_0+X_e,Y_0)
            plt.plot(Xe2,Ye2,'-',linewidth=1.5,color='blue',label='_nolegend_')

    ###################
    # Ring Gear
    Xh,Yh,rh,kh = Hypocycloid(R1,Z1,Resolution1)
    for i in range(0,int(2*Z1)):
        if(i%2!=0): # Case in Odd Number
            Xh1,Yh1 = Rotation(Xh,Yh,2*np.pi/kh,i)
            Xh2,Yh2 = Transform(Xh1,Yh1,X_0,Y_0)
            plt.plot(Xh2,Yh2,'-',linewidth=1.5,color='black',label='_nolegend_')

    Xe,Ye,re,ke = Epycycloid(R1,Z1,Resolution2)
    for i in range(0,int(2*Z1)):
        if(i%2==0): # Case in Even Number
            Xe1,Ye1 = Rotation(Xe,Ye,2*np.pi/kh,i)
            Xe2,Ye2 = Transform(Xe1,Ye1,X_0,Y_0)
            plt.plot(Xe2,Ye2,'-',linewidth=1.5,color='black',label='_nolegend_')

    # Pitch Cicle of Ring Gear
    XX,YY = Circle(2*R1,seg_circle)
    XX,YY = Transform(XX,YY,X_0,Y_0)
    plt.plot(XX,YY, ':', linewidth=1.0, color='red')

    # Pitch Cicle of Eccentric Disc
    XX,YY = Circle(2*R2,seg_circle)
    XX,YY = Transform(XX,YY,X_0+X_e,Y_0)
    plt.plot(XX,YY, ':', linewidth=1.0, color='red')

    # Bearing on Eccentric Disc
    XX,YY = Circle(bearing_dia,seg_circle)
    XX,YY = Transform(XX,YY,X_0+X_e,Y_0)
    plt.plot(XX,YY, '-', linewidth=1.5, color='blue')

    # Input Shaft
    input_dia = bearing_dia-2*X_e
    XX,YY = Circle(input_dia,seg_circle)
    XX,YY = Transform(XX,YY,X_0,Y_0)
    plt.plot(XX,YY, '-', linewidth=1.5, color='black')

    # Pin holes on Eccentric Disc
    pin_hole_dia = pin_dia-2*X_e
    X_pin = (R2+bearing_dia/2)/2
    Y_pin = 0.0
    for i in range(0,pins):
        XX,YY = Circle(pin_hole_dia,seg_circle)
        XX,YY = Transform(XX,YY,X_pin,Y_pin)
        XX2,YY2 = Rotation(XX,YY,angle_pins,i)
        XX2,YY2 = Transform(XX2,YY2,X_0+X_e,Y_0)
        plt.plot(XX2,YY2, '-', linewidth=1.5, color='blue')

    # Pin on Output Shaft
    X_pin = (R2+bearing_dia/2)/2
    Y_pin = 0.0
    for i in range(0,pins):
        XX,YY = Circle(pin_dia,seg_circle)
        XX,YY = Transform(XX,YY,X_pin,Y_pin)
        XX2,YY2 = Rotation(XX,YY,angle_pins,i)
        XX2,YY2 = Transform(XX2,YY2,X_0,Y_0)
        plt.plot(XX2,YY2, '-', linewidth=1.5, color='orange')
        
    # Annotate
    Cheight = 2*R1/40
    Nrow = 6*Cheight
    plt.text(X_0,Y_0+Nrow/2-Cheight*0, 'Z1=%s[ea]'%(Z1),
        verticalalignment='center', horizontalalignment='center', color='black', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*1, 'Z2=%s[ea]'%(Z2),
        verticalalignment='center', horizontalalignment='center', color='blue', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*2, 'Pitch Dia1=%s[mm]'%(2*R1),
        verticalalignment='center', horizontalalignment='center', color='black', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*3, 'Pitch Dia2=%s[mm]'%(2*R2),
        verticalalignment='center', horizontalalignment='center', color='blue', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*4, 'Reduction Ratio=%s'%(I),
        verticalalignment='center', horizontalalignment='center', color='red', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*5, 'Eccentric Distance=%s[mm]'%(2*X_e),
        verticalalignment='center', horizontalalignment='center', color='green', fontsize="large")

    plt.show()

##############################
# GUI
sg.theme('Default')
col = [[sg.Text('Module, M =',size = (32,1)),sg.Input(1.0,key='-M-',size = (10,1)),sg.Text('[mm], (>0)')],
       [sg.Text('Teeth Number of Ring, Z1 =',size = (32,1)),sg.Input(40,key='-Z1-',size = (10,1)),sg.Text('[ea], (>30)')],
       [sg.Text('Diff. of Ring and Disc, Ze =',size = (32,1)),sg.Input(2,key='-Ze-',size = (10,1)),sg.Text('[ea]')],
       [sg.Text('Number of Pins, pins =',size = (32,1)),sg.Input(6,key='-pins-',size = (10,1)),sg.Text('[ea]')],
       [sg.Text('Center Position, X_0 =',size = (32,1)),sg.Input(0.0,key='-X_0-',size = (10,1)),sg.Text('[mm]')],
       [sg.Text('Center Position, Y_0 =',size = (32,1)),sg.Input(0.0,key='-Y_0-',size = (10,1)),sg.Text('[mm]')],
       [sg.Button('Run'), sg.Button('Exit')]]

layout = [[col]]
window = sg.Window('CRD2',layout)

while True:
    event, values = window.read()

    try:
        M = float(values['-M-'])
        Z1 = int(values['-Z1-'])
        Ze = int(values['-Ze-'])
        pins = int(values['-pins-'])
        X_0 = float(values['-X_0-'])
        Y_0 = float(values['-Y_0-'])
    except:
        sg.popup('Type error.')

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Run':
        CRD2_PLOT(M,Z1,Ze,pins,X_0,Y_0)

window.close()


