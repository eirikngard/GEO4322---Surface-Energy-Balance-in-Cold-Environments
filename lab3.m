%% SNOWLAB 3 - 

clear all
close all

load('meteoFinse20162018_AromeNorway_apr2018.mat')
load('FinseSWEpdf.mat')

idx=find(time>=datenum(2016,5,1)&time<datenum(2016,10,1));
%python idx = 13873:17544
alpha = 0.7;
TS = 273.15;
%neglect precip and conducrtive heat 
%%
%make new variables 
time2 = time(idx)
LW2 = LW(idx)
prec2 = prec(idx)
RH2 = RH(idx)
snow2 = snow(idx)
SW2 = SW(idx)
wind = sqrt(U(idx).^2+V(idx).^2)
LWout = 5.67*10^-8.*(273.15)^4
SWout = (1-alpha)*SW2
Tnew = T2(idx)
%%
figure, plot(x,p)
title("fraction of snow with given depth")
%%
% we make a date variable using matlab date-format
date=time2;
% make plots
figure
plot(date,SW2,'r')
datetick
hold all
plot(date,SWout,'b')
legend('SWin','SWout')
title('shortwave')
%%
% calculate longwave balance
% make plot
figure, hold all
plot(date,LW2,'r')
plot(date,LWout,'b') %this is constant
legend('LWin','LWout')
title('longwave')
datetick
%%
% net radiation
netradiationbalance=SW2+LW2-SWout-LWout;
% plot it
figure
plot(date,netradiationbalance)
datetick
title('net radiation')
%%
% define the constants
cp=1005;A=2.8885e-8;P=85000;T0=0;

%sesible heat 
sens= cp*A*P*wind.*(Tnew-TS);

Lv=2430000;
SaturationvapourpressurePa = 610.78.*exp((17.08085.*(Tnew-TS)./(234.15+Tnew-TS)));
vapourpressure = RH2.*SaturationvapourpressurePa;

%latent heat
latent=0.623*Lv*A*wind.*(vapourpressure-611);

% rain heat flux
%cw=4200;
%rhow=1000;
%Rainenergy=rhow*cw*(Tnew-T0).*prec2/3600/1000; % conversion from mm/h to m/s 

%%
% energy available for melt
Meltenergy=netradiationbalance+sens+latent;%+Rainenergy;

rhow = 1000;
% melt rate in mm/h
meltmmh=Meltenergy/334000/rhow*3600*1000;   % conversion m/s to mm/h
% negative melt is not plausible and set to zero. in those instances
% cooling would occur
meltmmh(meltmmh<0)=0;
disp("hei")
%%
SWE = rhow_snow*SD/rhow_water
