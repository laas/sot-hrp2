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

        # Chest and head
        0., 0., 0., 0.,

        # Left Arm
        0.261799, -0.17453, 0., -0.523599, 0., 0., 0.1,
        # Left hand
        #0.,0.,0.,0.,0.,
        
        #Right Arm
        0.261799, 0.17453,  0., -0.523599, 0., 0., 0.1,
        #Right Hand
        #0.,0.,0.,0.,0.,

        # Legs
        0., 0., -0.453786, 0.872665, -0.418879, 0.,
        0., 0., -0.453786, 0.872665, -0.418879, 0.,

        )

    def __init__(self, name,
                 device = None,
                 tracer = None):

        # Define camera positions w.r.t gaze.

        # These positions have been copied from hrp2.geom and
        # roughly checked. Do not trust them too much.
        cameraBottomLeftPosition = np.matrix((
                (0.98481, 0.00000, 0.17365, 0.035),
                (0.,      1.,      0.,      0.072),
                (-0.17365, 0.00000, 0.98481, 0.075 - 0.03),
                (0., 0., 0., 1.),
                ))
        cameraBottomRightPosition = np.matrix((
                (0.98481, 0.00000, 0.17365, 0.035),
                (0.,      1.,      0.,     -0.072),
                (-0.17365, 0.00000, 0.98481, 0.075 - 0.03),
                (0., 0., 0., 1.),
                ))
        cameraTopLeftPosition = np.matrix((
                (0.99920,  0.00120, 0.03997, 0.01),
                (0.00000,  0.99955,-0.03000, 0.029),
                (-0.03999, 0.02997, 0.99875, 0.145 - 0.03),
                (0.,       0.,      0.,      1.),
                ))
        cameraTopRightPosition = np.matrix((
                (0.99920,  0.00000, 0.03999,  0.01),
                (0.00000,  1.00000, 0.00000, -0.029),
                (-0.03999, 0.00000, 0.99920,  0.145 - 0.03),
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
                       cameraTopLeftPosition, cameraTopRightPosition]:
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

        Hrp2.__init__(self, name, "14", device, tracer)

__all__ = ["Robot"]
