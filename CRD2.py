import os
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
import ezdxf

sg.set_options(font=('D2Coding', 12))

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

    ## Colors
    # 0 : white
    # 1 : red
    # 2 : yellow
    # 3 : green
    # 4 : cyan
    # 5 : blue
    # 6 : violet
    # 7 : white
    # 8 : grey
def SaveDXF(XhE,YhE,XeE,YeE,XhR,YhR,XeR,YeR,X_0,Y_0,Z1,Z2,rhE,rhR,khE,khR,R1,R2,bearing_dia,input_dia,X_e,X_pin,Y_pin,pin_hole_dia,pin_dia,angle_pins,pins):
    doc = ezdxf.new('R2000')
    msp = doc.modelspace()
    # Tooth of Eccentric Disc
    Xdxf0E,YdxfE = Rotation(XhE,YhE,2*np.pi/khE,1)
    Xdxf1E,Ydxf1E = Transform(Xdxf0E,YdxfE,X_0+X_e,Y_0)
    Xdxf2E,Ydxf2E = Transform(XeE,YeE,X_0+X_e,Y_0)
    cpoint1E = [(Xdxf1E[0],Ydxf1E[0])]
    cpoint2E = [(Xdxf2E[0],Ydxf2E[0])]
    for i in range(0,len(Xdxf1E)) :
        cpoint1E.append((Xdxf1E[i],Ydxf1E[i]))
        cpoint2E.append((Xdxf2E[i],Ydxf2E[i]))
    msp.add_spline(cpoint1E,dxfattribs={'color':4})
    msp.add_spline(cpoint2E,dxfattribs={'color':4})
    # Tooth of Ring Gear
    Xdxf0R,Ydxf0R = Rotation(XhR,YhR,2*np.pi/khR,1)
    Xdxf1R,Ydxf1R = Transform(Xdxf0R,Ydxf0R,X_0,Y_0)
    Xdxf2R,Ydxf2R = Transform(XeR,YeR,X_0,Y_0)
    cpoint1R = [(Xdxf1R[0],Ydxf1R[0])]
    cpoint2R = [(Xdxf2R[0],Ydxf2R[0])]
    for i in range(0,len(Xdxf1R)) :
        cpoint1R.append((Xdxf1R[i],Ydxf1R[i]))
        cpoint2R.append((Xdxf2R[i],Ydxf2R[i]))
    msp.add_spline(cpoint1R)
    msp.add_spline(cpoint2R)
    # Pitch Circles
    msp.add_circle((X_0+X_e,Y_0),radius=R2,dxfattribs={'color':4})
    msp.add_circle((X_0,Y_0),radius=R1,dxfattribs={'color':0})
    # Bearing Circles
    msp.add_circle((X_0+X_e,Y_0),radius=bearing_dia/2,dxfattribs={'color':4})
    msp.add_circle((X_0,Y_0),radius=input_dia/2)
    # Pin holes
    X_pinhole_cen1 = X_0+X_pin+X_e
    Y_pinhole_cen1 = Y_0+Y_pin
    X_pinhole_cen2,Y_pinhole_cen2 = Transform(X_pinhole_cen1,Y_pinhole_cen1,-X_0-X_e,-Y_0)
    for i in range(0,pins):
        X_pinhole_cen3,Y_pinhole_cen3 = Rotation(X_pinhole_cen2,Y_pinhole_cen2,angle_pins,i)
        X_pinhole_cen4,Y_pinhole_cen4 = Transform(X_pinhole_cen3,Y_pinhole_cen3,X_0+X_e,Y_0)
        msp.add_circle((X_pinhole_cen4,Y_pinhole_cen4),radius=pin_hole_dia/2,dxfattribs={'color':4})
    # Pins
    X_pin_cen1 = X_0+X_pin
    Y_pin_cen1 = Y_0+Y_pin
    X_pin_cen2,Y_pin_cen2 = Transform(X_pin_cen1,Y_pin_cen1,-X_0,-Y_0)
    for i in range(0,pins):
        X_pin_cen3,Y_pin_cen3 = Rotation(X_pin_cen2,Y_pin_cen2,angle_pins,i)
        X_pin_cen4,Y_pin_cen4 = Transform(X_pin_cen3,Y_pin_cen3,X_0,Y_0)
        msp.add_circle((X_pin_cen4,Y_pin_cen4),radius=pin_dia/2,dxfattribs={'color':6})
    # Deco for Ring Gear
    X_START_RING = R1+8*rhR+X_0
    Y_START_RING = Y_0
    X_END_RING = R1+X_0
    Y_END_RING = Y_0
    msp.add_line([X_START_RING,Y_START_RING],[X_END_RING,Y_END_RING])
    X_START_RING2,Y_START_RING2 = Transform(X_START_RING,Y_START_RING,-X_0,-Y_0)
    X_START_RING3,Y_START_RING3 = Rotation(X_START_RING2,Y_START_RING2,2*np.pi/Z1,1)
    X_START_RING4,Y_START_RING4 = Transform(X_START_RING3,Y_START_RING3,X_0,Y_0)
    X_END_RING2,Y_END_RING2 = Transform(X_END_RING,Y_END_RING,-X_0,-Y_0)
    X_END_RING3,Y_END_RING3 = Rotation(X_END_RING2,Y_END_RING2,2*np.pi/Z1,1)
    X_END_RING4,Y_END_RING4 = Transform(X_END_RING3,Y_END_RING3,X_0,Y_0)
    msp.add_line([X_START_RING4,Y_START_RING4],[X_END_RING4,Y_END_RING4])
    msp.add_arc(center=(X_0,Y_0), radius=R1+8*rhR, start_angle=0, end_angle=360/Z1)
    # Deco for Eccentric Disc
    X_START_DISC = R2-8*rhE+X_0+X_e
    Y_START_DISC = Y_0
    X_END_DISC = R2+X_0+X_e
    Y_END_DISC = Y_0
    msp.add_line([X_START_DISC,Y_START_DISC],[X_END_DISC,Y_END_DISC],dxfattribs={'color':4})
    X_START_DISC2,Y_START_DISC2 = Transform(X_START_DISC,Y_START_DISC,-X_0-X_e,-Y_0)
    X_START_DISC3,Y_START_DISC3 = Rotation(X_START_DISC2,Y_START_DISC2,2*np.pi/Z2,1)
    X_START_DISC4,Y_START_DISC4 = Transform(X_START_DISC3,Y_START_DISC3,X_0+X_e,Y_0)
    X_END_DISC2,Y_END_DISC2 = Transform(X_END_DISC,Y_END_DISC,-X_0-X_e,-Y_0)
    X_END_DISC3,Y_END_DISC3 = Rotation(X_END_DISC2,Y_END_DISC2,2*np.pi/Z2,1)
    X_END_DISC4,Y_END_DISC4 = Transform(X_END_DISC3,Y_END_DISC3,X_0+X_e,Y_0)
    msp.add_line([X_START_DISC4,Y_START_DISC4],[X_END_DISC4,Y_END_DISC4],dxfattribs={'color':4})
    msp.add_arc(center=(X_0+X_e,Y_0), radius=R2-8*rhE, start_angle=0, end_angle=360/Z2 ,dxfattribs={'color':4})
    # Output
    Result = os.path.join(WorkingDirectory, f'Result.dxf')
    doc.saveas(Result)

