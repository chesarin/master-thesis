function [theta] = logistic(X, y)
%% Initialization
[m, n] = size(X);
initial_theta = zeros(n, 1);
options = optimset('GradObj', 'on', 'MaxIter', 400)
[theta, cost] = ...
        fminunc(@(t)(costFunction(t, X, y)), initial_theta, options);

end
