function image_PCA = performPCA_matlab(image, n_components)
% Step 1: Load the 2D matrix
[rows, cols, channels] = size(image);

% get the channels*samples matrix
data = reshape(image, rows*cols, channels);

% Step 2: Calculate the mean of each feature
mean_values = mean(data);

% Step 3: Subtract the mean from each feature to center the data
centered_data = data - mean_values;

% Step 4: Calculate the covariance matrix
covariance_matrix = cov(centered_data);

% Step 5: Compute the eigenvectors and eigenvalues
[eigenvectors, eigenvalues] = eig(covariance_matrix);

% Step 6: Sort the eigenvalues in descending order
eigenvalues = diag(eigenvalues);
[eigenvalues, indices] = sort(eigenvalues, 'descend');
eigenvectors = eigenvectors(:, indices);
if n_components>=1

% Step 7: Retain either the first principal component or the components that explain 99% variance
% To retain the first principal component:
retained_eigenvectors = eigenvectors(:, 1);
else

% To retain the components explaining 99% variance:
cumulative_variance = cumsum(eigenvalues) / sum(eigenvalues);
num_components = find(cumulative_variance >= 0.99, 1);
retained_eigenvectors = eigenvectors(:, 1:num_components);
end
% Step 8: Perform PCA transformation
transformed_data = centered_data * retained_eigenvectors;

image_PCA=reshape(transformed_data, rows, cols, size(transformed_data,2));

