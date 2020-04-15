%calculates the surface temperature of the Earth using radiation, ground
%heat flux and sensible heat flux
% bucket filled with snow, putting water 
%parameters
albedo = 0.6; %albedo of snow surface

startTime = 0; % [days]
endTime = 2.*365;
timestep = 3/24 ./100; %[days]
outputTimestep = 3/24; %every 3h

%constants
sigma = 5.67e-8; %Stefan-Boltzmann constant [J/m2 K4]
daySec = 24 .* 60 .*60; %number of seconds in one day [sec]
L_f = 334 .* 1e6; %latent heat of freezing/melting of water [J/m3]
%takes more energy to evaporate water than to melt ice

%initialization for t = 0
t = startTime; %time [sec]
SWE = 0; %[m] snow water equivalent -> how full is the bucket?

%store values
t_store = t;
SWE_store = SWE;

%load('forcing_SEB_Suossjavri.mat')  %Change between Finse and Suossjavri/Finnmark by commenting out the forcing file
load('forcing_SEB_Finse.mat')

%main program

count=0;

for t = startTime:timestep:endTime
    
    %snowfall
    snow_in = interpolate_in_time(t, snowfall) ./1000 ./ daySec;  %from forcing data, convert mm/day to m/sec
    
    %incoming and ougoing shortwave (solar) radiation
    S_in = interpolate_in_time(t, Sin);  %from forcing data
    S_out = albedo .* S_in;
    
    %incoming and ougoing (thermal) radiation
    L_in = interpolate_in_time(t, Lin);  %from forcing data
    L_out = sigma .* (0+273.15).^4; %from Stefan-Botzman law [J/ sec m2] - melting ice has 0 degreeC
    % melt turn under assumption that temp=0, snow is melting
    
    %sensible heat flux
    T_air = interpolate_in_time(t, Tair);  %from forcing data
    wind_speed = interpolate_in_time(t, windspeed);  %from forcing data
    F_sensibleHeat = Q_h(T_air, 0, wind_speed);
    
    %latent heat flux/evapostranspiration
    absolute_humidity = interpolate_in_time(t, q);  %from forcing data
    F_latentHeat = Q_eq(0, absolute_humidity, wind_speed);
    
    %time integration - advance to next timestep
    
    %surface energy balance / mass balance
    melt_energy = S_in - S_out + L_in - L_out - F_sensibleHeat - F_latentHeat; %  SURFACE ENERGY BALANCE EQUATION!!!! [J/(m2 sec)]
    snow_melt_out = melt_energy ./ L_f; %[m/sec], convert energy to mass
    snow_melt_out = max(snow_melt_out, 0); %only of melt occurs!!
    
    %snow mass balance
    SWE = SWE + timestep .* daySec .* (snow_in - snow_melt_out);  % SNOW MASS BALANCE EQUATION
    SWE = max(SWE,0);
    
    %store values
    if mod(count,outputTimestep./timestep)==0
        SWE_store = [SWE_store ; SWE];
        t_store = [t_store; t];
    end
    count=count+1;

end




