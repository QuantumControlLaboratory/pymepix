import pickle

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

datas = pickle.load( open( "datas_triggered.p", "rb" ) )

print("Number Trigger: ", len(datas))
for trig_data in datas:
    typ, trig, t, x, y = trig_data

    grid = np.zeros((255,255))

    for sx, sy in zip(x,y):
        grid[sx][sy] += 1

    plt.imshow(grid,norm=matplotlib.colors.LogNorm(),cmap=plt.cm.jet)

    plt.show()

    x = list(range(len(t)))
    plt.plot(t, x)
    plt.show()
