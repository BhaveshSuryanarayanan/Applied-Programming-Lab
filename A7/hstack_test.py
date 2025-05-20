import numpy as np

# Initial data array with n rows and some columns
n = 5  # number of rows
initial_data = np.zeros((n, 1))  # Start with 1 column (or more if needed)

# Iteratively add data horizontally in each loop
num_iterations = 3  # Number of times we want to add data
for i in range(num_iterations):
    # Generate new data to add (one column, n rows)
    new_data = np.full((n, 1), i + 1)  # Example: fill with increasing numbers
    print(new_data)
    # Concatenate new data horizontally with the old data
    initial_data = np.hstack((initial_data, new_data))
    print(initial_data)

print("Final Data Array:\n", initial_data)