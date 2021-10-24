import csv
import perceptron_algo 
import numpy as np
import matplotlib.pyplot as plt

reader = csv.reader(open("spambase_X.csv", "rb"), delimiter=",")
x = list(reader)
X = np.array(x).astype("float")
X = X.transpose()

reader = csv.reader(open("spambase_y.csv", "rb"), delimiter=",")
Y = []
for row in reader:
    Y.append( int(row[0]) )

Y = np.array(Y)
mistakes = perceptron_algo.getMistakes( X, Y)
perceptron_algo.plotMistakes( mistakes )

plt.show()
                
print "Mistakes ", mistakes

