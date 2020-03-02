clear
close all

% first step is to import the data from the forcing file. 
load('meteoFinse20162018_AromeNorway_apr2018.mat');
% loads variables SW, LW, T2, U, V, RH, precip, snow, baro, time
% assume:
alpha = 0.7;
LWout= 316; % W m-2 --> melting surface
% no precip
% no heat conduction --> isothermal snow

% load Snow PDF
load('FinseSWEpdf.mat'); % x,p. p is snowcower-fraction
rhos = 333;
rhow = 1000;

for i=1:length(x)
    % initial SWE
    SWE_0 = x(i)*rhos/rhow; % m w.e. 

    % cut out the period of interest
    idx=find(time>=datenum(2016,5,1)&time<datenum(2016,10,1)); 

    % give the variables nice names
    date = time(idx);
    temperature = T2(idx)-273.15;
    humidity = RH(idx);
    windspeed = sqrt(U(idx).^2+V(idx).^2);
    globalrad = SW(idx);
    reflected = alpha*SW(idx);
    longwave_in = LW(idx);
    longwave_out = zeros(size(LW(idx)))+LWout;
    precip = zeros(size(prec(idx)));

    % calculate longwave balance
    longwavebalance=longwave_in-longwave_out;

    % net radiation
    netradiationbalance=globalrad-reflected+longwavebalance;

    % define the constants
    cp=1005;A=2.8885e-8;P=85000;T0=0; %T0=273.15

    % calculate the turbulent fluxes
    sens= cp*A*P*windspeed.*(temperature-T0);

    Lv=2430000;
    SaturationvapourpressurePa = 610.78.*exp((17.08085.*temperature)./(234.15+temperature));
    vapourpressure = humidity.*SaturationvapourpressurePa;

    latent=0.623*Lv*A*windspeed.*(vapourpressure-611);

    % rain heat flux
    cw=4200;
    rhow=1000;
    Rainenergy=rhow*cw*(temperature-T0).*precip/3600/1000; % conversion from mm/h to m/s 

    % energy available for melt
    Meltenergy=netradiationbalance+sens+latent+Rainenergy; %supposed to drop rainenergy?

    % melt rate in mm/h
    meltmh=Meltenergy/334000/rhow*3600;   % conversion m/s to m/h
    % negative melt is not plausible and set to zero. in those instances
    % cooling would occur
    meltmh(meltmh<0)=0;

    % % the total amount of melt during this period
    % totalmelt = sum(meltmh);
    % 
    % disp(['total melt = ',num2str(totalmelt),' m'])

    SWE(i,:) = SWE_0 -cumsum(meltmh);
    SWE(i,:) = max(SWE(i,:),0);
end

%% An area is snwcovered, each bin of the area has a given depth
%% we select all snowcoverd points and weight them with the area-fraction p
%% Then summing the weighted snowcover-fractions 

SCI=double(SWE>0); %where do we have snow? snow/NO-SNOW

for i2=1:length(p)
    SCI(i2,:)=SCI(i2,:)*p(i2); %weighting the snowcover
end
figure, plot(date,SCI)

SCF = sum(SCI,1); %snow cover fraction, summing the weighted snowcoverfractions

figure
plot(date,SCF)
datetick

figure
plot(date,SWE)
datetick
hold on

for i=1:9
swe_p(i,:)=SWE(i,:)*p(i);
end
swe_area=sum(swe_p,1);
plot(date,swe_area,'k','linewidth',2)
%this is plotting how the snowcover would decrease with differnt
%startingpoint and the weighted sum of the SWE