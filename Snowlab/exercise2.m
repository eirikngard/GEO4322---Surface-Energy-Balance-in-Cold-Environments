% plot and evaluate SEB from Austfonna over 2004 and 2008 melt seasons
% 
% Exercise 2, GEO4420, Torbjørn I. Østby
%
% EXPLANATION OF VARIABLES
% SEB2004:  struct of data from the 2004 summer season (May-September)
% SEB2008:  struct of data from the 2008 summer season (May-September)
%   t:          time, daily ( datenum format)
%   Tair:       measured air temperature at the AWS. (deg C)
%   albedo:     surface reflectance. (-)
%   Precip:     daily precipitation (mm)
%   SWin:       incoming short wave radiation (W/m2)
%   SWout:      reflected short wave radiation (W/m2)
%   LWin:       Absorbed long wave radiation (W/m2)
%   LWout:      Emitted long wave radiation (W/m2)
%   SH:         Sensible heat (W/m2)
%   LE:         Latent heat (W/m2)
%   R:          Sensible heat supplied by rain (W/m2)
%   G:          sub-surface energy exchange (W/m2)
%   M:          Melt (W/m2)
%   runoff:     Runoff pr day (mm w.eq.) / (kg/m^2)
%   refrozen:   refrozen water pr day (mm w.eq.) / (kg/m^2)
%   snowdepth:  Snow depth relative to ice surface (cm)

clear all, close all


%% load
load('SEB2004.mat')
load('SEB2008.mat')

%% exercise 2 a)
% plot SEB fluxes
figure
subplot(211) % 2004
plot(SEB04.t,SEB04.SWin-SEB04.SWout,'m',SEB04.t,SEB04.LWin-SEB04.LWout,'g'...
    ,SEB04.t,SEB04.SH,'r',SEB04.t,SEB04.LE,'b',SEB04.t,SEB04.R,'y',SEB04.t,SEB04.G,'c',SEB04.t,SEB04.M,'k')
title('Daily SEB-fluxes 2004'), ylabel('energy flux (W m^{-2})'),datetick('x',12)
legend('SW_{net}','LW_{net}','SH','LE','R','G','M')

subplot(212) % 2008
plot(SEB08.t,SEB08.SWin-SEB08.SWout,'m',SEB08.t,SEB08.LWin-SEB08.LWout,'g'...
    ,SEB08.t,SEB08.SH,'r',SEB08.t,SEB08.LE,'b',SEB08.t,SEB08.R,'y',SEB08.t,SEB08.G,'c',SEB08.t,SEB08.M,'k')
title('Daily SEB-fluxes 2008'), ylabel('energy flux (W m^{-2})'),datetick('x',12)
legend('SW_{net}','LW_{net}','SH','LE','R','G','M')
%%
% Calculate melt pr day (m w.eq.)
rho_water = 1000;
Lf = 334000; %phase change ice to water 
we_melt = SEB04.M/rho_water.*Lf; %[m/s]????
we_melt2 = we_melt./1000. * 86400; %[mm/day]??
we_melt_day = (we_melt2/SEB04.t);%[mm/day] t is days
figure, grid on, hold on
plot(SEB04.t,SEB04.runoff,'g')
plot(SEB04.t,we_melt_day), ylabel('mm/day water equi. melt')
legend('runoff','melt equivalent')
datetick
%See from this figure that runoff>melt.
%%
%Calculate monthly melt water eq. pr day
%month1 = SEB04.t(1:30)
%month2 = t(31:61)
%month3 = t(62:92)
%we_melt1 = we_melt_day(month1)
%figure
%plot(we_melt1)
%we_melt3 = we_melt_day(month3)

%%
%Correlation between albedo, snowdepth and refreezing
%albedo refrozen snowdepth
corr_alb_snow4 = corr(SEB04.albedo,SEB04.snowdepth)
corr_alb_snow8 = corr(SEB08.albedo,SEB08.snowdepth)
cor_str4 = sprintf('correlation 4 is %.2f',corr_alb_snow4)
cor_str8 = sprintf('correlation 8 is %.2f',corr_alb_snow8)
figure,hold on, grid on, title('correlation albedo snowdepth')
scatter(SEB04.albedo,SEB04.snowdepth, 'r','filled')
scatter(SEB08.albedo,SEB08.snowdepth, 'b','filled')
legend(cor_str4,cor_str8)

corr_alb_ref4 = corr(SEB04.albedo,SEB04.refrozen)
corr_alb_ref8 = corr(SEB08.albedo,SEB08.refrozen)
cor_str4 = sprintf('correlation 4 is %.2f',corr_alb_ref4)
cor_str8 = sprintf('correlation 8 is %.2f',corr_alb_ref8)
figure,hold on, grid on, title('correlation albedo refreezing')
scatter(SEB04.albedo,SEB04.refrozen, 'r','filled')
scatter(SEB08.albedo,SEB08.refrozen, 'b','filled')
legend(cor_str4,cor_str8)

