# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent

from ... import config
if not config.is_building_docs():
    from qiskit_metal import is_true


class ChipBorder(QComponent):
    """
    This class is a template
	Use this class as a blueprint to put together for your components - have fun

    .. meta::
        My QComponent

    """

    # Edit these to define your own template options for creation
    # Default drawing options
    default_options = Dict(inset = '150um',
                            corner_inset='550um',
                            chip_x='chip_size_x',
                            chip_y='chip_size_y')
    """Default drawing options"""

    # Name prefix of component, if user doesn't provide name
    component_metadata = Dict(short_name='border')
    """Component metadata"""

    def make(self):
        """Convert self.options into QGeometry."""

        p = self.p  # Parse the string options into numbers

        wo_x = (p.chip_x - p.inset)/2
        wo_y = (p.chip_y - p.inset)/2
        ci = p.corner_inset

        inner = draw.Polygon([(-wo_x+ci,-wo_y), (-wo_x, -wo_y+ci), (-wo_x, wo_y-ci), (-wo_x+ci, wo_y),
                                (wo_x-ci, wo_y), (wo_x, wo_y-ci), (wo_x, -wo_y+ci), (wo_x-ci, -wo_y)])
        outer = draw.rectangle(p.chip_x, p.chip_y, 0, 0)

        border = draw.subtract(outer, inner)

        border = draw.translate(border, p.pos_x, p.pos_y)

        geom = {'my_polygon': border}
        self.add_qgeometry('poly', geom, layer=p.layer, subtract=True)
