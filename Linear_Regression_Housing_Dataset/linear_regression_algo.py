import numpy as np

# ( xTx + lamBda * I )W = xTy
def getW( X, Y, lamBda ):
    rows, dim = X.shape
    xTx = np.matmul(X.transpose(), X)
    xTy = np.matmul(X.transpose(), Y)
    W = np.linalg.solve(xTx + lamBda*np.identity(dim), xTy)
    return W

def getMSE( X, Y, W ):
    Y_Pred = np.matmul(X, W)
    Y_err = Y_Pred - Y
    mse = np.matmul( Y_err.transpose(), Y_err )/len(Y)
    return mse[0][0]

def getNonZeros( W ):
    dim, _ = W.shape
    c = 0
    for i in range(dim):
        if W[i][0] != 0:
            c += 1

    percent_nonzero_W = c/dim * 100
    return percent_nonzero_W
