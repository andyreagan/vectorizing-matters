cpdef main():
    cdef unsigned int years = 10
    cdef unsigned int prem = 50
    cdef unsigned int wit = 5
    cdef unsigned int bom[120]
    cdef unsigned int eom[120]
    bom[0] = 0
    eom[0] = 0
    for month in range(1, years*12):
        bom[month] = eom[month-1] + prem
        eom[month] = bom[month] - wit
    return bom, eom