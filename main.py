#!/usr/bin/python3
import ctypes
from ctypes import CDLL, POINTER, c_int, c_float
import numpy as np
import time
import sys

print('Input array size')
S = input()
lowC = 1
highC = 10

C_LIB_NO_OPT = CDLL('./lib/bin/c_lib_no_opt.so')
C_LIB_OPT = CDLL('./lib/bin/c_lib_opt.so')
C_LIB_VECT = CDLL('./lib/bin/c_lib_vect.so')
C_LIB_AL = CDLL('./lib/bin/c_lib_al.so')

C_LIB_NO_OPT.cFunc.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), c_int]
C_LIB_OPT.cFunc.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), c_int]
C_LIB_VECT.cFunc.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), c_int]
C_LIB_AL.cFunc.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), c_int]

total = np.empty((1,), dtype=c_float)

#Memory allocation
A = np.empty((S,S), dtype=c_float)
L = np.empty((S,S), dtype=c_float)
U = np.empty((S,S), dtype=c_float)
B = np.empty((S,S), dtype=c_float)
C = np.empty((S,S), dtype=c_float)
R = np.empty((S,S), dtype=c_float)
Check = np.empty((S,S), dtype=c_float)

B[:][:] = np.random.randint(low=lowC, high = highC, size = (S,S))
C[:][:] = np.random.randint(low=lowC, high = highC, size = (S,S))

print("Starting without opt: ")
start = time.time()

C_LIB_NO_OPT.cFunc(A.ctypes.data_as(POINTER(c_float)),
				   B.ctypes.data_as(POINTER(c_float)),
				   C.ctypes.data_as(POINTER(c_float)),
				   L.ctypes.data_as(POINTER(c_float)),
				   U.ctypes.data_as(POINTER(c_float)),
				   R.ctypes.data_as(POINTER(c_float)),
				   Check.ctypes.data_as(POINTER(c_float)),
				   total.ctypes.data_as(POINTER(c_float)),
				   c_int(S))

stop = time.time()

np.set_printoptions(precision=2)
seconds = stop - start
print(seconds, 'seconds')
print

total = np.empty((1,), dtype=c_float)

A = np.empty((S,S), dtype=c_float)
L = np.empty((S,S), dtype=c_float)
U = np.empty((S,S), dtype=c_float)
R = np.empty((S,S), dtype=c_float)
Check = np.empty((S,S), dtype=c_float)

print("Starting with vectorization: ")
start = time.time()

C_LIB_OPT.cFunc(A.ctypes.data_as(POINTER(c_float)),
				 B.ctypes.data_as(POINTER(c_float)),
				 C.ctypes.data_as(POINTER(c_float)),
				 L.ctypes.data_as(POINTER(c_float)),
				 U.ctypes.data_as(POINTER(c_float)),
				 R.ctypes.data_as(POINTER(c_float)),
				 Check.ctypes.data_as(POINTER(c_float)),
				 total.ctypes.data_as(POINTER(c_float)),
				 c_int(S))

stop = time.time()

np.set_printoptions(precision=2)
seconds = stop - start
print(seconds, 'seconds')
print


total = np.empty((1,), dtype=c_float)

A = np.empty((S,S), dtype=c_float)
L = np.empty((S,S), dtype=c_float)
U = np.empty((S,S), dtype=c_float)
R = np.empty((S,S), dtype=c_float)
Check = np.empty((S,S), dtype=c_float)

print("Starting with parallel: ")
start = time.time()

C_LIB_VECT.cFunc(A.ctypes.data_as(POINTER(c_float)),
				B.ctypes.data_as(POINTER(c_float)),
				C.ctypes.data_as(POINTER(c_float)),
				L.ctypes.data_as(POINTER(c_float)),
				U.ctypes.data_as(POINTER(c_float)),
				R.ctypes.data_as(POINTER(c_float)),
				Check.ctypes.data_as(POINTER(c_float)),
				total.ctypes.data_as(POINTER(c_float)),
				c_int(S))

stop = time.time()

np.set_printoptions(precision=2)
seconds = stop - start
print(seconds, 'seconds')
print

A = np.empty((S,S), dtype=c_float)
L = np.empty((S,S), dtype=c_float)
U = np.empty((S,S), dtype=c_float)
R = np.empty((S,S), dtype=c_float)
Check = np.empty((S,S), dtype=c_float)

print("Starting with vectorization and parallel: ")
start = time.time()

C_LIB_VECT_AL.cFunc(A.ctypes.data_as(POINTER(c_float)),
				   	 B.ctypes.data_as(POINTER(c_float)),
				   	 C.ctypes.data_as(POINTER(c_float)),
				   	 L.ctypes.data_as(POINTER(c_float)),
				   	 U.ctypes.data_as(POINTER(c_float)),
				     R.ctypes.data_as(POINTER(c_float)),
				     Check.ctypes.data_as(POINTER(c_float)),
				     total.ctypes.data_as(POINTER(c_float)),
				     c_int(S))

stop = time.time()

np.set_printoptions(precision=2)
seconds = stop - start
print(seconds, 'seconds')
print
