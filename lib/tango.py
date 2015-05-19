
import ctypes as ct
import os
import resource
import numpy as np

class Tango:

    def __init__(self, config, grid, lis, lie, ljs, lje, gis, gie, gjs, gje):

        # FIXME: this doesn't appear to work.
        resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY,
                                                   resource.RLIM_INFINITY))

        my_path = os.path.dirname(os.path.realpath(__file__))
        self.lib = ct.cdll.LoadLibrary(os.path.join(my_path, 'libtango.so'))

        self.lib.tango_init.argtypes = [ct.POINTER(ct.c_char),
                                        ct.POINTER(ct.c_char),
                                        ct.c_uint, ct.c_uint, ct.c_uint,
                                        ct.c_uint, ct.c_uint, ct.c_uint,
                                        ct.c_uint, ct.c_uint]
        self.lib.tango_begin_transfer.argtypes = [ct.c_int,
                                                  ct.POINTER(ct.c_char)]
        self.lib.tango_put.argtypes = [ct.POINTER(ct.c_char),
                                       ct.POINTER(ct.c_double), ct.c_int]
        self.lib.tango_get.argtypes = [ct.POINTER(ct.c_char),
                                       ct.POINTER(ct.c_double), ct.c_int]

        self.lib.tango_init(config, grid, lis, lie, ljs, lje,
                                               gis, gie, gjs, gje)

    def begin_transfer(self, time, grid_name):
        self.lib.tango_begin_transfer(time, grid_name)

    def put(self, field_name, array):
        assert(array.flags['C_CONTIGUOUS'])
        assert(array.dtype == 'float64')
        self.lib.tango_put(field_name,
                           array.ctypes.data_as(ct.POINTER(ct.c_double)),
                           array.size)

    def get(self, field_name, array):
        assert(array.flags['C_CONTIGUOUS'])
        assert(array.dtype == 'float64')
        self.lib.tango_get(field_name,
                           array.ctypes.data_as(ct.POINTER(ct.c_double)),
                           array.size)

    def end_transfer(self):
        self.lib.tango_end_transfer()

    def finalize(self):
        self.lib.tango_finalize()
        self.lib = None
