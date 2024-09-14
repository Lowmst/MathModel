% Simulated Annealing 模拟退火算法

function best_solution = SA(fun, init_solution)

    best_solution = init_solution; % 最优解
    
    init_temperature = 1; % 初始温度
    temperature = init_temperature;
    last_temperature = 10^(-30); % 终止温度
    rate = 0.99999; % 降温速度
    
    % 此处求优化函数的最小值
    
    while temperature > last_temperature
        next_solution = zeros(1, length(best_solution));
        for i = 1 : 1 : length(best_solution)
            next_solution(i) = best_solution(i) + (rand-0.5)/100;
        end
        if fun(next_solution) < fun(best_solution)
            best_solution = next_solution;
        else
            if rand < exp(-(fun(next_solution) - fun(best_solution)) / temperature)
                best_solution = next_solution;
            end
        end
        temperature = temperature * rate;
    end
end