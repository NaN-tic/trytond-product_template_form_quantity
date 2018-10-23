# This file is part of stock_product_form module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond import backend
from trytond.model import ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.tools.multivalue import migrate_property
from trytond.modules.company.model import CompanyValueMixin

__all__ = ['Configuration', 'ConfigurationProductTemplateFormQuantity']

warehouse = fields.Many2One('stock.location', 'Warehouse',
    domain=[('type', '=', 'warehouse')])
lag_days = fields.Numeric('Number of lag days', digits=(16, 0))


class Configuration(metaclass=PoolMeta):
    __name__ = 'stock.configuration'
    warehouse = fields.MultiValue(warehouse)
    lag_days = fields.MultiValue(lag_days)

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field in ('warehouse', 'lag_days'):
            return pool.get('stock.configuration.product_template_form_quantity')
        return super(Configuration, cls).multivalue_model(field)


class ConfigurationProductTemplateFormQuantity(ModelSQL, CompanyValueMixin):
    "Stock Configuration Product Template Form Quantity"
    __name__ = 'stock.configuration.product_template_form_quantity'
    warehouse = warehouse
    lag_days = lag_days

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        exist = TableHandler.table_exist(cls._table)

        super(ConfigurationProductTemplateFormQuantity, cls).__register__(
            module_name)

        if not exist:
            cls._migrate_property([], [], [])

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.extend(['warehouse','lag_days'])
        value_names.extend(['warehouse','lag_days'])
        fields.append('company')
        migrate_property('stock.configuration', field_names, cls, value_names,
            fields=fields)
