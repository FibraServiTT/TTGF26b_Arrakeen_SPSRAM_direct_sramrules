# SPDX-License-Identifier: Apache-2.0
from typing import cast

from pdkmaster.technology import geometry as _geo, primitive as _prm
from pdkmaster import design as _dsgn

from c4m.pdk import sky130

_tech = sky130.tech
_prims = _tech.primitives

class TTTemplate1X1(_dsgn.FactoryOnDemandCell):
    def __init__(self, *, name: str, fab: _dsgn.CellFactory):
        super().__init__(name=name, fab=fab)

        self._c2l: _dsgn.Circuit2LayoutT | None

    @property
    def c2l(self) -> _dsgn.Circuit2LayoutT:
        if self._c2l is None:
            raise AttributeError(
                "TTTemplate1X1._create_layout_() has to be called before accessing 'c2l' attribute",
            )
        return self._c2l
    
    def _create_circuit_(self):
        ckt = self.new_circuit()

        ckt.new_net(name="clk", external=True)
        ckt.new_net(name="ena", external=True)
        ckt.new_net(name="rst_n", external=True)

        for bit in range(8):
            ckt.new_net(name=f"ui_in[{bit}]", external=True)
            ckt.new_net(name=f"uio_in[{bit}]", external=True)
            ckt.new_net(name=f"uio_oe[{bit}]", external=True)
            ckt.new_net(name=f"uio_out[{bit}]", external=True)
            ckt.new_net(name=f"uo_out[{bit}]", external=True)

        ckt.new_net(name="VGND", external=True)
        ckt.new_net(name="VDPWR", external=True)

    def _create_layout_(self):
        m4 = cast(_prm.MetalWire, _prims["m4"])
        prBoundary = cast(_prm.Auxiliary, _prims["prBoundary"])

        ckt = self.circuit
        nets = ckt.nets

        self._c2l = c2l = self.new_circuit2layout()

        c2l.set_boundary(
            bnd=_geo.Rect(left=0.0, bottom=0.0, right=161.0, top=111.52),
            extra_layer=prBoundary,
        )

        pin_shape = _geo.Rect.from_size(width=0.3, height=1.0)

        for n, net_name in enumerate((
            "ena", "clk", "rst_n",
            *(f"ui_in[{bit}]" for bit in range(8)),
            *(f"uio_in[{bit}]" for bit in range(8)),
            *(f"uo_out[{bit}]" for bit in range(8)),
            *(f"uio_out[{bit}]" for bit in range(8)),
            *(f"uio_oe[{bit}]" for bit in range(8)),
        )):
            x = 146.74 - n*2.76
            c2l.new_wire(
                net=nets[net_name], wire=m4, pin=True, shape=pin_shape, origin=_geo.Point(x=x, y=111.02),
            )
