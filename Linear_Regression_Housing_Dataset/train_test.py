import csv
import numpy as np
import linear_regression_algo

reader = csv.reader(open("housing_X_train.csv", "rb"), delimiter=",")
x = list(reader)
X = np.array(x).astype("float")

reader = csv.reader(open("housing_X_test.csv", "rb"), delimiter=",")
x = list(reader)
X_test = np.array(x).astype("float")

dim,rows = X.shape
X = np.insert(X, dim, values=1, axis=0)
X_test = np.insert(X_test, dim, values=1, axis=0)

X = X.transpose()
X_test = X_test.transpose()

dim = dim + 1

reader = csv.reader(open("housing_y_train.csv", "rb"), delimiter=",")
y = list(reader)
Y = np.array(y).astype("float")

reader = csv.reader(open("housing_y_test.csv", "rb"), delimiter=",")
y = list(reader)
Y_test = np.array(y).astype("float")

lamBda = 0
set_size = rows/10
bestlamBda_train = 0
min_error_train = 1e+18
bestlamBda_test = 0
min_error_test = 1e+18

while lamBda <= 100:
    print "\nlamBda ", lamBda

    W = linear_regression_algo.getW( X, Y, lamBda )
    train_error = linear_regression_algo.getMSE( X, Y, W )    
    print "Training error ", train_error

    if train_error < min_error_train:
        bestlamBda_train = lamBda
        min_error_train = train_error

    test_error = linear_regression_algo.getMSE( X_test, Y_test, W )
    print "Test error ", test_error

    if test_error < min_error_test:
        bestlamBda_test = lamBda
        min_error_test = test_error

    print "Percentage of nonzeros in W for lambda ", lamBda, linear_regression_algo.getNonZeros( W )

    lamBda += 10

lamBda = 0
bestlamBda_validation = 0
min_error_validation = 1e+18

while lamBda <= 100:
    print "\nlamBda ", lamBda
    k = 10

    sum_MSE = 0
    for i in range( 0, rows, set_size ):
        validation_set_X = X[i:i+set_size]
        validation_set_Y = Y[i:i+set_size]

        if i <= 0:
            training_set_X = X[i+set_size:rows]
            training_set_Y = Y[i+set_size:rows]
        elif k == 1:
            validation_set_X = X[i:rows]
            validation_set_Y = Y[i:rows]
            training_set_X = X[0:i]
            training_set_Y = Y[0:i]
        elif k < 1:
            break
        else:
            training_set_X = X[0:i-1]
            training_set_X = np.insert( training_set_X, len(training_set_X), values=X[i+set_size:rows], axis=0 )
            training_set_Y = Y[0:i-1]
            training_set_Y = np.insert( training_set_Y, len(training_set_Y), values=Y[i+set_size:rows], axis=0 )

        
        W = linear_regression_algo.getW( training_set_X, training_set_Y, lamBda )
        print "Percentage of nonzeros in W for lambda ", lamBda, linear_regression_algo.getNonZeros( W )
        
        k -= 1

        MSE = linear_regression_algo.getMSE( validation_set_X, validation_set_Y, W )
        sum_MSE += MSE
    avg_MSE = sum_MSE/10
    print "Average MSE ", str( avg_MSE )
    if avg_MSE < min_error_validation:
        bestlamBda_validation = lamBda
        min_error_validation = avg_MSE
    lamBda += 10

print "\nBest lambda for training ", bestlamBda_train
print "Best lambda for testing ", bestlamBda_test
print "Best lambda for validation ", bestlamBda_validation
