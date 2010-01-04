#!/usr/bin/python

import numpy
from sailfish import lbm
from sailfish import geo

import optparse
from optparse import OptionGroup, OptionParser, OptionValueError

class LBMGeoLDC(geo.LBMGeo3D):
    """Lid-driven cavity geometry."""

    max_v = 0.1

    def define_nodes(self):
        """Initialize the simulation for the lid-driven cavity geometry."""
        # bottom/top
        for x in range(0, self.lat_nx):
            for y in range(0, self.lat_ny):
                self.set_geo((x, y, self.lat_nz-1), self.NODE_VELOCITY, (self.max_v, 0.0, 0.0))
                self.set_geo((x, y, 0), self.NODE_WALL)

        # walls
        for z in range(1, self.lat_nz):
            for x in range(0, self.lat_nx):
                self.set_geo((x, 0, z), self.NODE_WALL)
                self.set_geo((x, self.lat_ny-1, z), self.NODE_WALL)
            for y in range(0, self.lat_ny):
                self.set_geo((0, y, z), self.NODE_WALL)
                self.set_geo((self.lat_nx-1, y, z), self.NODE_WALL)

    def init_dist(self, dist):
        self.velocity_to_dist((0, 0, 0), (0.0, 0.0, 0.0), dist)
        self.fill_dist((0, 0, 0), dist)

        self.velocity_to_dist((0, 0, self.lat_nz-1), (self.max_v, 0.0, 0.0), dist)
        self.fill_dist((0, 0, self.lat_nz-1), dist, target=(slice(None), slice(None), self.lat_nz-1))

    # FIXME
    def get_reynolds(self, viscosity):
        return int((self.lat_nx-1) * self.max_v/viscosity)

class LDCSim(lbm.LBMSim):

    filename = 'ldc'

    def __init__(self, geo_class):
        opts = []
        defaults={'lat_nz': 64, 'lat_ny': 64, 'lat_nx': 64, 'grid':
                'D3Q13', 'verbose': True}
        lbm.LBMSim.__init__(self, geo_class, options=opts, defaults=defaults)

sim = LDCSim(LBMGeoLDC)
sim.run()
