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
si=20 #marbot be nemodar v takhier andaze

def list_data_lvdt_loadcell():
    df = openpyxl.load_workbook('F:\تحصیلات\ارشد\IIT\code properties material\data\data_all.xlsx')

        # Get workbook active sheet object
        # from the active attribute
    sheet_obj = df.active
    Row_1 =[]
    Row_2 =[]
    #print(sheet_obj.max_column)
    for M in range(1,sheet_obj.max_row+1):
        cell_obj_Row_1 = sheet_obj.cell(row = M, column = 1)
        cell_obj_Row_2 = sheet_obj.cell(row = M, column = 2)
        Row_1.append(cell_obj_Row_1.value)
        Row_2.append(cell_obj_Row_2.value)

    # print('stress=',Row_1)
    # print('strain=',Row_2)
    return Row_1, Row_2

def estimate_mechanical_properties(Row_1,Row_2,R,n,m,h,d,to1,tol2,si = 20):
    while 1:
        E = 0
        t = 0
        stress = []
        strain = []
        count = 0
        for j in range(0,m) :
            t=t+1
            data_stress = []
            data_strain =[]
            for i in range(count,len(Row_2)-1):

                if Row_2[i+1]> Row_2[i]:
                    count = i+1
                    break
                data_stress.append(Row_2[i])
                data_strain.append(Row_1[i])
            # print(data_stress)



            #Row_2 =data_stress
            #Row_1 = data_strain
            hm = data_strain[0]
            Fm = data_stress[0]
            def power_fit(x,a,b):
                return a * x ** b

            # Calling the curve_fit function
            params, covariance = curve_fit(f = power_fit, xdata =data_strain , ydata = data_stress)
            a = params[0]
            b = params[1]

            f_perime = a * b * hm**( b  - 1)

            S = f_perime
            hd = 0.75*(Fm/S)
            hstarc = h + (t-1)*d - hd
            hstarp = hstarc*0.131*(1-3.423*n + 0.079*n**2)*((1+6.258*(h+(t-1)*d)*R - 8.072*((h+(t-1)*d)/R)**2))
            hc = hstarp+hstarc
            Ac = pi*(2*R*hc - hc**2)
            a = sqrt(Ac/pi)
            e = 0.14*a/(R-h-(t-1)*d)
            s = Fm/(3*Ac)
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
        N = params[1]

        

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
    x2 = np.array([ey,0.02,0.03,0.04,0.05,0.06,0.07,0.09,0.1,0.15,0.25])
    plt.xlabel('Stress')
    plt.ylabel('Strain')
    plt.plot(x1, x1*E,c='red',ls='-',lw=2) # elastic 
    plt.pause(0.05)
    plt.plot(x2, power_fit(x2,k,N),c='red',ls='-',lw=2) #plasti
    plt.pause(0.05)
    plt.plot(sy/E,sy+0.02,'r.',markersize=10)
    plt.pause(1000)
    plt.show()
    return ey,sy,k,E,n



