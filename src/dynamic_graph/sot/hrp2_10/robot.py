# -*- coding: utf-8 -*-
# Copyright 2011, Florent Lamiraux, Thomas Moulard, JRL, CNRS/AIST
#
# This file is part of dynamic-graph.
# dynamic-graph is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# dynamic-graph is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Lesser Public License for more details.  You should have
# received a copy of the GNU Lesser General Public License along with
# dynamic-graph. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
from dynamic_graph.sot.hrp2 import Hrp2
import numpy as np


# Internal helper tool.
def matrixToTuple(M):
    tmp = M.tolist()
    res = []
    for i in tmp:
        res.append(tuple(i))
    return tuple(res)

class Robot (Hrp2):
    """
    This class instanciates LAAS Hrp2 robot
    """
    halfSitting = (
        # Free flyer
        0., 0., 0.648702, 0., 0. , 0.,

        # Legs
        0., 0., -0.453786, 0.872665, -0.418879, 0.,
        0., 0., -0.453786, 0.872665, -0.418879, 0.,

        # Chest and head
        0., 0., 0., 0.,

        # Arms
        0.261799, -0.17453, 0., -0.523599, 0., 0., 0.1, 0.261799,
        0.261799, 0.17453,  0., -0.523599, 0., 0., 0.1, 0.261799,
        )

    def __init__(self, name,
                 device = None,
                 tracer = None):

        # Define camera positions w.r.t gaze.

        # These positions have been copied from hrp2_10.urdf
        # except for cameraTopLeftPosition and cameraTopRightPosition
        cameraBottomLeftPosition = np.matrix((
                (0.98703661, 0.05887354, 0.14930717, 0.0514675),
                (-0.06015316, 0.99818088, 0.00406493, 0.06761652),
                (-0.14879625, -0.01299353, 0.98878251, 0.06929336 - 0.03),
                (0., 0., 0., 1.),
                ))
        cameraBottomRightPosition = np.matrix((
                (0.97634419, -0.04283205,  0.21193734,  0.05735882),
                (0.04475292,  0.99898895, -0.00427252, -0.07566727),
                (-0.21154006, 0.01365627,  0.97727392,  0.07390919 - 0.03),
                (0., 0., 0., 1.),
                ))
        #very rough approximate coming from hrp2_14
        cameraTopLeftPosition = np.matrix((
                (0.99920,  0.00120, 0.03997, 0.01),
                (0.00000,  0.99955,-0.03000, 0.029),
                (-0.03999, 0.02997, 0.99875, 0.145 - 0.03),
                (0.,       0.,      0.,      1.),
                ))
        #very rough approximate coming from hrp2_14
        cameraTopRightPosition = np.matrix((
                (0.99920,  0.00000, 0.03999,  0.01),
                (0.00000,  1.00000, 0.00000, -0.029),
                (-0.03999, 0.00000, 0.99920,  0.145 - 0.03),
                (0.,       0.,      0.,       1.),
                ))
        cameraXtionRGBPosition = np.matrix((
                (0.98162902,  0.02441221, 0.18923135,  0.0869229361),
                (-0.02440555, 0.99969934, -0.00236575, 0.0149334883),
                (-0.18923221, -0.002296, 0.98192968,  0.108828329 - 0.03),
                (0.,       0.,      0.,       1.),
                ))

        # Frames re-orientation:
        # Z = depth (increase from near to far)
        # X = increase from left to right
        # Y = increase from top to bottom
        c1_M_c = np.matrix(
            [[ 0.,  0.,  1., 0.],
             [-1.,  0.,  0., 0.],
             [ 0., -1.,  0., 0.],
             [ 0.,  0.,  0., 1.]])

        for camera in [cameraBottomLeftPosition, cameraBottomRightPosition,
                       cameraTopLeftPosition, cameraTopRightPosition,
                       cameraXtionRGBPosition]:
            camera[:] = camera * c1_M_c

        self.AdditionalFrames.append(
                ("cameraBottomLeft",
                 matrixToTuple(cameraBottomLeftPosition), "gaze"))
        self.AdditionalFrames.append(
                ("cameraBottomRight",
                 matrixToTuple(cameraBottomRightPosition), "gaze"))
        self.AdditionalFrames.append(
                ("cameraTopLeft",
                 matrixToTuple(cameraTopLeftPosition), "gaze"))
        self.AdditionalFrames.append(
                ("cameraTopRight",
                 matrixToTuple(cameraTopRightPosition), "gaze"))
        self.AdditionalFrames.append(
                ("cameraXtionRGB",
                 matrixToTuple(cameraXtionRGBPosition), "gaze"))

        Hrp2.__init__(self, name, "10", device, tracer)

__all__ = ["Robot"]
