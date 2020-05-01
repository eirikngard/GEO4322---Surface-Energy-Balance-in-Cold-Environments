# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 09:02:06 2020

@author: Eirik N
"""

import numpy as np
import scipy.io #Import to read .mat forcing file
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random
import time

from surface_balance_functions import interpolate_in_time, Q_h, Q_eq

plt.close('all')

###Parameters###

c_h = 2.2e6;#heat capacity of rock [J/m3K] 
K = 3; #Thermal conductivity for rock [wm-1K-1]
d1 = 0.1; #thickness of surface block [m] 
d2 = 0.5; #thickness og second grid cell

drainage_constant = 1 #mm/day subsurface runoff for saturation = 1
albedo = 0.2; #0.6 for snow

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
#water_level = bucket_depth/2; #half bucket 
E1 = c_h*d1*T1;#initial energy of the block [J/m2]
E2 = c_h*d2*T2;#initial energy of the second layer [J/m2]

###Storing values###

t=1;
timee = np.arange(startTime,endTime,timestep)#0,730,timestep)#startTime,endTime,timestep
T1_result = []
T2_result = []


time_result = []

figdir = "../figures/"
surface_runoff=0

###Reading the .mat forcing file###

finse = scipy.io.loadmat('forcing_SEB_Finse.mat')
Tair = finse['Tair']
rainfall = finse['rainfall']
Sin = finse['Sin']
Lin = finse['Lin']
windspeed = finse['windspeed']
q = finse['q']

#bucket_depth = 1; #maximum depth of bucket for water storage
bucket_depth = np.arange(0.1,0.5,0.1)

#%%
'''''''''''''''Main program'''''''''''''''''
then = time.time()#timestamp of script start mark

new_water = []
new_surface = []
new_subsurface = []
for t in timee:
    water_level_result = []
    surface_runoff_result = []
    subsurface_runoff_result = []

    for bucket in bucket_depth:
        
        water_level = bucket/2; #half bucket 

        water_in_rainfall = interpolate_in_time(t,rainfall)/1000/daySec;
        saturation = water_level/bucket;#is this correct? water_in_rainfall insted?
        water_out_subsurface_runoff = drainage_constant/1000/daySec*saturation;
       
        wind_speed = interpolate_in_time(t,windspeed);
     
        absolute_humidity = interpolate_in_time(t,q);
        [F_latentHeat, water_out_evapotranspiration] = Q_eq(T1,absolute_humidity,wind_speed,saturation);
       
        water_level = water_level + timestep*daySec*(water_in_rainfall-water_out_evapotranspiration-water_out_subsurface_runoff);# WATER BALANCE EQUATION
        surface_runoff = max(0,water_level-bucket);#if water level is higher than bucket 
        water_level = min(water_level,bucket);#remove water when bucket tops over
        
        
        #Resulting values
        if count % (outputTimestep/timestep)==0: #return remainder after division 
            
            water_level_result.append([water_level])
            surface_runoff_result.append([surface_runoff/timestep*1000])#mm/day
            subsurface_runoff_result.append([water_out_subsurface_runoff*daySec*1000])#mm/day
    
        count = count+1
    new_water.append(water_level_result)
    new_surface.append(surface_runoff_result)
    new_subsurface.append(subsurface_runoff_result)
now = time.time()
print("Runtime:", (now-then)/60, "minutes")
#%%
import numpy as np
import matplotlib.pyplot as plt
test1 = np.arange(1,10,1)
test2 = np.arange(1,5,1)

a = 1

list1 = []
for tes in test1:
    list11 = []
    for tess in test2:
        list11.append(tess)
    list1.append(list11)

plt.figure()
plt.plot(list1[2])
plt.show()
#%%
result_array = np.array([])

for line in data_array:
    result = do_stuff(line)
    result_array = np.append(result_array, result)