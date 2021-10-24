import numpy as np
import matplotlib.pyplot as plt

def getMistakes( X, Y, max_pass=500 ):
    rows, dim = X.shape
    W = np.array( [ 0 for i in range(dim) ] )
    b = 0.00
    mistakes = [ 0 for i in range(max_pass) ]

    for t in range(max_pass):
        for i in range(rows):
            if Y[i] * ( np.dot( W, X[i] ) + b ) <= 0:
                W = W + Y[i]*X[i]
                b = b + Y[i]
                mistakes[t] += 1
                                                        
    return mistakes

def plotMistakes( mistakes ):
    plt.figure()
    plt.xlabel( 'Passes' )
    plt.ylabel( 'Mistakes' )
    plt.title( 'Perceptron Algorithm convergence' )

    plt.plot( mistakes )
                    
