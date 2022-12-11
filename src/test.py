from sortedcontainers import SortedDict
import numpy as np
# this file is for unit-test some functionality

if __name__ == '__main__':
    a = [ 1,1,2,3,4]
    a = np.array(a)
    print(np.argmin(a[a<2]))