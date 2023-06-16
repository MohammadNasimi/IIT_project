import pandas as pd
import numpy as np
def Residual_Stress(x,y):
    # df = pd.read_excel(file)
    # x = df.iloc[:, 0].tolist()
    # y = df.iloc[:, 1].tolist()
    # for i in range(0, len(x)):
    #     x[i] = -x[i]
    #     y[i] = -4*y[i]
    Max = max(x)
    x0 = x.index(Max) 
    p_max = y[x0]
    h_max = x[x0]
    y_prime = y[x0+1:]
    x_prime = x[x0+1:]
    Min = min(y_prime)
    y0 = y_prime.index(Min) 
    h_r = x_prime[y0]
    third_data = 1+round(len(y_prime)/3)
    y_prime_third = y_prime[: third_data]
    x_prime_third = x_prime[: third_data]
    slope = np.polyfit(y_prime_third, x_prime_third, 1)
    dp_dh = slope[0]
    # estimate sink_in pile_up
    h_b=0
    if h_r/h_max < 0.83:
        h_c=h_max-(0.72*p_max/dp_dh+h_b)
    else:
        h_c=1.2*(h_max-p_max/dp_dh+h_b)
    A_c=24.56*(h_c**2)
    
    return p_max,A_c
def estimate_residual_stress(lvdt,loadcell,lvdt1,loadcell1,kapa):  
    # with_rs = Residual_Stress('n0.4\\3D-Q-n04-Case1.xlsx')
    # no_rs =Residual_Stress('n0.4\\3D-Q-n04-noRS.xlsx')
    # kapa=float(input('insert the stress ratio='))
    with_rs = Residual_Stress(lvdt,loadcell)
    no_rs =Residual_Stress(lvdt1,loadcell1)
    RS_Lee_2= (no_rs[0]-with_rs[0])*3/((1+kapa)*with_rs[1])
    RS_Lee_1= kapa*RS_Lee_2
    return RS_Lee_1,RS_Lee_2
