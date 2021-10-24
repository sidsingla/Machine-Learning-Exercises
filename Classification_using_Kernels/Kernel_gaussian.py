from __future__ import division
import numpy as np 
import pandas as pd
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
    
def get_kernel_train_val(sig):
    kernel_mat = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            kernel_mat[i][j] = np.exp( -np.linalg.norm( X_train[i] - X_train[j] )/float(sig) )
        #kernel_mat[i] = kernel_mat[i]/np.linalg.norm( kernel_mat[i] )
    return kernel_mat

def get_kernel_test_val(sig):
    kernel_mat = np.zeros((test_n,n))
    for i in range(test_n):
        for j in range(n):
            euc_dist = np.linalg.norm( X_test[i] - X_train[j] )
            kernel_mat[i][j] = math.exp( -euc_dist/float(sig) )            
        #kernel_mat[i] = kernel_mat[i]/np.linalg.norm( kernel_mat[i] )

    return kernel_mat

for sigma in range(2, 11, 2):
    kernel_mat = get_kernel_train_val(sigma)
    kernel_test_train_mat = get_kernel_test_val(sigma)

    for lambd in range(0, 51, 10):
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
                prod_alphas_kernel = np.dot( alphas.transpose(), kernel_mat[i] )
                try:
                    pi = expit( prod_alphas_kernel )
                    #pi = 1/( 1 + math.exp( -prod_alphas_kernel ) )
                    reg_term = 2*lambd*np.dot(alphas.transpose(),kernel_mat)
                    grad = grad + kernel_mat[i]*(pi - (Y_train[i]+1)/2) + reg_term

                    if pi >= 0.5 and Y_train[i] != 1:
                        train_error += 1.00
                    if pi < 0.5 and Y_train[i] != -1:
                        train_error += 1.00
                except:
                    pass
                
            if train_error <= best_train_error:
                best_alphas = alphas
                best_train_error = train_error

            if abs(train_error - prev_train_error) > 2.00:
                ita = ita * 0.9
            else:
                ita = ita * 1.1
            prev_train_error = train_error
            #print( "t ", t, " Training error", train_error )

            alphas = alphas - (ita*grad)
            t = t-1

        errors = 0.00
        for ii in range(test_n):
            prod_alphas_kernel = np.matmul( best_alphas.transpose(), kernel_test_train_mat[ii] )
            #pi = 1/( 1 + math.exp( -prod_alphas_kernel ) )
            pi = expit( prod_alphas_kernel )
            if pi >= 0.5 and Y_test[ii] != 1:
                errors += 1.00
            if pi < 0.5 and Y_test[ii] != -1:
                errors += 1.00

        print ("Sigma ", sigma, " lambda ", lambd, " Percentage Test Error ", (errors*100)/test_n )

