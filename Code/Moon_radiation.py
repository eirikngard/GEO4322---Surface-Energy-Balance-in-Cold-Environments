# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 11:07:26 2020

@author: Eirik Nordgård
"""

''' Simple program to calcualte surface temperature of the Earth'''

###Imports###

import numpy as np
import scipy.io #Import to read .mat forcing file
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from interpolate_in_time import interpolate_in_time
from Q_h import Q_h
from Q_eq import Q_eq

###Parameters###

c_h = 2.2e6;#heat capacity of rock [J/m3K]
K = 3; #Thermal conductivity for rock [wm-1K-1]
d1 = 0.1; #thickness of surface block [m] 
d2 = 0.5; #thickness og second grid cell
bucket_depth = 0.1; #maximum depth of bucket for water storage
drainage_constant = 10 #mm/day subsurface runoff for saturation = 1
albedo = 0.2;

startTime = 0; #[days]
endTime = 2*365;
#timestep = (3/24)/100; #[days]
timestep = (3/24)/100; #[days] 
outputTimestep = 3/24; #envery 3h

###Constants###
 
sigma = 5.67e-8; #Stefan boltzmann constant [J/m2K4]
daySec = 24*60*60; # sec in a day
count=0; #counter 

###IC for t=0###

t = startTime; #time [sec]
T1 = 0; #initial surface temperature [C]
T2 = 0; #Initial temperature of second layer ground
water_level = bucket_depth/2; #half bucket 
E1 = c_h*d1*T1;#initial energy of the block [J/m2]
E2 = c_h*d2*T2;#initial energy of the second layer [J/m2]

###Storing values###

t=1;
time = np.arange(0,10000,timestep)
T1_result = []
T2_result = []
water_level_result = []
surface_runoff_result = []
subsurface_runoff_result = []
time_result = []

###Reading the .mat forcing file###

finse = scipy.io.loadmat('forcing_SEB_Finse.mat')
Tair = finse['Tair']
rainfall = finse['rainfall']
Sin = finse['Sin']
Lin = finse['Lin']
windspeed = finse['windspeed']
q = finse['q']

#%%
'''''''''''''''Main program'''''''''''''''''
#for t in startTime:timestep:endTime:
for t in time:
#for i in range(startTime,endTime,timestep):    
    #water balance - rainfall and subsurface runoff outflof,
    #only if the groud is not frozen
    if T1>=0 and T2>=0:
        water_in_rainfall = interpolate_in_time(t,rainfall)/1000/daySec;
        saturation = water_level/bucket_depth;
        water_out_subsurface_runoff = drainage_constant/1000/daySec*saturation;
    else: 
        water_out_subsurface_runoff = 0;
    
    #Incoming solar radiation
    S_in = interpolate_in_time(t,Sin); #from forcing data
    S_out = albedo*S_in;
    #F_sun = sigma*(T_sun)**4*(r_sun/(r_sun+d_earth_sun))**2; #W/m2
    #S_in = (1-albedo)*F_sun*np.cos(2*np.pi*t/P); #W/m2
    #S_in = np.max(S_in,0);
    
    #Outgoing thermal readiation
    L_in = interpolate_in_time(t,Lin);#from forcing data 
    L_out = sigma*(T1+273.15)**4; # W/m2
    
    #Ground heat flux
    F_cond = -K*(T1-T2)/((d1+d2)/2); #Fouriers law of heat conduction
    
    #Sensible Heat flux
    T_air = interpolate_in_time(t,Tair);#from forcing data
    wind_speed = interpolate_in_time(t,windspeed);
    F_sensibleHeat = Q_h(T_air,T1,wind_speed);
    
    #Latent Heat flux/evapotranspiration
    absolute_humidity = interpolate_in_time(t,q);
    [F_latentHeat, water_out_evapotranspiration] = Q_eq(T1,absolute_humidity,wind_speed,saturation);
    
    
    # Surface energy balance - next timestep
    E1 = E1+timestep*daySec*(S_in-S_out+L_in-L_out+F_cond-F_sensibleHeat-F_latentHeat) #SURFACE ENERGY BALANCE EQ!!!
    E2 = E2 + timestep*daySec*(-F_cond)
    T1 = E1/(c_h*d1) #convert energy content to temperature, using heat capacity 
    T2 = E1/(c_h*d2)
    
    #Water Balance
    if (T1-T2).any()>=0:#T1>=0 and T2>=0:
        water_level = water_level + timestep*daySec*(water_in_rainfall-water_out_evapotranspiration-water_out_subsurface_runoff);# WATER BALANCE EQUATION
        surface_runoff = max(0,water_level-bucket_depth);#if water level is higher than bucket 
        water_level = min(water_level,bucket_depth);#remove water when bucket tops over
    else:
        surface_run_off = 0;
    
    #Resulting values
    if count % (outputTimestep/timestep)==0:
        
        T1_result.append(T1)
        T2_result.append(T2)
        water_level_result.append(water_level)
        surface_runoff_result.append(surface_runoff)
        subsurface_runoff_result.append(water_out_subsurface_runoff)
        #t_result.append(t)

    count = count+1
#%%

fig, ax = plt.subplots()
plt.plot(T1_result, color='red', label = "Layer 1")
plt.plot(T2_result, color='blue', label = "Layer2")
ax.set_ylabel("Temperature [\u2103]", fontsize = 15)
ax.set_xlabel("Time [h]", fontsize = 15)
plt.legend()
ax.set_title("Surface temperature of Earth", fontsize  = 20)
plt.show()

#SHOULD BE PHASE-SHIFTED. IS NOT, WHY???
#%%
fig, ax = plt.subplots(3)
ax[0].plot(water_level_result,color= 'red')
ax[0].legend(["Water Level"])
ax[1].plot(surface_runoff_result,color= 'blue')
ax[1].legend(["Surface Runoff"])
ax[2].plot(subsurface_runoff_result,color= 'green')
ax[2].legend(["SubSurface Runoff"])
plt.show()

#just a small change 
