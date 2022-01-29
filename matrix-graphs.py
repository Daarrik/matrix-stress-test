import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline

# classical_data = pd.read_csv('classical.csv', header=None)
# x = classical_data[0]
# y = classical_data[1]
# XYSpline = make_interp_spline(x, y)
# X = np.linspace(min(x), max(x), 500)
# Y = XYSpline(X)
# plt.plot(X, Y)
# plt.show()

# div_con_data = pd.read_csv('div_con.csv', header=None)
# x = div_con_data[0]
# y = div_con_data[1]
# XYSpline = make_interp_spline(x, y)
# X = np.linspace(min(x), max(x), 500)
# Y = XYSpline(X)
# plt.plot(X, Y)

# strassen_data = pd.read_csv('strassen.csv', header=None)
# x = strassen_data[0]
# y = strassen_data[1]
# XYSpline = make_interp_spline(x, y)
# X = np.linspace(min(x), max(x), 500)
# Y = XYSpline(X)
# plt.plot(X, Y)
# plt.xticks([2, 4, 8, 16, 32, 64, 128])
# plt.xlabel('Matrix size')
# plt.ylabel('Average time per calculation (s)')

# plt.legend(['Classical', 'Divide and Conquer', 'Strassen'])
# plt.show()

files = ['classical.csv', 'div_con.csv', 'strassen.csv']
for file in files:
    data = pd.read_csv(file, header=None)
    x = data[0]
    y = data[1]
    XYSpline = make_interp_spline(x, y)
    X = np.linspace(min(x), max(x), 500)
    Y = XYSpline(X)
    plt.plot(X, Y)
    plt.title(file[:file.index('.csv')])
    plt.xlabel('Matrix size')
    plt.ylabel('Average time per calculation (s)')
    plt.xticks([2, 4, 8, 16, 32, 64, 128])
    plt.show()