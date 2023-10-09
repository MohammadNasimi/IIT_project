import openpyxl
import numpy as  np
import matplotlib.pyplot as plt
from math import *
# Import curve fitting package from scipy
from scipy.optimize import curve_fit
# Initialization
# R =   float(input('Insert Radius of indenter = '))
R = 0.79
# n =   float(input('Insert strain hardening coefficient = '))
n=0.2
# m =   float(input('Insert number of cycles = '))
m=9
# h =   float(input('Insert first indentation depth = '))
h=0.01
# d =   float(input('Insert indentations interval = '))
d=0.01
# tol1= float(input('Insert tolerance for n = '))
tol1=0.01
# tol2= float(input('Insert tolerance for yield point ='))
tol2=0.01    

def estimate_p_h_max_slope(depth_max, number_cycle,unloading_ratio,depth,load):
    def objective_linear(x, a, b):
        return a * x + b
    use_for_slope = round((unloading_ratio/10)*2/5)
    P_Max=[]
    h_max =[]
    slop_cycle = []
    Width_origin_cycle = []
    depth_change=[]
    depth_end_up = depth_max/number_cycle
    count =0
    depth_change=[x/10000 for x in depth]
    for j in range(1,number_cycle+1):
        
        for i in range(count,len(depth)):
            if depth_end_up<depth[i]:
                    count = i+1
                    # print(count,depth[i],load[i])
                    h_max.append(depth_change[i])
                    P_Max.append(load[i])
                    start=count-1
                    break
        depth_end_down = depth_end_up*unloading_ratio/100
        for i in range(count,len(depth)):
            if depth_end_down+1>depth[i]:
                    count = i+1
                    # print(count,depth[i])
                    end =count-1
                    break
            if depth_end_down == depth_max*unloading_ratio/100:
                depth_end_down = depth_end_down +7
        end = start + int((end-start)/use_for_slope)
        x_linear, y_linear =  depth_change[start+20:end],load[start+20:end]
        popt, _ = curve_fit(objective_linear, x_linear,y_linear)
        slope, Width_origin = popt
        slop_cycle.append(slope)
        Width_origin_cycle.append(Width_origin)
        depth_end_up = depth_end_up + depth_max/number_cycle
        
    return P_Max,h_max,slop_cycle,Width_origin_cycle

def estimate_Mechanical_properties(depth,load,R,n,m,h,d,tol1,tol2,depth_max, number_cycle,unloading_ratio):   
    P_Max,h_max,slop_cycle,Width_origin_cycle=estimate_p_h_max_slope(depth_max, number_cycle,unloading_ratio,depth,load)
    def power_fit(x,a,b):
        return a * x ** b
    while 1:
        E = 0
        t = 0
        stress = []
        strain = []
        for i in range(len(P_Max)):
            t=t+1

            hm = h_max[i]
            Fm = P_Max[i]
            a = slop_cycle[i]
            b = Width_origin_cycle[i]
            b= abs(1)
            f_perime = a * b * hm**( b  - 1)

            S = f_perime
            hd = 0.75*(Fm/S)
            hstarc = h + (t-1)*d - hd
            hstarp = hstarc*0.131*(1-3.423*n + 0.079*n**2)*((1+6.258*(h+(t-1)*d)*R - 8.072*((h+(t-1)*d)/R)**2))
            hc = hstarp+hstarc
            Ac = pi*(2*R*hc - hc**2)
            a = sqrt(Ac/pi)
            e = 0.14*a/(R-h-(t-1)*d)
            s = Fm/(3*Ac)*2
            EIIT = S*sqrt(pi)/(2*sqrt(Ac))
            Es = 0.91/(1/EIIT-8.729e-7)
            E = E+Es
            stress.append(s)
            strain.append(e)
            plt.plot(e,s,'bo')
            plt.pause(0.3)
                # Calling the curve_fit function
        params, covariance = curve_fit(f = power_fit, xdata = strain, ydata = stress)
        k = params[0]
        k =k
        N = params[1]
        # print(strain)
        # print(stress)
        if abs(n-N)>tol1:
            n = (n+N)/2
        else:          
            break
    n = N
    E = E/m
    #  Second Loop
    ee ={}
    j = 1
    ee[j] = 0.003
    while 1:
        ee[j+1] = round((k*ee[j]**n + 0.002*E)/E,5)  
        if abs(ee[j+1]-ee[j]) > tol2:
            j=j+1 
        else:
            ey = ee[j+1]
            sy = k*ee[j+1]**n
            # print('ey=',ey)
            # print('sy=',sy)
            break
    # print('k=',k)
    # print('E=',E)
    # print('n=',n)
    # print('elastic=',E*ey)
    # print('plastic=',k*ey**N)
    x1 = np.array([0,sy/E])
    x2 = np.array([ey,ey+0.02,ey+0.03,ey+0.04,ey+0.05,ey+0.06,ey+0.07,ey+0.09,ey+0.1])
    plt.xlabel('ُStrain')
    plt.ylabel('Stress')
    plt.plot(x1, x1*E,c='red',ls='-',lw=2) # elastic 
    plt.pause(0.05)
    plt.plot(x2, power_fit(x2,k,N),c='red',ls='-',lw=2) #plasti
    # plt.plot(x2, k*x2**N,c='red',ls='-',lw=2) #plasti
    plt.pause(0.05)
    plt.plot(sy/E+0.001,sy+0.02,'r.',markersize=20)
    plt.pause(0.05)
    plt.show(block=False)
    return ey,sy,k,E,n




