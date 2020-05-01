# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 15:32:41 2020

@author: Eirik Nordgård
"""
'''Script containing all functions used in the surface-balance script'''

import math 
import numpy as np


#script to calculate Q_h

def Q_h(Tair, T1, windspeed):
    #q = specific humidity [kg/kg]
    
    z = 2; #height of air temperature 
    z0 = 1e-2; #roughness length
    p = 1005*100;
    Tair = Tair+273.15;#Tair+
    T1 = T1+273.15;#T1 +
    rho = p/(287.058*Tair); #air density [kg/m3]
    cp = 1005; #heat capacity of air
    kappa = 0.4;
    Q_h = (-rho*cp*kappa*5*kappa/math.log(z/z0))*((Tair-T1)/math.log(z/z0));
    
    return Q_h

def Q_eq(T_surface, q, windspeed, saturation):
            
    p = 1005*100;
    kappa=0.4;
    z =  2; 
    z0 = 1e-2;
    T_surface=T_surface+273.15;
    
    rho_air = p/(287.058*T_surface); #air density [kg m^(-3)]
    rho_water = 1000; #water density [kg m^(-3)]
    L_w = 1e3*(2500.8 - 2.36*(T_surface-273.15));  #latent heat of evaporation of water [J/kg]
    satPresWater = 0.622* 6.112* 100*np.exp(17.62*(T_surface-273.15)/(243.12-273.15+T_surface)); #Magnus equation, e.g. https://en.wikipedia.org/wiki/Vapour_pressure_of_water
    Q_e_pot = -rho_air*L_w*kappa*windspeed*kappa/math.log(z/z0)*(q-satPresWater/p)/math.log(z/z0);
    Q_e = saturation*Q_e_pot;
    water_out_evapotranspiration = Q_e/(L_w*rho_water);
    
    return Q_e, water_out_evapotranspiration

def interpolate_in_time(time,variable):
    time = time*8;
    before = math.floor(time) + 1;
    fraction = time - (before-1);
    value = (1-fraction) * variable[before] + fraction*variable[before]
    
    return value.item() 