corr_ref_snow4 = corr(SEB04.refrozen,SEB04.snowdepth)
corr_ref_snow8 = corr(SEB08.refrozen,SEB08.snowdepth)
cor_str4 = sprintf('correlation 4 is %.2f',corr_ref_snow4)
cor_str8 = sprintf('correlation 8 is %.2f',corr_ref_snow8)
figure,hold on, grid on,title('correlation refreezing snowdepth') 
scatter(SEB04.refrozen,SEB04.snowdepth, 'r','filled')
scatter(SEB08.refrozen,SEB08.snowdepth, 'b','filled')
legend(cor_str4,cor_str8)
%%
corr_alb_run4 = corr(SEB04.albedo,SEB04.runoff)
corr_alb_run8 = corr(SEB08.albedo,SEB08.runoff)
cor_str4 = sprintf('correlation 4 is %.2f',corr_alb_run4)
cor_str8 = sprintf('correlation 8 is %.2f',corr_alb_run8)
figure,hold on, grid on,title('correlation albedo runoff') 
scatter(SEB04.albedo,SEB04.runoff, 'r','filled')
scatter(SEB08.albedo,SEB08.runoff, 'b','filled')
legend(cor_str4,cor_str8)

%% b)
% plot Tair, albedo and runoff for these years
t = SEB04.t-datenum(2004,1,1,0,0,0); % common time
figure,set(gcf,'units','normalized','outerposition',[0 0 .7 1]);
subplot(511),plot(t,SEB04.Tair,'k',t,SEB08.Tair,'r'...
    ,t,zeros(size(t)),':k'),ylabel('daily T_{air} (\circC)')...
    ,legend('2004','2008'),datetick('x',3),set(gca,'xticklabel',[]),axis tight
subplot(512),plot(t,SEB04.albedo,'k',t,SEB08.albedo,'r'),ylabel('daily albedo (-)')...
    ,datetick('x',3),set(gca,'xticklabel',[]),axis tight
subplot(513),plot(t,SEB04.runoff,'k',t,SEB08.runoff,'r')...
    ,ylabel('daily runoff (mm w.eq.)'),datetick('x',3),set(gca,'xticklabel',[]),axis tight
subplot(514),plot(t,zeros(size(t)),'c',t,SEB04.snowdepth,'k'...
    ,t,SEB08.snowdepth,'r'),ylabel({'snow depth (cm)','rel. to last summer surface'})...
    ,datetick('x',3),set(gca,'xticklabel',[]),axis tight
subplot(515),plot(t,SEB04.refrozen,'k',t,SEB08.refrozen,'r')...
    ,ylabel('daily refreezing (mm w.eq.)'),datetick('x',3),axis tight

%% c) Radiation balance and clouds
% plot SWin, SWout,LWin,LWout and net
figure
subplot(211) % 2004
plot(SEB04.t,SEB04.SWin,'m',SEB04.t,SEB04.SWout,'g'...
    ,SEB04.t,SEB04.LWin,'r',SEB04.t,SEB04.LWout,'b'...
    ,SEB04.t,SEB04.SWin-SEB08.SWout,'y',SEB04.t,SEB04.LWin-SEB08.LWout,'c'...
    ,SEB04.t,SEB04.SWin-SEB04.SWout+SEB04.LWin-SEB04.LWout,'k')
title('Daily SEB-fluxes 2004'), ylabel('energy flux (W m^{-2})'),datetick('x',12)
legend('SW_{in}','SW_{out}','LW_{in}','LW_{out}','SW_{net}','LW_{net}','Total')

subplot(212) % 2008
plot(SEB08.t,SEB08.SWin,'m',SEB08.t,SEB08.SWout,'g'...
    ,SEB08.t,SEB08.LWin,'r',SEB08.t,SEB08.LWout,'b'...
    ,SEB08.t,SEB08.SWin-SEB08.SWout,'y',SEB08.t,SEB08.LWin-SEB08.LWout,'c'...
    ,SEB08.t,SEB08.SWin-SEB08.SWout+SEB08.LWin-SEB08.LWout,'k')
title('Daily SEB-fluxes 2004'), ylabel('energy flux (W m^{-2})'),datetick('x',12)
legend('SW_{in}','SW_{out}','LW_{in}','LW_{out}','SW_{net}','LW_{net}','Total')
%% d) mass balance
% bn = bw + bs 
% In: precipitation (mm)
%Out: runoff 
%   runoff:     Runoff pr day (mm w.eq.) / (kg/m^2)
%   refrozen:   refrozen water pr day (mm w.eq.) / (kg/m^2)
%   snowdepth:  Snow depth relative to ice surface (cm)

figure, hold on
plot(SEB04.t,SEB04.Precip)
plot(SEB04.t,SEB04.runoff)
plot(SEB04.t,SEB04.Precip-SEB04.runoff)