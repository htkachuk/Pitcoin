import numpy as np
import matplotlib.pyplot as plt

def main():
    a = 6
    #Tкачук
    b = 13
    #Анна-Кристина

    y, x = np.ogrid[-5:5:100j, -5:5:100j]
    fig = plt.figure()
    pl = plt.subplot() 
    pl.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - x * a - b, [0])
    pl.grid()
    plt.show()
    fig.savefig('curve.png', bbox_inches='tight')

if __name__ == '__main__':
    main()