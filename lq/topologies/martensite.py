##############################################################################
# Copyright (C) 2021, Advanced Design and Manufacturing Lab (ADML). 
# All rights reserved. 
#
# This software and its documentation and related materials are owned by 
# ADML. The software may only be incorporated into application programs owned
# by members of ADML. The structure and organization of this software are
# the valuable trade secrets of ADML and its suppliers. The software is also 
# protected by copyright law and international treaty provisions.
#
# By use of this software, its documentation or related materials, you 
# acknowledge and accept the above terms.
##############################################################################

from ..commons import eachpointAdaptive
from .fcc import unit_cell

import numpy as np

import cadquery as cq

# Register our custom plugins before use.
cq.Workplane.eachpointAdaptive = eachpointAdaptive

def fcc_martensite(unit_cell_size: float,
                    strut_diameter: float,
                    node_diameter: float,
                    # Nx: int,
                    Ny: int,
                    Nz: int,
                    uc_break: int):
    if uc_break < 1:
        raise ValueError('The value of the beginning of the break should larger than 1')
    UC_pnts = []
    Nx = Nz + uc_break - 1
    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                if k < i:
                    UC_pnts.append(
                        (i * unit_cell_size,
                        j * unit_cell_size,
                        k * unit_cell_size))
    print("Datapoints generated")
    result = cq.Workplane().tag('base')
    result = result.pushPoints(UC_pnts)
    unit_cell_params = []
    for i in range(Nx * Ny):
        for j in range(Nz):
            unit_cell_params.append({"unit_cell_size": unit_cell_size,
                "strut_radius": strut_diameter * 0.5,
                "node_diameter": node_diameter,
                "type": 'fcc'})
    result = result.eachpointAdaptive(unit_cell,
                                        callback_extra_args = unit_cell_params,
                                        useLocalCoords = True)
    print("The lattice is generated")
    return result