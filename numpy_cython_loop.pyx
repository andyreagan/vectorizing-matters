import numpy as np

cpdef main():
    cdef unsigned int years = 10
    cdef unsigned int prem = 50
    cdef unsigned int wit = 5
    bom = np.zeros(years*12)
    eom = np.zeros(years*12)
    for month in range(1, years*12):
        bom[month] = eom[month-1] + prem
        eom[month] = bom[month] - wit
    return bom, eom