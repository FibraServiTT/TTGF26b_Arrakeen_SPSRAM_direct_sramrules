# SPDX-License-Identifier: Apache-2.0
from typing import cast

from pdkmaster import technology as _tch
from pdkmaster.technology import geometry as _geo
from pdkmaster import design as _dsgn

from c4m.pdk import sky130
prims = sky130.tech.primitives

from template import TTTemplate1X1


name = "tt_um_c4m_spsram_direct"

class Top(TTTemplate1X1):
    def __init__(self, *, fab: _dsgn.CellFactory):
        super().__init__(name=name, fab=fab)

    def _create_layout_(self):
        super()._create_layout_()

        m4 = cast(_tch.MetalWire, prims["m4"])

        ckt = self.circuit
        nets = ckt.nets

        vss = nets["VGND"]
        vdd = nets["VDPWR"]

        c2l = self.c2l

        bnd = self.layout.boundary

        x_mid = 0.5*bnd.right
        w = 11.0
        s = 0.4

        bottom = 2.0
        top = bnd.top - 2.0

        right = x_mid - 0.5*s
        left = right - w
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        c2l.new_wire(net=vss, wire=m4, pin=True, shape=shape)

        left = x_mid + 0.5*s
        right = left + w
        shape = _geo.Rect(left=left, bottom=bottom, right=right, top=top)
        c2l.new_wire(net=vdd, wire=m4, pin=True, shape=shape)
