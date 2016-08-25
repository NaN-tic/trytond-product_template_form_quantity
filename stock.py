# This file is part of stock_product_form module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Configuration']


class Configuration:
    __metaclass__ = PoolMeta
    __name__ = 'stock.configuration'
    warehouse = fields.Property(fields.Many2One('stock.location', 'Warehouse',
        domain=[('type', '=', 'warehouse')]))
    lag_days = fields.Property(fields.Numeric('Number of lag days',
            digits=(16, 0)))
