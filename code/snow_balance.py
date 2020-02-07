# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 13:36:59 2020

@author: Eirik Nordgård
"""
#Same as the other, only with snow

###Imports###

import numpy as np
import scipy.io #Import to read .mat forcing file
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from surface_balance_functions import interpolate_in_time, Q_h, Q_eq

###Parameters###

c_h = 2.2e6;#heat capacity of rock [J/m3K] 
K = 3; #Thermal conductivity for rock [wm-1K-1]
d1 = 0.1; #thickness of surface block [m] 
d2 = 0.5; #thickness og second grid cell
bucket_depth = 0.5; #maximum depth of bucket for water storage
drainage_constant = 10 #mm/day subsurface runoff for saturation = 1
albedo = 0.6; #0.6 for snow

SWE = 0; #snow-water-equivavelt [m] (bucket depth, starts empty in summer)

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
#T2 = 0; #Initial temperature of second layer ground
water_level = bucket_depth/2; #half bucket 
E1 = c_h*d1*T1;#initial energy of the block [J/m2]
E2 = c_h*d2*T2;#initial energy of the second layer [J/m2]

###Storing values###
SWE_result = []

t=1;
time = np.arange(0,730,timestep)#startTime,endTime,timestep
T1_result = []
#T2_result = []
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
snowfall = finse['snowfall']

#%%
'''''''''''''''Main program'''''''''''''''''

for t in time:

    
    snow_in = interpolate_in_time(t,snowfall)/1000/daySec; #[mm/day]

    
    #Incoming solar radiation
    S_in = interpolate_in_time(t,Sin); #from forcing data
    S_out = albedo*S_in;
    
    #Outgoing thermal readiation
    L_in = interpolate_in_time(t,Lin);#from forcing data 
    L_out = sigma*(0+273.15)**4; # W/m2, melting snow is 0 celcius
    
    #Ground heat flux
    #F_cond = -K*(T1-T2)/((d1+d2)/2); #Fouriers law of heat conduction
    #removing this because we only concider one layer of snow
    
    #Sensible Heat flux
    T_air = interpolate_in_time(t,Tair);#from forcing data
    wind_speed = interpolate_in_time(t,windspeed);
    F_sensibleHeat = Q_h(T_air,0,wind_speed); #surface temperature T1 is 0
    
    #Latent Heat flux/evapotranspiration
    absolute_humidity = interpolate_in_time(t,q);
    [F_latentHeat, water_out_evapotranspiration] = Q_eq(0,absolute_humidity,wind_speed,saturation);
    #line above, water is in reality leaving the system here, not taken into account
    #line above, coulpling betwenn water and energy cycle.
    
    # Surface energy balance - next timestep
    melt_energy = (S_in-S_out+L_in-L_out-F_sensibleHeat-F_latentHeat);#[J/m2S] #SURFACE ENERGY BALANCE EQ!!!

    #Snow mass Balance

    SWE = SWE + timestep*daySec*(snow_in-);# WATER BALANCE EQUATION


    #Resulting values
    if count % (outputTimestep/timestep)==0:
        
        T1_result.append(T1)
        T2_result.append(T2)
        water_level_result.append(water_level)
        surface_runoff_result.append(surface_runoff)#mm/day
        subsurface_runoff_result.append(water_out_subsurface_runoff)#mm/day
        
        #ADD SENSIBLE AND LATENT HEAT HERE SO YOU CAN PLOt THEM

    count = count+1
#%%
'''''''''Plotting ome figures'''''''''
figdir = "../figures/"

fig, ax = plt.subplots()
plt.plot(T1_result, color='red', label = "Surface")
plt.plot(T2_result, color='blue', label = "Layer below")
ax.set_ylabel("Temperature [\u2103]", fontsize = 15)
ax.set_xlabel("Time [h]", fontsize = 15)
plt.legend()
ax.set_title("Surface temperature of Earth", fontsize  = 20)
plt.savefig(figdir + "snow_surftemp.pdf")
plt.show()

#SHOULD BE PHASE-SHIFTED. IS NOT, WHY???
#%% Random subplots

fig, ax = plt.subplots(3)
ax[0].plot(water_level_result,color= 'red')
ax[0].legend(["Water Level"])
ax[1].plot(surface_runoff_result,color= 'blue')
ax[1].legend(["Surface Runoff"])
ax[2].plot(subsurface_runoff_result,color= 'green')
ax[2].legend(["SubSurface Runoff"])
plt.savefig(figdir + "snow_waterbalance.pdf")
plt.show()

#from this figure, water_level_result and SubSurface is almost identical
#%% Comparing true and calculted temperature 

fig = plt.figure()
plt.title("Comparison of true and calculated temp")
plt.plot(Tair,color='r', label="Tair_true", alpha=0.7)
plt.plot(T1_result,label="Temp_calc",alpha=0.7)
plt.xlim([0,6000])
plt.legend()
plt.savefig(figdir + 'true_calc_compar.pdf')
plt.show()

#%% 
fig, ax =plt.subplots(3)
ax[0].plot(windspeed), ax[0].legend(["Windspeed"])
ax[1].plot(Tair), ax[1].legend(["Tair_true"])
ax[1].set_xlim([0,8000])
ax[2].plot(T1_result), ax[2].legend(["Temp_calc"])
plt.show()

#%% Plotting som of the Finse data

relHumidity = finse['relHumidity']

fig, ax =plt.subplots(2,2)
ax=ax.flatten()
ax[0].plot(rainfall), ax[0].legend(["Rainfall"])
ax[1].plot(Tair), ax[1].legend(["Tair_true"])
ax[1].set_xlim([0,8000])
ax[2].plot(q), ax[2].legend(["Humidity"])
ax[3].plot(relHumidity), ax[3].legend(["Relative Humidity"])
plt.show()

#%% Want to plot the coherence/correlation 
from sklearn.metrics import r2_score

r2 = r2_score(Tair[0:5840],T1_result)
print(r2)
#%%
#Surface_runoff has wrong units! should be in mm/day (so in range 0-10 mm/day!)
fig, ax = plt.subplots(2)
ax[0].plot(surface_runoff_result)
ax[1].plot(subsurface_runoff_result)
plt.show()

