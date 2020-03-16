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