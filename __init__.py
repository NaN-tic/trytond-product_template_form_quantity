# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .product import *
from .stock import *


def register():
    Pool.register(
        Template,
        Configuration,
        Lot,
        module='product_template_form_quantity', type_='model')
    Pool.register(
        LotReport,
        module='stock_move_jreport', type_='report')
