# Darrik Houck

import time
import numpy as np  # Used for random matrices and ease of splitting/concatenation
import csv

def classical_multiplication(m1, m2):
    # Disgusting list comprehension for matrix multiplication. Faster than nested for loops
    # result = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*m2)] for X_row in m1]

    result = [[0 for x in range(len(m1))] for y in range(len(m1))]
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m2)):
                result[i][j] += m1[i][k] * m2[k][j]
    return np.array(result)

def split_matrix(m):
    m11 = m[:int(len(m)/2), :int(len(m)/2)]
    m12 = m[:int(len(m)/2), int(len(m)/2):]
    m21 = m[int(len(m)/2):, :int(len(m)/2)]
    m22 = m[int(len(m)/2):, int(len(m)/2):]
    return m11, m12, m21, m22

def divide_and_conquer(m1, m2):
    if len(m1) == 1:
        return m1 * m2

    a11, a12, a21, a22 = split_matrix(m1)
    b11, b12, b21, b22 = split_matrix(m2)

    c11 = divide_and_conquer(a11, b11) + divide_and_conquer(a12, b21)
    c12 = divide_and_conquer(a11, b12) + divide_and_conquer(a12, b22)
    c21 = divide_and_conquer(a21, b11) + divide_and_conquer(a22, b21)
    c22 = divide_and_conquer(a21, b12) + divide_and_conquer(a22, b22)
    c = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))
    return c

def strassen(m1, m2):
    if len(m1) == 1:
        return m1 * m2

    a11, a12, a21, a22 = split_matrix(m1)
    b11, b12, b21, b22 = split_matrix(m2)

    p = strassen(a11 + a22, b11 + b22)
    q = strassen(a21 + a22, b11)
    r = strassen(a11, b12 - b22)
    s = strassen(a22, b21 - b11)
    t = strassen(a11 + a12, b22)
    u = strassen(a21 - a11, b11 + b12)
    v = strassen(a12 - a22, b21 + b22)

    c11 = p + s - t + v
    c12 = r + t
    c21 = q + s
    c22 = p + r - q + u
    c = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))
    return c

# def new_strassen(m1, m2):
#     a11, a12, a21, a22 = split_matrix(m1)
#     b11, b12, b21, b22 = split_matrix(m2)

#     if len(m1) == 2:
#         c11 = classical_multiplication(a11, b11) + classical_multiplication(a12, b21)
#         c12 = classical_multiplication(a11, b12) + classical_multiplication(a12, b22)
#         c21 = classical_multiplication(a21, b11) + classical_multiplication(a22, b21)
#         c22 = classical_multiplication(a21, b12) + classical_multiplication(a22, b22)
#         c = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))
#         return c

#     p = new_strassen(a11 + a22, b11 + b22)
#     q = new_strassen(a21 + a22, b11)
#     r = new_strassen(a11, b12 - b22)
#     s = new_strassen(a22, b21 - b11)
#     t = new_strassen(a11 + a12, b22)
#     u = new_strassen(a21 - a11, b11 + b12)
#     v = new_strassen(a12 - a22, b21 + b22)

#     c11 = p + s - t + v
#     c12 = r + t
#     c21 = q + s
#     c22 = p + r - q + u
#     c = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))
#     return c
    
def main():
    sizes = [2, 4, 8, 16, 32, 64, 128] 
    runs = 20
    num_matrices = 500

    for n in sizes:
        classical_sum, div_con_sum, strassen_sum = 0, 0, 0
        for run in range(0, runs):  # Start of runs
            set1 = []
            set2 = []

            print(f'creating matrices of size {n}x{n} for run {run}')
            for i in range(0, num_matrices):
                set1.append(np.random.randint(low=0, high=10, size=(n, n)))
                set2.append(np.random.randint(low=0, high=10, size=(n, n)))
            
            print('classical multiplication')
            start_time = time.time()
            for i in range(len(set1)):
                classical_multiplication(set1[i], set2[i])
            end_time = time.time()
            time_elapsed = end_time - start_time
            avg_calc_time = time_elapsed/len(set1)
            classical_sum += avg_calc_time
            print(f'time elapsed: {time_elapsed}')
            print(f'average time per calculation: {avg_calc_time}')
            print()

            print('divide and conquer')
            start_time = time.time()
            for i in range(len(set1)):
                divide_and_conquer(set1[i], set2[i])
            end_time = time.time()
            time_elapsed = end_time - start_time
            avg_calc_time = time_elapsed/len(set1)
            div_con_sum += avg_calc_time
            print(f'time elapsed: {time_elapsed}')
            print(f'average time per calculation: {avg_calc_time}')
            print()

            print('strassen method')
            start_time = time.time()
            for i in range(len(set1)):
                strassen(set1[i], set2[i])
            end_time = time.time()
            time_elapsed = end_time - start_time
            avg_calc_time = time_elapsed/len(set1)
            strassen_sum += avg_calc_time
            print(f'time elapsed: {time_elapsed}')
            print(f'average time per calculation: {avg_calc_time}')
            print()
            # End of runs
        with open('classical.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([n, classical_sum/runs])
        with open('div_con.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([n, div_con_sum/runs])
        with open('strassen.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([n, strassen_sum/runs])

if __name__ == '__main__':
    main()