cdef extern from "include/instance.h":
    ctypedef unsigned int Some
    ctypedef struct Visitor:
        char *name
        Some id
        int date
    cdef void set_details(char *name, int date, Some id)
    cdef void get_details()