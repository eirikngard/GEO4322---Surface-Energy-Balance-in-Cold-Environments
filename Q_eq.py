# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 11:07:41 2020

@author: Eirik Nordgård
"""

import math 
import numpy as np

def Q_eq(T_surface, q, windspeed, saturation):
        
    #T_surface = 10    
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
