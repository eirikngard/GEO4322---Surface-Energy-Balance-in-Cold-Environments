function value = interpolate_in_time(time, variable)

time= time.*8;
before = floor(time)+1;
fraction = time - (before-1);
value = (1-fraction) .* variable(before) + fraction .* variable(before+1);