def CRD2_PLOT(M,Z1,Ze,pins,X_0,Y_0,BEARING_FACTOR,PIN_HOLE_FACTOR,X_pin):
    # Setup figure
    fig = plt.figure(figsize=(13,13))
    plt.axes().set_aspect('equal')
    plt.title('Cycloidal Eccentric Reducer Designer 2')
    plt.grid(True)
    # Parameters
    R1 = Z1*M/2
    Resolution1 = 20
    Z2 = Z1-Ze
    R2 = Z2*M/2
    Resolution2 = 20
    X_e = -(R2-R1)
    seg_circle = 360
    bearing_dia = 2*R2*BEARING_FACTOR
    pin_hole_dia = (R2-bearing_dia/2)*PIN_HOLE_FACTOR
    pin_dia = pin_hole_dia-2*X_e
    angle_pins = 2*np.pi/pins
    I=Z2/(Z2-Z1)
    # Eccentric Disc
    XhE,YhE,rhE,khE = Hypocycloid(R2,Z2,Resolution2)
    for i in range(0,int(2*Z2)):
        if(i%2!=0): # Case in Odd Number
            Xh1,Yh1 = Rotation(XhE,YhE,2*np.pi/khE,i)
            Xh2,Yh2 = Transform(Xh1,Yh1,X_0+X_e,Y_0)
            plt.plot(Xh2,Yh2,'-',linewidth=1.5,color='blue',label='_nolegend_')
    XeE,YeE,reE,keE = Epycycloid(R2,Z2,Resolution1)
    for i in range(0,int(2*Z2)):
        if(i%2==0): # Case in Even Number
            Xe1,Ye1 = Rotation(XeE,YeE,2*np.pi/keE,i)
            Xe2,Ye2 = Transform(Xe1,Ye1,X_0+X_e,Y_0)
            plt.plot(Xe2,Ye2,'-',linewidth=1.5,color='blue',label='_nolegend_')
    # Ring Gear
    XhR,YhR,rhR,khR = Hypocycloid(R1,Z1,Resolution1)
    for i in range(0,int(2*Z1)):
        if(i%2!=0): # Case in Odd Number
            Xh1,Yh1 = Rotation(XhR,YhR,2*np.pi/khR,i)
            Xh2,Yh2 = Transform(Xh1,Yh1,X_0,Y_0)
            plt.plot(Xh2,Yh2,'-',linewidth=1.5,color='black',label='_nolegend_')
    XeR,YeR,reR,keR = Epycycloid(R1,Z1,Resolution2)
    for i in range(0,int(2*Z1)):
        if(i%2==0): # Case in Even Number
            Xe1,Ye1 = Rotation(XeR,YeR,2*np.pi/keR,i)
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
    #X_pin = (R2+bearing_dia/2)/2
    Y_pin = 0.0
    for i in range(0,pins):
        XX,YY = Circle(pin_hole_dia,seg_circle)
        XX,YY = Transform(XX,YY,X_pin,Y_pin)
        XX2,YY2 = Rotation(XX,YY,angle_pins,i)
        XX2,YY2 = Transform(XX2,YY2,X_0+X_e,Y_0)
        plt.plot(XX2,YY2, '-', linewidth=1.5, color='blue')
    # Pin on Output Shaft
    for i in range(0,pins):
        XX,YY = Circle(pin_dia,seg_circle)
        XX,YY = Transform(XX,YY,X_pin,Y_pin)
        XX2,YY2 = Rotation(XX,YY,angle_pins,i)
        XX2,YY2 = Transform(XX2,YY2,X_0,Y_0)
        plt.plot(XX2,YY2, '-', linewidth=1.5, color='orange')
    # Annotate
    Cheight = 2*R1/40
    Nrow = 11*Cheight
    plt.text(X_0,Y_0+Nrow/2-Cheight*0, 'Z1=%s[ea]'%(Z1),
        verticalalignment='center', horizontalalignment='center', color='black', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*1, 'Z2=%s[ea]'%(Z2),
        verticalalignment='center', horizontalalignment='center', color='blue', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*2, 'Pitch Dia1=%s[mm]'%(2*R1),
        verticalalignment='center', horizontalalignment='center', color='black', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*3, 'Pitch Dia2=%s[mm]'%(2*R2),
        verticalalignment='center', horizontalalignment='center', color='blue', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*4, 'Tooth Circle Dia1=%s[mm]'%(2*R1/(2*Z1)),
        verticalalignment='center', horizontalalignment='center', color='black', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*5, 'Tooth Circle Dia2=%s[mm]'%(2*R2/(2*Z2)),
        verticalalignment='center', horizontalalignment='center', color='blue', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*6, 'Reduction Ratio=%s'%(I),
        verticalalignment='center', horizontalalignment='center', color='red', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*7, 'Eccentric Distance=%s[mm]'%(X_e),
        verticalalignment='center', horizontalalignment='center', color='green', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*8, 'Pin Dia=%s[mm]'%(pin_dia),
        verticalalignment='center', horizontalalignment='center', color='orange', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*9, 'Pin Hole Dia=%s[mm]'%(pin_hole_dia),
        verticalalignment='center', horizontalalignment='center', color='blue', fontsize="large")
    plt.text(X_0,Y_0+Nrow/2-Cheight*10, 'Bearing Dia=%s[mm]'%(bearing_dia),
        verticalalignment='center', horizontalalignment='center', color='blue', fontsize="large")
    # dxf
    SaveDXF(XhE,YhE,XeE,YeE,XhR,YhR,XeR,YeR,X_0,Y_0,Z1,Z2,rhE,rhR,khE,khR,R1,R2,bearing_dia,input_dia,X_e,X_pin,Y_pin,pin_hole_dia,pin_dia,angle_pins,pins)
    # Figure
    Result = os.path.join(WorkingDirectory, f'Result.png')
    plt.savefig(Result,dpi=100)
    plt.show()

