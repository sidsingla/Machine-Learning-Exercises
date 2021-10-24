import numpy as np 
from scipy.special import expit
import pdb
import csv
import math, random

reader = csv.reader(open("train_X_dog_cat.csv", "rb"), delimiter=",")
x = list(reader)
X_train = np.array(x).astype("float")

reader = csv.reader(open("test_X_dog_cat.csv", "rb"), delimiter=",")
x = list(reader)
X_test = np.array(x).astype("float")

reader = csv.reader(open("train_y_dog_cat.csv", "rb"), delimiter=",")
y = list(reader)
Y_train = np.array(y).astype("float")

n, d = X_train.shape
test_n, _ = X_test.shape

reader = csv.reader(open("test_y_dog_cat.csv", "rb"), delimiter=",")
y = list(reader)
Y_test = np.array(y).astype("float")

# Normalizing matrices
for i in range(n):
    X_train[i] = X_train[i]/np.linalg.norm( X_train[i] )

for i in range(test_n):
    X_test[i] = X_test[i]/np.linalg.norm( X_test[i] )
    
def get_kernel_train_val(kernel):
    if kernel == 'linear':
        kernel_mat = np.dot(X_train, X_train.transpose())

    if kernel == 'poly':
        kernel_mat = ( 1 + np.dot(X_train, X_train.transpose()) ) ** 5

    return kernel_mat

def get_kernel_test_val(kernel):
    if kernel == 'linear':
        kernel_mat = np.dot(X_test, X_train.transpose())

    if kernel == 'poly':
        kernel_mat = ( 1 + np.dot(X_test, X_train.transpose()) ) ** 5
                
    return kernel_mat

kernels = ['linear', 'poly']
lambdas = [0, 20, 40, 60, 80 ]

for kernel in kernels:
    print "\nKernel ", kernel
    kernel_mat = get_kernel_train_val(kernel=kernel)
    kernel_test_train_mat = get_kernel_test_val(kernel=kernel)
    
    for lambd in lambdas:
        t = 1000
        alphas = np.ones(n) * 1e-7
        best_alphas = alphas
        ita = 1e-7
        best_train_error = 300.00
        prev_train_error = 10000.00

        while t >= 0:
            grad = np.zeros(n)
            train_error = 0.00
            mini_batch = np.random.choice( np.arange(n), 50 )
            for i in mini_batch:
                prod_alphas_kernel = np.matmul( alphas.transpose(), kernel_mat[i] )
                try:
                    pi = expit( prod_alphas_kernel )
                    #pi = 1/( 1 + math.exp( -prod_alphas_kernel ) )
                    reg_term = 2*lambd*np.matmul(alphas.transpose(),kernel_mat)
                    grad = grad + kernel_mat[i]*(pi - (Y_train[i]+1)/2) + reg_term

                    if pi >= 0.5 and Y_train[i] != 1:
                        train_error += 1.00
                    if pi < 0.5 and Y_train[i] != -1:
                        train_error += 1.00
                except:
                    pass
              
            if train_error <= best_train_error and train_error != 0:
                best_alphas = alphas
                best_train_error = train_error

            # Adjusting step function
            if abs(train_error - prev_train_error) > 2.00:
                ita = ita * 0.8
            else:
                ita = ita * 1.2
            prev_train_error = train_error
            
            alphas = alphas - (ita*grad)
            t = t-1

        errors = 0.00
        for ii in range(test_n):
            prod_alphas_kernel = np.matmul( best_alphas.transpose(), kernel_test_train_mat[ii] )
            pi = expit( prod_alphas_kernel )
            if pi >= 0.5 and Y_test[ii] != 1:
                errors += 1.00
            if pi < 0.5 and Y_test[ii] != -1:
                errors += 1.00

        print ("lambda ", lambd, " Percentage Test Error ", (errors*100)/test_n )
