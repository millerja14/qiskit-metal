from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent
import numpy as np

class CapCoupler(QComponent):
    """
    Generates two pin capacitive coupler.
    """

    default_options = Dict(
        gap = "4um",
        width = "100um",
        length = "30um",
        gnd_gap = 'cpw_gap',
        cpw_width = 'cpw_width',
        cpw_gap = 'cpw_gap'
    )

    """Default options."""

    component_metadata = Dict(short_name='cap',
                              _qgeometry_table_poly='True',
                              _qgeometry_table_junction='True')
    """Component metadata"""

    TOOLTIP = """Simple Capacitive Coupler."""

    ##############################################MAKE######################################################

    def make(self):
        """Build the component."""

        p = self.p

        bbox = draw.rectangle(2*p.length+p.gap, p.width, 0, 0)
        coupler_etch = draw.buffer(bbox, p.gnd_gap)

        gap = draw.rectangle(p.gap, p.width+2*p.gap, 0, 0)

        coupler = draw.subtract(bbox, gap)

        port_line_in = draw.LineString([(-p.length-p.gap/2, -p.cpw_width / 2), (-p.length-p.gap/2, p.cpw_width / 2)])
        port_line_out = draw.LineString([(p.length+p.gap/2, p.cpw_width / 2), (p.length+p.gap/2, -p.cpw_width / 2)])

        polys = [coupler, coupler_etch, port_line_in, port_line_out]

        polys = draw.translate(polys, p.length+p.gap/2, 0)
        polys = draw.rotate(polys, p.orientation, origin=(0, 0))

        polys = draw.translate(polys, p.pos_x, p.pos_y)


        [coupler, coupler_etch, port_line_in, port_line_out] = polys

        # generate qgeometry for metal and etch
        self.add_qgeometry('poly', {'coupler': coupler},
                           chip=p.chip)
        self.add_qgeometry('poly',
                           {'coupler_etch': coupler_etch},
                           subtract=True,
                           chip=p.chip)

        self.add_pin("in", port_line_in.coords, p.cpw_width)
        self.add_pin("out", port_line_out.coords, p.cpw_width)
