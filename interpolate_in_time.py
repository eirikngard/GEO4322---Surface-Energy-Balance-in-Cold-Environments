# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 10:38:42 2020

@author: Eirik Nordgård
"""
#Script for interpolation

import math 

def interpolate_in_time(time,variable):
    time = time*8;
    before = math.floor(time) + 1;
    fraction = time - (before-1);
    value = (1-fraction) * variable[before] + fraction*variable[before]
    return value.item() 
