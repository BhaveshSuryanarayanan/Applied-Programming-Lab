import csv
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Open the CSV file and read the data
file = open('d1.txt', 'r')
reader = csv.reader(file)

data = list(reader)
data = np.array(data, dtype=np.float64)

x, y = data[:, 0], data[:, 1]
n = x.size
print(n)

def f(l, a, b):
    return (a / (l**5)) / (np.exp(b / l) - 1)

initial_guess = [1.0000000000000001e-07, 515843448218.6518]

popt, pcov = curve_fit(f, x, y, p0=initial_guess)

a_opt, b_opt = popt
a =1.0000000000000001e-07
a = a**5
b = 515843448218.6518
y2 = a/ ((x**5)*(np.exp(b / x) - 1))
print(y2)
print(f"Fitted parameters: a = {a_opt}, b = {b_opt}")

loss = np.mean((y-y2)**2)
print(loss)
plt.scatter(x, y, label='Data', color='red')
plt.plot(x, y2, label='Fitted curve', color='blue')
plt.legend()
# plt.show()
