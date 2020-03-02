clear
close all


% first step is to import the data from the file 'AWSdata.xls'. there are
% several ways of doing this, and I simply used the xlsread function. this
% is aware of the actual convention for decimal separator and you do not have to care about comma or point... it easily is re-used...
% 
[data,name]=xlsread('AWSdata.xls');

% give the variables nice names
decday = data(:,2);
temperature = data(:,4);
humidity = data(:,5);
windspeed = data(:,6);
globalrad = data(:,7);
reflected = data(:,8);
longwave_in = data(:,9);
longwave_out = data(:,10);
precip = data(:,11);


% we make a date variable using matlab date-format
date=datenum(data(1,1),1,0)+decday;
% make plots
figure
plot(date,globalrad)
datetick
hold all
plot(date,reflected)
title('shortwave')

% calculate longwave balance
longwavebalance=longwave_in-longwave_out;
% make plot
figure
plot(date,longwave_in)
hold all
plot(date,longwave_out)
plot(date,longwavebalance)
title('longwave')
datetick

% net radiation
netradiationbalance=globalrad-reflected+longwavebalance;
% plot it
figure
plot(date,netradiationbalance)
datetick
title('net radiation')

% define the constants
cp=1005;A=2.8885e-8;P=85000;T0=0;

% calculate the turbulent fluxes
sens= cp*A*P*windspeed.*(temperature-T0);

Lv=2430000;
SaturationvapourpressurePa = 610.78.*exp((17.08085.*temperature)./(234.15+temperature));
vapourpressure = humidity/100.*SaturationvapourpressurePa;

latent=0.623*Lv*A*windspeed.*(vapourpressure-SaturationvapourpressurePa);

% rain heat flux
cw=4200;
rhow=1000;
Rainenergy=rhow*cw*(temperature-T0).*precip/3600/1000; % conversion from mm/h to m/s 

% plot it
figure
plot(date,Rainenergy)
datetick
title('rain energy (W m-2)')

% energy available for melt
Meltenergy=netradiationbalance+sens+latent+Rainenergy;

% melt rate in mm/h
meltmmh=Meltenergy/334000/rhow*3600*1000;   % conversion m/s to mm/h
% negative melt is not plausible and set to zero. in those instances
% cooling would occur
meltmmh(meltmmh<0)=0;

% make plot
figure
plot(date,Meltenergy)
datetick
title('melt energy')

figure
plot(date,meltmmh)
datetick
title('meltrate mm/h')

% the total amount of melt during this period
totalmelt = sum(meltmmh);

disp(['total melt = ',num2str(totalmelt),' mm'])