# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 10:44:19 2020

@author: Eirik Nordgård
"""

import math 
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
    
    #5=windspeed
    return Q_h