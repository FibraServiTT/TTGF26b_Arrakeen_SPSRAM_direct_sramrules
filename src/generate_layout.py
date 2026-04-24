#!/bin/env python3
# SPDX-License-Identifier: Apache-2.0
from typing import Any

from pdkmaster import design as _dsgn
from pdkmaster.io.klayout import export2db

from c4m.pdk import sky130

import pya
pya: Any

from top import Top

lib = sky130.Library(name="TTSKY_SRAM")
fab = sky130.CellFactory(lib=lib)
top = Top(fab=fab)
lib.cells += top


kltech = pya.Technology.technology_by_name("C4M.IHPSG13G2")
klsaveopt = kltech.save_layout_options.dup()
klsaveopt.write_context_info = False

kldb = export2db(
    lib, gds_layers=sky130.gds_layers,
    add_pin_label=True,
)

kldb.write(f"gds/{top.name}.gds")