##############################
# GUI
sg.theme('Default')
col = [[sg.Text('Working Directory :',size=(15,1)), sg.Input('./Result/',key='-WorkingDirectoty-',size=(16,1)), sg.FolderBrowse()],
        [sg.Text('Pitch Dia, D1 =',size = (32,1)),sg.Input(38.0,key='-D1-',size = (10,1)),sg.Text('[mm]')],
       [sg.Text('Teeth Number of Ring, Z1 =',size = (32,1)),sg.Input(38,key='-Z1-',size = (10,1)),sg.Text('[ea], (Even Number)')],
       [sg.Text('Diff. of Ring and Disc, Ze =',size = (32,1)),sg.Input(2,key='-Ze-',size = (10,1)),sg.Text('[ea]')],
       [sg.Text('Number of Pins, pins =',size = (32,1)),sg.Input(16,key='-pins-',size = (10,1)),sg.Text('[ea]')],
       [sg.Text('Pin X Position =',size = (32,1)),sg.Input(2.0,key='-PIN_XPOS-',size = (10,1)),sg.Text('[mm]')],
       [sg.Text('Center Position, X_0 =',size = (32,1)),sg.Input(0.0,key='-X_0-',size = (10,1)),sg.Text('[mm]')],
       [sg.Text('Center Position, Y_0 =',size = (32,1)),sg.Input(0.0,key='-Y_0-',size = (10,1)),sg.Text('[mm]')],
       [sg.Text('Bearing Size =',size = (32,1)),sg.Input(21.0,key='-BEARING_SIZE-',size = (10,1)),sg.Text('[mm]')],
       [sg.Text('Pin Size =',size = (32,1)),sg.Input(2.0,key='-PIN_SIZE-',size = (10,1)),sg.Text('[mm]')],
       [sg.Button('Run'), sg.Button('Exit')]]

layout = [[col]]
window = sg.Window('CRD2',layout,icon="CRD2.ico")

while True:
    event, values = window.read()

    try:
        WorkingDirectory = values['-WorkingDirectoty-']
        D1 = float(values['-D1-'])
        Z1 = int(values['-Z1-'])
        M = D1/Z1
        Ze = int(values['-Ze-'])
        pins = int(values['-pins-'])
        X_pin = float(values['-PIN_XPOS-'])
        X_0 = float(values['-X_0-'])
        Y_0 = float(values['-Y_0-'])
        BEARING_SIZE = float(values['-BEARING_SIZE-'])
        BEARING_FACTOR = BEARING_SIZE/(M*(Z1-Ze))
        PIN_SIZE = float(values['-PIN_SIZE-'])
        PIN_HOLE_FACTOR = (PIN_SIZE+Ze*M) / ((Z1-Ze)*M/2-BEARING_SIZE/2)
    except:
        sg.popup('Type error.')

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Run':
        os.makedirs(WorkingDirectory, exist_ok=True)
        CRD2_PLOT(M,Z1,Ze,pins,X_0,Y_0,BEARING_FACTOR,PIN_HOLE_FACTOR,X_pin)

window.close()
