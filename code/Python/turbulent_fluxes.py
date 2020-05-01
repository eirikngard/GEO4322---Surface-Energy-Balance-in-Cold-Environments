# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 08:37:04 2020

@author: Eirik Nordgård
"""
#Script to solve exercises on turbulent fluxes in GEO4432.
#Mostly plotting of data 
                         
#%%           
'''
Importig files and creating variables
'''                          
import pandas as pd
import glob
import os

os.chdir("C:/Users/Eirik N/Documents/UiO/GEO4432")
df = pd.read_csv('2018-07-15T093000.csv')

u = df['u_m/s']
v = df['v_m/s']
w = df['w_m/s']
T = df['T_degC']
co2 = df['CO2_ppm']
h2o = df['H2O_ppt']

#%%
'''
Simple plot for overview
'''
import matplotlib.pyplot as plt

fig, ax = plt.subplots(3)
ax[0].plot(u), ax[0].legend("u")
ax[1].plot(v), ax[1].legend("v")
ax[2].plot(w), ax[2].legend("w")
plt.show()

fig, ax = plt.subplots(3)
ax[0].scatter(w,T,s=1), ax[0].legend("wTemp")
ax[1].scatter(w,h2o,s=1), ax[1].legend("wh2o")
ax[2].scatter(w,co2,s=1), ax[2].legend("wco2")
ax.legend()
plt.show()
#%%
'''
Statistics for variables 
'''
#When the statistical properties of a process are independent of time
#the process is stationary. 

path = r"C:\Users\Eirik N\Documents\UiO\GEO4432\eddy_raw_data"
all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent

mu, su, mv, sv, mw, sw = [], [], [], [], [], []
mt, st, mh2, sh2, mco, sco = [], [], [], [], [], []

for this_file in all_files:
    this_df=pd.read_csv(this_file)
    mu.append(this_df['u_m/s'].mean())
    su.append(this_df['u_m/s'].std())
    mv.append(this_df['v_m/s'].mean())
    sv.append(this_df['v_m/s'].std())
    mw.append(this_df['w_m/s'].mean())
    sw.append(this_df['w_m/s'].std())
    mt.append(this_df['T_degC'].mean())
    st.append(this_df['T_degC'].std())
    mh2.append(this_df['CO2_ppm'].mean())
    sh2.append(this_df['CO2_ppm'].std())
    mco.append(this_df['H2O_ppt'].mean())
    sco.append(this_df['H2O_ppt'].std())

fig, ax = plt.subplots(6)
ax[0].plot(mu),ax[0].plot(su), ax[0].legend("u")
ax[1].plot(mv),ax[1].plot(su), ax[1].legend("v")
ax[2].plot(mw),ax[2].plot(su), ax[2].legend("w")
ax[3].plot(mt),ax[3].plot(st), ax[3].legend("T")
ax[4].plot(mh2),ax[4].plot(sh2), ax[4].legend("H2O")
ax[5].plot(mco),ax[5].plot(sco), ax[5].legend("CO2")
plt.show()

#More or less stationarity from 
#file 170 and out. STD ~ 0. 
#%%
'''
Reynolds Decomposition
'''
#u = u_mean + u_fluctuation 
#u_fluc = u-u_mean

fu, fv, fw, ft, fh2, fco = [], [], [], [], [], []
mean_u = this_df['u_m/s'].mean()
mean_v = this_df['v_m/s'].mean()
mean_w = this_df['w_m/s'].mean()
mean_t = this_df['T_degC'].mean()
mean_h2 = this_df['H2O_ppt'].mean()
mean_co = this_df['CO2_ppm'].mean()
for this_file in all_files:
    this_df=pd.read_csv(this_file)
    fu.append((this_df['u_m/s']-mean_u).mean())
    fv.append((this_df['v_m/s']-mean_v).mean())
    fw.append((this_df['w_m/s']-mean_w).mean())
    ft.append((this_df['T_degC']-mean_t).mean())
    fh2.append((this_df['H2O_ppt']-mean_h2).mean())
    fco.append((this_df['CO2_ppm']-mean_co).mean())
    
fig, ax = plt.subplots(6)
ax[0].plot(fu), ax[0].legend("u")
ax[1].plot(fv), ax[1].legend("v")
ax[2].plot(fw), ax[2].legend("w")
ax[3].plot(ft), ax[3].legend("T")
ax[4].plot(fh2), ax[4].legend("H2O")
ax[5].plot(fco), ax[5].legend("CO2")
plt.show()
#%%
'''
Calcualte turbulent fluxes, H, LE and NEE
'''
import math 
import numpy as np

def LE(temp, wind):
    '''Calculate latent heat'''    
    p = 1005*100; kappa=0.4; z =  2; z0 = 1e-2;
    temp=temp+273.15; saturation = 1; q = 0.0025; #kg/kg
    rho_air = p/(287.058*temp); #air density [kg m^(-3)]
    L_w = 1e3*(2500.8 - 2.36*(temp-273.15));  #latent heat of evaporation of water [J/kg]    
    satPresWater = 0.622* 6.112* 100*np.exp(17.62*(temp-273.15)/(243.12-273.15+temp)); #Magnus equation, e.g. https://en.wikipedia.org/wiki/Vapour_pressure_of_water    
    Q_e_pot = -rho_air*L_w*kappa*wind*kappa/math.log(z/z0)*(q-satPresWater/p)/math.log(z/z0);    
    LE = saturation*Q_e_pot;    
    return LE

def H(temp, wind):
    '''Calculate sensible heat'''
    z = 2; #height of air temperature 
    z0 = 1e-2; #roughness length
    p = 1005*100; temp = temp+273.15; T1 = 293.15; #set to const
    rho = p/(287.058*temp); cp = 1005; kappa = 0.4;
    H = (-rho*cp*kappa*wind*kappa/math.log(z/z0))*((temp-T1)/math.log(z/z0));
    return H
#formulas page 127 in "physical hydrology" (Dingman)
#%%
path = r'C:\Users\Eirik N\Documents\UiO\GEO4432\eddy_raw_data'                     # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent

df_from_each_file = (pd.read_csv(f) for f in all_files)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)
# doesn't create a list, nor does it append to one

w1 = concatenated_df['w_m/s']
T1 = concatenated_df['T_degC']
latent_flux = LE(T1,w1)
sensible_flux = H(T1,w1)
#%%
plt.figure()
plt.ylim(-200,200)
plt.plot(sensible_flux)
plt.show()
