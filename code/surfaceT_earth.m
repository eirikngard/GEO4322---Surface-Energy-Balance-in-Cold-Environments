%calculates the surface temperature of the Earth using radiation, ground
%heat flux and sensible heat flux

    %parameters
result_water = []
result_surface = []
result_subsurface = []
for bucket_depth = 0.5:0.1:1.0;
    %disp(albedo) %added just to see if it completes each iteration
    c_h = 2.2e6; % heat capacity of rock [J/m3K]
    K = 3; % thermal conductivity of rock [W/m K]
    d_1 = 0.1; % thickness of surface grid cell [m]
    d_2 = 0.5; %thickness of second grid cell [m]
    albedo = 0.2; %albedo of surface
    %bucket_depth = 0.5; % maximum depth of baucket for storage of water [m]
    drainage_constant = 1; %mm/day subsurface runoff for saturation = 1

    startTime = 0; % [days]
    endTime = 2.*365;
    timestep = 3/24 ./100; %[days]
    outputTimestep = 3/24; %every 3h

    %constants
    sigma = 5.67e-8; %Stefan-Boltzmann constant [J/m2 K4]
    daySec = 24 .* 60 .*60; %number of seconds in one day [sec]

    %initialization for t = 0
    t = startTime; %time [sec]
    T_1 = 0; %initial surface grid cell temperature [degree C];
    T_2 = 0; %initial temperature of second grid cell [degree C];
    water_level = bucket_depth ./ 2; %half full bucket
    E_1 = c_h .* d_1 .* T_1; % initial energy of the block [J/m2]
    E_2 = c_h .* d_2 .* T_2; % initial energy of the block [J/m2]


    %store values
    T_1_store = T_1;  %surface temperature stored here!
    T_2_store = T_2;
    water_level_store = water_level;
    surface_runoff_store = 0;
    subsurface_runoff_store = 0;
    t_store = t;

    %load('forcing_SEB_Suossjavri.mat')  %Change between Finse and Suossjavri/Finnmark by commenting out the forcing file
    load('forcing_SEB_Finse.mat')

    %main program

    count=0;
    %new_water=0;
    %new_surface_runoff=0;
    %new_subsurface_runoff=0;
    %for bucket_dept = 0:0.1:1

    for t = startTime:timestep:endTime

        %water balance - rainfall and subsurface outflow, only if ground is not
        %frozen
        if T_1>=0 && T_2>= 0  %only if the ground is unfrozen
            water_in_rainfall = interpolate_in_time(t, rainfall) ./1000 ./ daySec;  %from forcing data, convert mm/day to m/sec
            saturation =  water_level ./ bucket_depth;
            water_out_subsurface_runoff = drainage_constant ./1000 ./ daySec .* saturation;
        else
            water_out_subsurface_runoff = 0;
        end

        %incoming and ougoing shortwave (solar) radiation
        S_in = interpolate_in_time(t, Sin);  %from forcing data
        S_out = albedo .* S_in;

        %incoming and ougoing (thermal) radiation
        L_in = interpolate_in_time(t, Lin);  %from forcing data
        L_out = sigma .* (T_1+273.15).^4; %from Stefan-Botzman law [J/ sec m2]

        %ground heat flux
        F_cond = -K.*(T_1 - T_2)./( (d_1+d_2)./2 ); %Fourier's Law of heat conduction

        %sensible heat flux
        T_air = interpolate_in_time(t, Tair);  %from forcing data
        wind_speed = interpolate_in_time(t, windspeed);  %from forcing data
        F_sensibleHeat = Q_h(T_air, T_1, wind_speed);

        %latent heat flux/evapostranspiration
        absolute_humidity = interpolate_in_time(t, q);  %from forcing data
        [F_latentHeat, water_out_evapotranspiration] = Q_eq(T_1, absolute_humidity, wind_speed, saturation);

        %time integration - advance to next timestep

        %surface energy balance 
        E_1 = E_1 + timestep .* daySec .* (S_in - S_out + L_in - L_out - F_sensibleHeat - F_latentHeat + F_cond); %  SURFACE ENERGY BALANCE EQUATION!!!!
        E_2 = E_2 + timestep .* daySec .* (-F_cond); 
        T_1 = E_1 ./ (c_h .* d_1); %convert emegy contemt to temeprature, using the heat capacity
        T_2 = E_2 ./ (c_h .* d_2);

        %water balance
        if T_1>=0 && T_2>= 0  %only if the ground is unfrozen
            water_level = water_level + timestep .* daySec .* (water_in_rainfall - water_out_evapotranspiration - water_out_subsurface_runoff);  % WATER BALANCE EQUATION
            surface_run_off = max(0, water_level - bucket_depth); %if water level is higher than the bucket
            water_level = min(water_level, bucket_depth); %remove water when bucket tops over
        else
            surface_run_off = 0;
        end

        %store values
        if mod(count,outputTimestep./timestep)==0
            T_1_store = [T_1_store ; T_1];
            T_2_store = [T_2_store ; T_2];
            water_level_store = [water_level_store; water_level];
            surface_runoff_store = [surface_runoff_store ; surface_run_off ./timestep .*1000];  %in mm/day!!!!
            subsurface_runoff_store = [subsurface_runoff_store ; water_out_subsurface_runoff .* daySec .*1000]; % in mm/day!!!!
            t_store = [t_store; t];
        end
        count=count+1;
    end
        result_water=[result_water water_level_store];
        result_surface = [result_surface surface_runoff_store]
        result_subsurface = [result_subsurface subsurface_runoff_store]
end

%%
figurepath = 'C:/Users/Eirik N/Documents/UiO/GEO4432/figures'

figure
hold all
plot(result_water(:,1)), plot(result_water(:,2)), plot(result_water(:,3))
plot(result_water(:,4)), plot(result_water(:,5))
title('Water Level with varying bucket depth')
xlabel('Time'), ylabel('Water level')
lgd = legend('0.5','0.6','0.7','0.8','0.9','Location','southeast')
title(lgd,'Bucket Depth [m]')
saveas(gcf,[figurepath,'/bucket_depth.pdf']);
%%
figure
hold all
plot(result_surface(:,1))
plot(result_surface(:,2))
plot(result_surface(:,3))
plot(result_surface(:,4))
plot(result_surface(:,5))
%%
figure
hold all
plot(result_subsurface(:,1))
plot(result_subsurface(:,2))
plot(result_subsurface(:,3))
plot(result_subsurface(:,4))
plot(result_subsurface(:,5))

