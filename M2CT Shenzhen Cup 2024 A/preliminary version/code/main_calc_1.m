clear;format long g;

coords_ori = [110.241 27.204 824;
    110.780 27.456 727;
    110.712 27.785 742;
    110.251 27.825 850;
    110.524 27.617 786;
    110.467 27.921 678;
    110.047 27.121 575];

[x_t, y_t, z_t] = coord2xyz(coords_ori(:, 1), coords_ori(:, 2), coords_ori(:, 3));

times = [100.767 112.220 188.020 258.985 118.443 266.871 163.024];

for i = 1 : 1 : 7
    eval(sprintf('f%d = @(x) sqrt((x(1) - x_t(%d))^2 + (x(2) - y_t(%d))^2 + (x(3) - z_t(%d))^2) - (times(%d)-x(4))*0.34;', i, i, i, i, i));
end

sum = @(x) f1(x)^2+f2(x)^2+f3(x)^2+f4(x)^2+f6(x)^2+f7(x)^2;

x = fminunc(sum, [0 0 0 0]);

disp(x);