clc;clear;format long g;

function [c, ceq] = nonlinConstraints(x)
    c = -x(3);  % x3 > 0 可以写成 -x3 < 0
    ceq = [];   % 无等式约束
end

coords = [
    110.241 27.204 824;
    110.783	27.456 727;
    110.762	27.785 742;
    110.251	28.025 850;
    110.524	27.617 786;
    110.467	28.081 678;
    110.047	27.521 575
    ];

[x_t, y_t, z_t] = coord2xyz(coords(:, 1), coords(:, 2), coords(:, 3)); % 坐标转换

times = [
    100.767	164.229	214.850	270.065;
    92.453	112.220	169.362	196.583;
    75.560	110.696	156.936	188.020;
    94.653	141.409	196.517	258.985;
    78.600	86.216	118.443	126.669;
    67.274	166.270	175.482	266.871;
    103.738	163.024	206.789	210.306
    ];

% rand_t = rand(7, 4) - 0.5; % 引入随机误差
% times = times + rand_t;

final = [];

for sonic = 1 : 4
    len = length(times(1, :));
    results = [];
    results_index = [];
    for i = 1 : len
        for j = 1 : len
            for k = 1 : len
                for l = 1 : len
                    for m = 1 : len
                        for n = 1 : len
                            time = [times(1, 1) times(2, i) times(3, j) times(4, k) times(5, l) times(6, m) times(7, n)];

                            % 生成优化目标函数
                            for t = 1 : 1 : 7
                                eval(sprintf('f%d = @(x) sqrt((x(1) - x_t(%d))^2 + (x(2) - y_t(%d))^2 + (x(3) - z_t(%d))^2) - (time(%d)-x(4))*0.34;', t, t, t, t, t));
                            end
                            sum = @(x) f1(x)^2+f2(x)^2+f3(x)^2+f4(x)^2+f5(x)^2+f6(x)^2+f7(x)^2;

                            opt = optimoptions('fmincon', 'Display','none');
                            [x, fval] = fmincon(sum, [0 0 0 0], [], [], [], [], [], [], @nonlinConstraints, opt);

                            results = [results; times(1, 1) times(2, i) times(3, j) times(4, k) times(5, l) times(6, m) times(7, n) fval x];
                            results_index = [results_index; 1 i j k l m n fval];
                        end
                    end
                end
            end
        end
    end
    [~, min_index0] = min(results(:, 8));
    [~, min_index1] = min(results_index(:, 8));
    result = results(min_index0, :);
    result_index = results_index(min_index1, :);

    % 在times矩阵中去除已确定归属的时间数据
    for i = 1 : 7
        eval(sprintf('times_r%d = times(%d, :);', i, i));
        eval(sprintf('times_r%d(result_index(%d))=[];', i, i));
    end
    times = [times_r1;times_r2;times_r3;times_r4;times_r5;times_r6;times_r7];

    % 最终结果保存在final矩阵中，包含了各个残骸对应的时间数据，优化目标函数值，坐标，发生时间
    final = [final; result];
end

% 进行坐标转换并输出
[lo, la, he] = xyz2coord(final(:, 9), final(:, 10), final(:, 11));
disp([lo, la, he, final(:, 12)]);