# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 08:58:04 2020

@author: Eirik N
"""



import numpy as np
import scipy.io #Import to read .mat forcing file
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time

from surface_balance_functions import interpolate_in_time, Q_h, Q_eq

plt.close('all')
#then = time.time()#timestamp of script start mark
###Parameters###
new_water = []
new_runoff = []
new_subsurface = []
bucket_depth = np.arange(0.5,1,0.1)

for bucket in bucket_depth:
    
    c_h = 2.2e6;#heat capacity of rock [J/m3K] 
    K = 3; #Thermal conductivity for rock [wm-1K-1]
    d1 = 0.1; #thickness of surface block [m] 
    d2 = 0.5; #thickness og second grid cell
    #bucket_depth = 1; #maximum depth of bucket for water storage
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
    water_level = bucket/2; #half bucket 
    E1 = c_h*d1*T1;#initial energy of the block [J/m2]
    E2 = c_h*d2*T2;#initial energy of the second layer [J/m2]
    
    ###Storing values###
    
    t=1;
    time = np.arange(startTime,endTime,timestep)#0,730,timestep)#startTime,endTime,timestep
    T1_result = []
    T2_result = []
    time_result = []
    water_level_result = []
    water_level_result.append(water_level)
    surface_runoff_result = []
    subsurface_runoff_result = []
    
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
    
    #%%
    '''''''''''''''Main program'''''''''''''''''
    """
    #use this insted of lists
    tup1=()
    for i in range(1,10,2):
       tup1+= (i,)
    print tup1
    """    
    
    for t in time: 
        water_level = bucket/2; #half bucket 
        
        if T1>=0 and T2>=0:
            water_in_rainfall = interpolate_in_time(t,rainfall)/1000/daySec;
            saturation = water_level/bucket;#is this correct? water_in_rainfall insted?
            water_out_subsurface_runoff = drainage_constant/1000/daySec*saturation;
        else: 
            water_out_subsurface_runoff = 0;
        
            #Incoming solar radiation
        S_in = interpolate_in_time(t,Sin); #from forcing data
        S_out = albedo*S_in;
        
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
        #line above, coulpling betwenn water and energy cycle.
        
        # Surface energy balance - next timestep
        E1 = E1+timestep*daySec*(S_in-S_out+L_in-L_out+F_cond-F_sensibleHeat-F_latentHeat) #SURFACE ENERGY BALANCE EQ!!!
        E2 = E2 + timestep*daySec*(-F_cond)
        T1 = E1/(c_h*d1) #convert energy content to temperature, using heat capacity 
        T2 = E2/(c_h*d2)
      
        #Water Balance
        if T1>=0 and T2>=0:#if (T1-T2).any()>=0:#T1>=0 and T2>=0:
            water_level = water_level + timestep*daySec*(water_in_rainfall-water_out_evapotranspiration-water_out_subsurface_runoff);# WATER BALANCE EQUATION
            surface_runoff = max(0,water_level-bucket);#if water level is higher than bucket 
            water_level = min(water_level,bucket);#remove water when bucket tops over
        else:
            surface_runoff = 0;
        
        #Resulting values
        if count % (outputTimestep/timestep)==0: #return remainder after division 
            
            water_level_result.append(water_level)
            surface_runoff_result.append(surface_runoff/timestep*1000)#mm/day
            subsurface_runoff_result.append(water_out_subsurface_runoff*daySec*1000)#mm/day
            #try to avoid this append procedure, sloving down the code alot?
            #water_level_result += (water_level,)
            #surface_runoff_result += (surface_runoff/timestep*1000,)
            #subsurface_runoff_result += (water_out_subsurface_runoff*daySec*1000,)
            #tup1+= (i,)
            #ADD SENSIBLE AND LATENT HEAT HERE SO YOU CAN PLOt THEM
    
        count = count+1
    
    new_water.append(water_level_result)
    #new_runoff.append(surface_runoff_result)
    #new_subsurface.append(subsurface_runoff_result)
    #new_water += (water_level_result,)
    #new_runoff += (surface_runoff_result,)
    #new_subsurface += (subsurface_runoff_result,)

#%%

fig, ax = plt.subplots(2,2)
ax = ax.flatten()
ax[0].plot(new_water[0])
ax[1].plot(new_water[1])
ax[2].plot(new_water[2])
ax[3].plot(new_water[3])
plt.show()
#%%
plt.figure()
plt.plot(subsurface_runoff_result)
plt.show()
#%% Plotting som of the Finse data

relHumidity = finse['relHumidity']

fig, ax =plt.subplots(2,2)
ax=ax.flatten()
ax[0].plot(rainfall), ax[0].legend(["Rainfall"],prop={'size': 20})
ax[1].plot(surface_runoff_result, color='k'), ax[1].legend(["Surface Runoff"],prop={'size': 20})
#ax[1].set_xlim([0,8000])
ax[2].plot(subsurface_runoff_result,color='brown'), ax[2].legend(["SubSur Runoff"],prop={'size': 20})
ax[3].plot(water_level_result, color='green'), ax[3].legend(["Water Level"],prop={'size': 20})
plt.savefig(figdir + 'runoff_metrics.pdf')
plt.show()

#%%
fig, ax = plt.subplots(3)
ax[0].plot(water_level_result,color= 'red')
ax[0].legend(["Water Level"])
ax[1].plot(surface_runoff_result,color= 'blue')
ax[1].legend(["Surface Runoff"])
ax[2].plot(subsurface_runoff_result,color= 'green')
ax[2].legend(["SubSurface Runoff"])
plt.savefig(figdir + "waterbalance.pdf")
plt.show()

#Surface_runoff has wrong units! should be in mm/day (so in range 0-10 mm/day!)

#%%
#Plotting water level with varying bucket depth 
fig, ax = plt.subplots(3)
ax[0].plot(new_water[0],'r', label='0.5'), ax[0].legend()
ax[1].plot(new_water[2],'k', label='0.7'), ax[1].legend()
ax[2].plot(new_water[4],'k', label='0.9'), ax[2].legend()
fig.suptitle('Bucket_depth')
plt.show()
#%%
plt.figure()
plt.plot(new_water[0]),plt.plot(new_water[1])
plt.show()






