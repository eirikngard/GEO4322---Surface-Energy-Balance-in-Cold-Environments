function Q_h = Q_h(Tair, T_1, windspeed)
%q=specific humidity [kg/kg]

z =  2; %height of air temperature
z0 = 1e-2;  %roughness length
p = 1005.*100;

Tair=Tair+273.15;
T_1=T_1+273.15;

rho = p./(287.058.*Tair); %air density [kg m^(-3)]
cp=1005; %heat capacity of air
kappa=0.4;

Q_h  = -rho.*cp.*kappa.* windspeed.*kappa ./ log(z./z0) .* (Tair-T_1) ./ log(z./z0);

%% From lecture on this code:

%here we dont resolve the small scale turbulence
%We only use the "average" windspeed.

%this is an "average" eqation, takes away the ral physics 
%in turbulence, only describing the "net/long term" situation
%We are replaicing the navier stokes equation by 
%a parametrization

%we have proportionallity to windspeed, more wind gives 
%more eddies (turbulence).

%z_air is at 2m because: fluxes have been measured by the 
%eddy covariance method...?

% the eddy covariance is the basis for this skript..
%this is a simplification of the reality.
