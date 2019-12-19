#!/usr/bin/python3

# computations for paper 'Enumeration of planar Tangles'

import tanglenum
import pandas
import time

tangle_type = ['fixed', 'one-sided', 'free']
P = 10

filename = 'enumeration_of_planar_tangles.txt'
open(filename, 'w').close()
file = open(filename, 'a')
file.write('Enumeration of Tangles of size <= ' + str(P) + '\n')
file.write('===================================\n')

start_time = time.time()
A = tanglenum.generate_tangles(P)
file.write('computation took ' + str(time.time() - start_time) + ' seconds\n\n')

for k in range(3):
    file.write(tangle_type[k] + ':\n')
    file.write(str(pandas.DataFrame(
        [[len(A[k][i][j]) for j in range(1,P+2)] for i in range(P+1)],
        columns = range(1, P+2))))
    file.write('\n\n')
file.close()
